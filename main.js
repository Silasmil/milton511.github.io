/* main.js — somas3ccybersecurity. All interactive logic, no deps. */
(function () {
  "use strict";

  /* ---------- THEME ---------- */
  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    try { localStorage.setItem("theme", theme); } catch (e) {}
    var btn = document.querySelector(".theme-toggle");
    if (btn) btn.textContent = theme === "dark" ? "☀ Light" : "🌙 Dark";
  }
  window.toggleTheme = function () {
    var cur = document.documentElement.getAttribute("data-theme") || "dark";
    applyTheme(cur === "dark" ? "light" : "dark");
  };
  (function initTheme() {
    var saved = null;
    try { saved = localStorage.getItem("theme"); } catch (e) {}
    if (!saved) {
      var prefersLight = window.matchMedia &&
        window.matchMedia("(prefers-color-scheme: light)").matches;
      saved = prefersLight ? "light" : "dark";
    }
    applyTheme(saved);
  })();

  /* ---------- INJECT HEADER ---------- */
  function injectHeader(cb) {
    if (document.querySelector(".site-header")) { cb(); return; }
    fetch("header.html")
      .then(function (r) { return r.ok ? r.text() : Promise.reject(); })
      .then(function (html) {
        var wrap = document.createElement("div");
        wrap.innerHTML = html;
        var frag = document.createDocumentFragment();
        while (wrap.firstChild) frag.appendChild(wrap.firstChild);
        document.body.insertBefore(frag, document.body.firstChild);
        cb();
      })
      .catch(function () { cb(); });
  }

  /* ---------- ACTIVE NAV ---------- */
  function markActiveNav() {
    var here = location.pathname.split("/").pop() || "index.html";
    document.querySelectorAll(".nav-links a").forEach(function (a) {
      if ((a.getAttribute("href") || "") === here) a.classList.add("active");
    });
  }

  /* ---------- NINJA ---------- */
  function initNinja() {
    var ninja = document.getElementById("ninja");
    if (!ninja) return;
    var reduce = window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var touch = window.matchMedia && window.matchMedia("(hover: none)").matches;
    if (reduce || touch) { ninja.remove(); return; }
    document.body.classList.add("ninja-on");
    var x = innerWidth / 2, y = innerHeight / 2, nx = x, ny = y;
    document.addEventListener("mousemove", function (e) { x = e.clientX; y = e.clientY; });
    (function loop() {
      nx += (x - nx) * 0.22;
      ny += (y - ny) * 0.22;
      var flip = (x - nx) < -0.5 ? "scaleX(-1)" : "scaleX(1)";
      ninja.style.transform = "translate(" + nx + "px," + ny + "px) translate(-50%,-50%) " + flip;
      requestAnimationFrame(loop);
    })();
  }

  /* ---------- REVEAL ---------- */
  function initReveal() {
    var els = document.querySelectorAll(".reveal");
    if (!els.length) return;
    if (!("IntersectionObserver" in window)) {
      els.forEach(function (el) { el.classList.add("in"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.12 });
    els.forEach(function (el) { io.observe(el); });
  }

  /* ---------- COPY BUTTONS ---------- */
  function initCopyButtons() {
    document.querySelectorAll("pre").forEach(function (pre) {
      if (pre.querySelector(".copy-btn")) return;
      var btn = document.createElement("button");
      btn.className = "copy-btn";
      btn.type = "button";
      btn.textContent = "Copy";
      btn.setAttribute("aria-label", "Copy code to clipboard");
      btn.addEventListener("click", function () {
        var code = pre.querySelector("code");
        var text = code ? code.innerText : pre.innerText;
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(function () {
            btn.textContent = "Copied!";
            btn.classList.add("copied");
            setTimeout(function () {
              btn.textContent = "Copy";
              btn.classList.remove("copied");
            }, 1500);
          });
        }
      });
      pre.appendChild(btn);
    });
  }

  /* ---------- PROGRESS ---------- */
  function initProgress() {
    var bar = document.getElementById("progress-bar");
    var article = document.querySelector(".writeup-body");
    if (!bar || !article) return;
    function update() {
      var rect = article.getBoundingClientRect();
      var total = article.offsetHeight - window.innerHeight;
      var scrolled = Math.max(0, -rect.top);
      var pct = total > 0 ? Math.min(100, (scrolled / total) * 100) : 0;
      bar.style.width = pct + "%";
    }
    window.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    update();
  }

  /* ---------- SKILL BARS ---------- */
  function initSkillBars() {
    var bars = document.querySelectorAll(".skill-bar span[data-level]");
    if (!bars.length) return;
    if (!("IntersectionObserver" in window)) {
      bars.forEach(function (el) { el.style.width = el.getAttribute("data-level") + "%"; });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          var el = e.target;
          el.style.width = el.getAttribute("data-level") + "%";
          io.unobserve(el);
        }
      });
    }, { threshold: 0.4 });
    bars.forEach(function (el) { io.observe(el); });
  }

  /* ---------- COMMAND PALETTE ---------- */
  var PAGES = [
    { label: "Home",         href: "index.html",       hint: "Page" },
    { label: "About",        href: "about.html",       hint: "Page" },
    { label: "Skills",       href: "skills.html",      hint: "Page" },
    { label: "Writeups",     href: "writeups.html",    hint: "Page" },
    { label: "Labs",         href: "labs.html",        hint: "Page" },
    { label: "Projects",     href: "projects.html",    hint: "Page" },
    { label: "Roadmap",      href: "roadmap.html",     hint: "Page" },
    { label: "CV",           href: "cv.html",          hint: "Page" },
    { label: "Cover Letter", href: "coverletter.html", hint: "Page" },
    { label: "Contact",      href: "contact.html",     hint: "Page" },
    { label: "Hire Me",      href: "hire.html",        hint: "Page" }
  ];

  var WRITEUPS = [
    { label: "Secure App",                href: "writeups/secure-app.html",             hint: "Mobile · Easy" },
    { label: "Rooted or not?",            href: "writeups/rooted-or-not.html",          hint: "Mobile · Easy" },
    { label: "Loaded Dice",               href: "writeups/loaded-dice.html",            hint: "Smart Contract · Easy" },
    { label: "The Vault That Ate Itself", href: "writeups/vault-that-ate-itself.html",  hint: "Smart Contract · Easy" },
    { label: "Echo Signature",            href: "writeups/echo-signature.html",         hint: "Smart Contract · Medium · First Blood" },
    { label: "Oracle",                    href: "writeups/oracle.html",                 hint: "Crypto · Medium" },
    { label: "Securebank",                href: "writeups/securebank.html",             hint: "Web · Easy" },
    { label: "Cleartext Catch",           href: "writeups/cleartext-catch.html",        hint: "Forensics · Easy" },
    { label: "No See Code",               href: "writeups/no-see-code.html",            hint: "Forensics · Easy" }
  ];

  function initPalette() {
    var overlay = document.getElementById("palette-overlay");
    var input = document.getElementById("palette-input");
    var list = document.getElementById("palette-list");
    var trigger = document.getElementById("palette-trigger");
    if (!overlay || !input || !list) return;

    var items = PAGES.concat(WRITEUPS);
    var filtered = items.slice();
    var selected = 0;

    function render() {
      list.innerHTML = "";
      if (!filtered.length) {
        var empty = document.createElement("li");
        empty.className = "empty";
        empty.textContent = "No matches";
        list.appendChild(empty);
        return;
      }
      filtered.forEach(function (item, i) {
        var li = document.createElement("li");
        if (i === selected) li.classList.add("selected");
        var left = document.createElement("span");
        left.textContent = item.label;
        var right = document.createElement("span");
        right.className = "hint";
        right.textContent = item.hint;
        li.appendChild(left);
        li.appendChild(right);
        li.addEventListener("click", function () { window.location.href = item.href; });
        li.addEventListener("mouseenter", function () { selected = i; render(); });
        list.appendChild(li);
      });
    }

    function openPalette() {
      overlay.classList.add("open");
      input.value = "";
      filtered = items.slice();
      selected = 0;
      render();
      setTimeout(function () { input.focus(); }, 30);
    }
    function closePalette() {
      overlay.classList.remove("open");
    }
    function updateFilter() {
      var q = input.value.toLowerCase().trim();
      filtered = items.filter(function (item) {
        return !q ||
          item.label.toLowerCase().indexOf(q) !== -1 ||
          item.hint.toLowerCase().indexOf(q) !== -1;
      });
      selected = 0;
      render();
    }

    input.addEventListener("input", updateFilter);
    input.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") {
        e.preventDefault();
        if (selected < filtered.length - 1) { selected++; render(); }
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        if (selected > 0) { selected--; render(); }
      } else if (e.key === "Enter") {
        e.preventDefault();
        if (filtered[selected]) window.location.href = filtered[selected].href;
      } else if (e.key === "Escape") {
        closePalette();
      }
    });
    overlay.addEventListener("click", function (e) {
      if (e.target === overlay) closePalette();
    });
    if (trigger) trigger.addEventListener("click", openPalette);

    document.addEventListener("keydown", function (e) {
      var meta = e.metaKey || e.ctrlKey;
      if (meta && e.key.toLowerCase() === "k") {
        e.preventDefault();
        if (overlay.classList.contains("open")) closePalette(); else openPalette();
      }
      if (e.key === "Escape" && overlay.classList.contains("open")) closePalette();
    });
  }

  /* ---------- FILTER CHIPS ---------- */
  function initFilters() {
    var chipGroups = document.querySelectorAll("[data-filter-group]");
    if (!chipGroups.length) return;
    chipGroups.forEach(function (group) {
      // Avoid double-binding if initFiltersNow runs twice
      if (group.dataset.bound === "1") return;
      group.dataset.bound = "1";
      var chips = group.querySelectorAll(".chip");
      var targetSelector = group.getAttribute("data-filter-target");
      var items = document.querySelectorAll(targetSelector + " [data-category]");
      chips.forEach(function (chip) {
        chip.addEventListener("click", function () {
          chips.forEach(function (c) {
            c.classList.remove("active");
            c.setAttribute("aria-selected", "false");
          });
          chip.classList.add("active");
          chip.setAttribute("aria-selected", "true");
          var cat = chip.getAttribute("data-filter");
          items.forEach(function (item) {
            var show = cat === "all" || item.getAttribute("data-category") === cat;
            item.style.display = show ? "" : "none";
          });
        });
      });
    });
  }

  /* ---------- FILTERS RE-INIT (exposed for dynamic pages) ---------- */
  window.initFiltersNow = initFilters;

  /* ---------- BOOT ---------- */
  injectHeader(function () {
    markActiveNav();
    initNinja();
    initReveal();
    initCopyButtons();
    initProgress();
    initSkillBars();
    initPalette();
    initFilters();
  });
})();
