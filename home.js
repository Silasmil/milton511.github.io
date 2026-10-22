/* home.js — typewriter + animated counters. No deps. */
(function () {
  "use strict";

  /* ---------- TYPEWRITER ---------- */
  var PHRASES = [
    "Milton Silas",
    "Red Team Specialist",
    "Cisco IT Essentials Instructor",
    "CTF Player — First Blood",
    "Fullstack Developer (in progress)",
    "Penetration Tester"
  ];
  var el = document.getElementById("typewriter");
  if (el) {
    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce) {
      el.textContent = "Milton Silas";
    } else {
      var phraseIdx = 0, charIdx = 0, deleting = false;
      var TYPE_MS = 80, DELETE_MS = 40, HOLD_MS = 1500, BETWEEN_MS = 400;

      function tick() {
        var current = PHRASES[phraseIdx];
        if (!deleting) {
          charIdx++;
          el.textContent = current.slice(0, charIdx);
          if (charIdx === current.length) {
            deleting = true;
            setTimeout(tick, HOLD_MS);
            return;
          }
          setTimeout(tick, TYPE_MS);
        } else {
          charIdx--;
          el.textContent = current.slice(0, charIdx);
          if (charIdx === 0) {
            deleting = false;
            phraseIdx = (phraseIdx + 1) % PHRASES.length;
            setTimeout(tick, BETWEEN_MS);
            return;
          }
          setTimeout(tick, DELETE_MS);
        }
      }
      tick();
    }
  }

  /* ---------- COUNTERS ---------- */
  var counters = document.querySelectorAll(".counter-num");
  if (!counters.length) return;

  function animateCounter(node) {
    var target = parseInt(node.getAttribute("data-target"), 10);
    if (isNaN(target) || target === 0) { node.textContent = target; return; }
    var start = 0, duration = 1200, startTime = null;
    function step(ts) {
      if (!startTime) startTime = ts;
      var progress = Math.min((ts - startTime) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3);
      node.textContent = Math.round(eased * target);
      if (progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    counters.forEach(function (n) {
      n.textContent = n.getAttribute("data-target");
    });
    return;
  }

  if (!("IntersectionObserver" in window)) {
    counters.forEach(animateCounter);
    return;
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) {
        animateCounter(e.target);
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.4 });
  counters.forEach(function (n) { io.observe(n); });
})();
