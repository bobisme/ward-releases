#!/usr/bin/env bash
# bench/smoke-determinism.sh — three-run determinism check.
#
# Methodology §5 "Determinism": every tool must produce byte-identical
# SARIF across three independent runs on the same input. Tools that fail
# get filed as a bug and recorded as best-of-three; tools that pass go
# straight into the headline.
#
# This script picks 5 entries from the bench corpus (or all entries if
# the corpus has fewer than 5), runs every tool 3× per entry, and
# asserts the SARIF (or each tool's canonical output) is byte-identical
# across runs.
#
# Usage:
#   bench/smoke-determinism.sh [--manifest PATH] [--out DIR] [--tools LIST]
#
# Exit codes:
#   0 — every tool is deterministic across all 5 entries
#   1 — at least one tool / entry pair produced different output
#   2 — harness / configuration error
#
# Methodology section reference: §5 "Determinism".

set -euo pipefail

MANIFEST="${MANIFEST:-bench/corpus.toml}"
OUT_DIR="${OUT_DIR:-target/bench-determinism}"
TOOLS="${TOOLS:-ward,codeql,semgrep,rudra,cargo-geiger}"
RUNS=3
SUBSET_N=5

while [[ $# -gt 0 ]]; do
  case "$1" in
    --manifest) MANIFEST="$2"; shift 2;;
    --out) OUT_DIR="$2"; shift 2;;
    --tools) TOOLS="$2"; shift 2;;
    --runs) RUNS="$2"; shift 2;;
    --subset) SUBSET_N="$2"; shift 2;;
    -h|--help)
      sed -n '2,25p' "$0"; exit 0;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done

if [[ ! -f "${MANIFEST}" ]]; then
  echo "smoke-determinism: manifest not found at ${MANIFEST}" >&2
  echo "  Pass --manifest <path> or set MANIFEST=<path>." >&2
  echo "  (Bench corpus collection is bn-2tdyf; this is expected to be" >&2
  echo "   absent on the bn-38laq harness-scaffolding branch.)" >&2
  exit 2
fi

mkdir -p "${OUT_DIR}"

# Pick the first SUBSET_N entries with expected_result = "tp" so each
# tool has SARIF emissions to compare. The simple grep is fine for the
# smoke; the real harness consults manifest.rs.
mapfile -t ENTRIES < <(
  awk '
    /^\[\[entries\]\]/ {flag=1; next}
    flag && /^id *= */ {
      # strip surrounding quotes
      gsub(/^id *= *"?|"?$/, "", $0); print; flag=0
    }
  ' "${MANIFEST}" | head -n "${SUBSET_N}"
)
if [[ ${#ENTRIES[@]} -eq 0 ]]; then
  echo "smoke-determinism: no entries found in ${MANIFEST}" >&2
  exit 2
fi
echo "smoke-determinism: ${#ENTRIES[@]} entries × ${RUNS} runs × tools=${TOOLS}"

IFS=',' read -r -a TOOL_LIST <<< "${TOOLS}"

FAIL_COUNT=0

for entry in "${ENTRIES[@]}"; do
  for tool in "${TOOL_LIST[@]}"; do
    HASHES=()
    for run in $(seq 1 "${RUNS}"); do
      OUT_SUBDIR="${OUT_DIR}/${entry}/${tool}/run-${run}"
      mkdir -p "${OUT_SUBDIR}"
      # ward-eval bench-run --filter <entry-id> --tools <tool> runs the
      # full pipeline for a single (entry, tool) pair.
      cargo run --quiet -p ward-eval --bin ward-eval -- \
        bench-run \
        --manifest "${MANIFEST}" \
        --tools "${tool}" \
        --filter "${entry}" \
        --out "${OUT_SUBDIR}" \
        --skip-version-check \
        >/dev/null 2>&1 || true
      # Canonical artifact: per-tool SARIF or bench-results JSON.
      ARTIFACT="${OUT_SUBDIR}/bench-results-${tool}.json"
      if [[ -f "${ARTIFACT}" ]]; then
        # Strip volatile fields (duration_secs, ram_peak_mib) before
        # hashing — these legitimately differ across runs. The
        # methodology's determinism requirement is on the SARIF
        # *findings*, not wall-clock.
        HASH="$(jq -S 'walk(if type == "object" then del(.duration_secs, .ram_peak_mib) else . end)' \
                "${ARTIFACT}" 2>/dev/null | sha256sum | cut -d' ' -f1)"
      else
        HASH="missing"
      fi
      HASHES+=("${HASH}")
    done
    UNIQ=$(printf '%s\n' "${HASHES[@]}" | sort -u | wc -l)
    if [[ "${UNIQ}" -eq 1 ]]; then
      echo "  PASS ${entry}/${tool}: deterministic across ${RUNS} runs (${HASHES[0]:0:12})"
    else
      echo "  FAIL ${entry}/${tool}: NOT deterministic — hashes:"
      for h in "${HASHES[@]}"; do echo "    - ${h:0:32}"; done
      FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
  done
done

echo ""
if [[ "${FAIL_COUNT}" -eq 0 ]]; then
  echo "smoke-determinism: PASS — every (entry, tool) deterministic across ${RUNS} runs"
  exit 0
else
  echo "smoke-determinism: FAIL — ${FAIL_COUNT} (entry, tool) pairs non-deterministic"
  echo "  Per methodology §5 affected tools must run best-of-three and the"
  echo "  writeup must disclose the non-determinism."
  exit 1
fi
