// Ward — landing page interactivity

(function () {
  function animateBars() {
    document.querySelectorAll(".bar-fill").forEach(el => {
      const w = el.style.getPropertyValue("--w") || el.dataset.w || "0%";
      el.style.width = "0%";
      requestAnimationFrame(() => {
        requestAnimationFrame(() => { el.style.width = w; });
      });
    });
  }

  let traceTimer = null;
  function startTrace() {
    if (traceTimer) { clearInterval(traceTimer); traceTimer = null; }
    const svg = document.querySelector(".trace .links");
    const badge = document.getElementById("traceBadge");
    const files = document.querySelectorAll(".trace .file");
    if (!svg || !badge) return;

    function run() {
      svg.querySelectorAll("path").forEach(p => p.classList.remove("active"));
      files.forEach(f => f.classList.remove("hit-pulse"));
      badge.classList.remove("show");

      const paths = svg.querySelectorAll("path");
      paths.forEach((p, i) => {
        setTimeout(() => { p.classList.add("active"); files[i+1]?.classList.add("hit-pulse"); }, 400 + i * 700);
      });
      setTimeout(() => badge.classList.add("show"), 1900);
    }
    run();
    traceTimer = setInterval(run, 4200);
  }

  function init() {
    animateBars();
    startTrace();

    const cmp = document.getElementById("cmp");
    if (cmp && "IntersectionObserver" in window) {
      const io = new IntersectionObserver((entries) => {
        entries.forEach(e => { if (e.isIntersecting) animateBars(); });
      }, { threshold: 0.35 });
      io.observe(cmp);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
