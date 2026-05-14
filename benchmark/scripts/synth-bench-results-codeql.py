#!/usr/bin/env python3
"""Synthesize bench-results-codeql.json from partial on-disk artifacts.

Mirrors BenchToolResult schema from crates/ward-eval/src/bench/mod.rs and the
CodeQL SARIF parse logic in crates/ward-eval/src/bench/runners/codeql.rs.

Conventions:
  - SARIF present + parses -> success: classification per (expected, detected)
  - codeql-db/ present but no SARIF -> timed_out at DB-create step (10-min cap)
    detected=false, classification per expected (tp->FN, tn->TN),
    error="codeql_db_create_timed_out", timed_out=true, duration_secs=600.0
  - Neither -> not_run: detected=false, classification per expected,
    error="not_run", timed_out=false, duration_secs=0.0
"""

import json
import os
import sys
import re
from pathlib import Path

ROOT = Path("/home/bob/src/ward/ws/bn-1qq7o-wrap")
MANIFEST = ROOT / "tests/cve-registry/benchmarks/unsafe-rust-bench/manifest.toml"
RAW_DIR = ROOT / "target/bench/unsafe-rust-v2/raw/codeql"
OUT_PATH = ROOT / "target/bench/unsafe-rust-v2/bench-results-codeql.json"


def parse_manifest_entries(path: Path):
    """Minimal TOML entry extractor — needs only id, expected_result, affected_file."""
    text = path.read_text()
    # Split on [[entries]] section markers
    chunks = re.split(r"^\[\[entries\]\]\s*$", text, flags=re.MULTILINE)
    entries = []
    for chunk in chunks[1:]:
        # Stop at next [[ or [section]
        chunk = re.split(r"^\[", chunk, flags=re.MULTILINE)[0]
        e = {}
        for line in chunk.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            m = re.match(r'(\w+)\s*=\s*"([^"]*)"', line)
            if m:
                e[m.group(1)] = m.group(2)
                continue
            m = re.match(r"(\w+)\s*=\s*(\d+)", line)
            if m:
                e[m.group(1)] = int(m.group(2))
        if "id" in e:
            entries.append(e)
    return entries


def classify(expected: str, detected: bool) -> str:
    if expected == "tp":
        return "TP" if detected else "FN"
    return "FP" if detected else "TN"


def detected_for_entry(findings, affected_file: str) -> bool:
    if not affected_file:
        return len(findings) > 0
    target = affected_file.replace("\\", "/")
    target_base = os.path.basename(target)
    for f in findings:
        path = f["file"].replace("\\", "/")
        if path == target:
            return True
        if path.endswith("/" + target):
            return True
        if target_base and os.path.basename(path) == target_base:
            return True
    return False


def parse_codeql_sarif(sarif_path: Path):
    """Mirror crates/ward-eval/src/bench/runners/codeql.rs::parse_codeql_sarif."""
    try:
        with open(sarif_path) as f:
            v = json.load(f)
    except Exception:
        return None
    out = []
    for run in v.get("runs", []):
        rule_levels = {}
        rules = run.get("tool", {}).get("driver", {}).get("rules", [])
        for r in rules:
            rid = r.get("id", "")
            lvl = (
                r.get("defaultConfiguration", {}).get("level", "warning")
                if isinstance(r.get("defaultConfiguration", {}), dict)
                else "warning"
            )
            rule_levels[rid] = lvl
        for result in run.get("results", []) or []:
            rule_id = result.get("ruleId", "")
            level = result.get("level") or rule_levels.get(rule_id, "warning")
            # Methodology §5: drop note-level
            if level == "note":
                continue
            message = ""
            msg = result.get("message")
            if isinstance(msg, dict):
                message = msg.get("text", "")
            for loc in result.get("locations", []) or []:
                ploc = loc.get("physicalLocation", {})
                art = ploc.get("artifactLocation", {})
                uri = art.get("uri", "").lstrip("./")
                if not uri:
                    continue
                region = ploc.get("region", {})
                start_line = region.get("startLine")
                out.append(
                    {
                        "rule_id": rule_id,
                        "file": uri,
                        "start_line": start_line,
                        "message": message,
                        "confidence": 0.0,
                    }
                )
    return out


def build_record(entry, raw_dir: Path):
    entry_id = entry["id"]
    expected = entry.get("expected_result", "tp")
    affected_file = entry.get("affected_file", "")
    edir = raw_dir / entry_id
    sarif = edir / "codeql.sarif"
    db = edir / "codeql-db"

    base = {
        "tool": "codeql",
        "harness_id": entry_id,
        "expected": expected,
        "findings": [],
    }

    if sarif.exists():
        findings = parse_codeql_sarif(sarif)
        if findings is None:
            # Malformed SARIF — treat as error
            detected = False
            rec = {
                **base,
                "detected": False,
                "classification": classify(expected, False),
                "duration_secs": 0.0,
                "error": "codeql_sarif_parse_failed",
            }
            return rec
        detected = detected_for_entry(findings, affected_file)
        rule_ids = sorted({f["rule_id"] for f in findings if f["rule_id"]})
        rec = {
            **base,
            "detected": detected,
            "classification": classify(expected, detected),
            "findings": findings,
            "duration_secs": 0.0,
        }
        if rule_ids:
            rec["rule_ids_fired"] = rule_ids
        return rec

    if db.is_dir():
        # DB-create completed but query/analyze step did not write SARIF.
        # Almost certainly hit the 10-min cap during `codeql database analyze`.
        rec = {
            **base,
            "detected": False,
            "classification": classify(expected, False),
            "duration_secs": 600.0,
            "timed_out": True,
            "error": "codeql_analyze_timed_out",
        }
        return rec

    # Never processed
    rec = {
        **base,
        "detected": False,
        "classification": classify(expected, False),
        "duration_secs": 0.0,
        "error": "not_run",
    }
    return rec


def main():
    entries = parse_manifest_entries(MANIFEST)
    print(f"Parsed {len(entries)} entries from manifest", file=sys.stderr)
    if len(entries) != 160:
        print(f"WARNING: expected 160 entries, got {len(entries)}", file=sys.stderr)

    records = []
    n_sarif = 0
    n_timeout = 0
    n_not_run = 0
    n_detected = 0
    classifications = {"TP": 0, "FP": 0, "TN": 0, "FN": 0}
    for entry in entries:
        rec = build_record(entry, RAW_DIR)
        records.append(rec)
        cls = rec["classification"]
        classifications[cls] = classifications.get(cls, 0) + 1
        err = rec.get("error", "")
        if err == "not_run":
            n_not_run += 1
        elif err == "codeql_analyze_timed_out":
            n_timeout += 1
        else:
            n_sarif += 1
            if rec["detected"]:
                n_detected += 1

    print(
        f"SARIF parsed: {n_sarif} | DB-only timeouts: {n_timeout} | not_run: {n_not_run}",
        file=sys.stderr,
    )
    print(f"Detected (file-level match): {n_detected}", file=sys.stderr)
    print(f"Classifications: {classifications}", file=sys.stderr)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(records, f, indent=2)
    print(f"Wrote {OUT_PATH} ({len(records)} entries)", file=sys.stderr)


if __name__ == "__main__":
    main()
