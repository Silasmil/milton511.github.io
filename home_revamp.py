#!/usr/bin/env python3
"""
home_revamp.py
- Adds OG/Twitter/Canonical/JSON-LD meta tags to all 22 HTML files.
- Injects the GoatCounter tracking script (skips localhost).
- Rewrites index.html with the typewriter hero, animated counters,
  6 featured cards, "by the numbers" band, and CTA.
- Creates home.js (typewriter + counter animation).
- Appends the new CSS to style.css.
- Creates og-default.png via inline SVG (no deps).
"""
import pathlib, re, sys, os

ROOT = pathlib.Path(__file__).resolve().parent
SITE = "https://silasmil.github.io"
SITE_NAME = "somas3ccybersecurity"
GC_SNIPPET = '''<script data-goatcounter="https://somas3c.goatcounter.com/count"
        async src="//gc.zgo.at/count.js"></script>
<script>
  // Skip tracking on localhost so local previews don't pollute the dashboard
  if (location.hostname === "localhost" || location.hostname === "127.0.0.1") {
    if (window.goatcounter) window.goatcounter.ignore = true;
  }
</script>'''

# ---------------------------------------------------------------
# 1. META injection — every page
# ---------------------------------------------------------------
PAGES = {
    "index.html":           ("Home", "Cybersecurity analyst, red team specialist, and Cisco instructor. 9 CTF writeups, real labs, and fullstack projects.", "website"),
    "about.html":           ("About", "Cybersecurity analyst and red team specialist based in Kenya. Cisco instructor. Fullstack developer in progress.", "website"),
    "skills.html":          ("Skills", "Web, mobile, smart contract, and network security. Detection, IR, and secure code review. Fullstack in progress.", "website"),
    "writeups.html":        ("CTF Writeups", "9 CTF writeups from Perfect Root (AfricaHackon). First Blood on Echo Signature (ECDSA malleability). Every flag included.", "website"),
    "labs.html":            ("Labs & Workshops", "Cisco IT Essentials, CCNP Inter-VLAN routing lab, Future Interns cybersecurity portfolio, and Perfect Root CTF.", "website"),
    "projects.html":        ("Projects", "Pentest Toolkit (v1.1), SomaSec (in dev), the CTF Writeup Engine, and this portfolio.", "website"),
    "roadmap.html":         ("Roadmap", "OSCP and CRTP in progress. Cloud security, smart contract audit, and 20 CTF writeups in the roadmap.", "website"),
    "cv.html":              ("CV", "CV of Milton Silas — Cybersecurity Analyst, Red Team Specialist, Cisco Instructor.", "website"),
    "coverletter.html":     ("Cover Letter", "Cover letter of Milton Silas for cybersecurity, red team, and training roles.", "website"),
    "contact.html":         ("Contact", "Contact Milton Silas — email, GitHub, and hire inquiry. Based in Kilifi, Kenya.", "website"),
    "hire.html":            ("Hire Me", "Pentesting, secure code review, and security training. Fixed-scope engagements from a working red team specialist.", "website"),
    "404.html":             ("Not Found", "This page does not exist.", "website"),
    "playbook.html":        ("Home-Lab Playbook", "A minimalist cybersecurity home-lab playbook. From zero to a working red-team lab in one weekend, using one laptop.", "article"),
    "signal.html":          ("Signal", "The cybersecurity and IT feed I actually read. Updated daily at 06:00 EAT. Kenya, Africa, and global.", "website"),
}

# writeups pages
WRITEUPS = {
    "secure-app":           ("Secure App — Android Hardcoded Secret", "Hardcoded credential inside an APK, recovered by static analysis. No device, no root, no runtime.", "article"),
    "rooted-or-not":        ("Rooted or not? — Android Root-Check Bypass", "XOR-encoded flag behind a client-side root check. The decryption algorithm is fully visible in smali.", "article"),
    "loaded-dice":          ("Loaded Dice — Predictable Randomness", "On-chain lottery with predictable randomness. Winner reconstructed offline from block fields.", "article"),
    "vault-that-ate-itself":("The Vault That Ate Itself — Reentrancy", "Textbook reentrancy in withdraw(). Recursive drain in a single transaction, flag derived from the function selector.", "article"),
    "echo-signature":       ("Echo Signature — ECDSA Malleability", "ECDSA signature malleability enabling replay. First Blood — flag derived from the malleated signature hash.", "article"),
    "oracle":               ("Oracle — CBC Padding Oracle", "CBC padding oracle attack against a silent binary. Full plaintext recovered byte-by-byte from exit codes alone.", "article"),
    "securebank":           ("Securebank — SQLi → SSTI → RCE", "SQLi → client-trusted JWT → SSTI in EJS. Three bugs chained into full remote code execution.", "article"),
    "cleartext-catch":      ("Cleartext Catch — PCAP / FTP", "FTP credentials and a backup file recovered from a PCAP. Carved from a raw TCP stream and unlocked with the reused password.", "article"),
    "no-see-code":          ("No See Code — Zero-Width Steganography", "Zero-width Unicode steganography inside a password-protected zip. Two-channel payload decoded byte-by-byte.", "article"),
}

def meta_block(title, description, ogtype, url, image):
    return f'''<meta property="og:type" content="{ogtype}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:image" content="{image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{image}">
<link rel="canonical" href="{url}">'''

def person_schema():
    return '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Person",
"name":"Milton Silas",
"url":"https://silasmil.github.io/",
"jobTitle":"Cybersecurity Analyst, Red Team Specialist, Cisco Instructor",
"worksFor":{"@type":"Organization","name":"somas3ccybersecurity"},
"address":{"@type":"PostalAddress","addressLocality":"Kilifi","addressCountry":"KE"},
"sameAs":["https://github.com/Silasmil"],
"knowsAbout":["Penetration Testing","Red Teaming","Web Application Security","Smart Contract Security","Network Security","Android Security","CTF"]}
</script>'''

def article_schema(title, description, url):
    return f'''<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article",
"headline":"{title}",
"description":"{description}",
"url":"{url}",
"author":{{"@type":"Person","name":"Milton Silas"}},
"publisher":{{"@type":"Organization","name":"{SITE_NAME}"}}}}
</script>'''

def inject_meta(path, title, description, ogtype, url, image):
    src = path.read_text(encoding="utf-8")
    if 'property="og:title"' in src:
        return False  # already has meta
    block = meta_block(title, description, ogtype, url, image)
    if ogtype == "article":
        block += "\n" + article_schema(title, description, url)
    # insert before </head>
    src = src.replace("</head>", block + "\n</head>", 1)
    # also ensure title tag is right
    src = re.sub(r"<title>[^<]*</title>", f"<title>{title} — {SITE_NAME}</title>", src, count=1)
    path.write_text(src, encoding="utf-8")
    return True

def inject_goatcounter(path):
    src = path.read_text(encoding="utf-8")
    if "goatcounter.com" in src:
        return False
    src = src.replace("</body>", GC_SNIPPET + "\n</body>", 1)
    path.write_text(src, encoding="utf-8")
    return True

print("== 1. inject meta + goatcounter ==")
for filename, (title, desc, ogtype) in PAGES.items():
    p = ROOT / filename
    if not p.exists():
        print(f"  · {filename} (missing, skipped)")
        continue
    url = f"{SITE}/" if filename == "index.html" else f"{SITE}/{filename}"
    image = f"{SITE}/og-default.png"
    ok_m = inject_meta(p, title, desc, ogtype, url, image)
    ok_g = inject_goatcounter(p)
    print(f"  · {filename} → meta={'✓' if ok_m else '='} gc={'✓' if ok_g else '='}")

# homepage gets Person schema too
idx = ROOT / "index.html"
if idx.exists():
    src = idx.read_text(encoding="utf-8")
    if 'application/ld+json' not in src:
        src = src.replace("</head>", person_schema() + "\n</head>", 1)
        idx.write_text(src, encoding="utf-8")

print("== 2. inject meta into writeups/*.html ==")
for slug, (title, desc, ogtype) in WRITEUPS.items():
    p = ROOT / "writeups" / f"{slug}.html"
    if not p.exists():
        print(f"  · {slug}.html (missing, skipped)")
        continue
    url = f"{SITE}/writeups/{slug}.html"
    image = f"{SITE}/og-default.png"
    ok_m = inject_meta(p, title, desc, ogtype, url, image)
    ok_g = inject_goatcounter(p)
    print(f"  · {slug}.html → meta={'✓' if ok_m else '='} gc={'✓' if ok_g else '='}")

# ---------------------------------------------------------------
# 2. new homepage
# ---------------------------------------------------------------
HOME = r'''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>somas3ccybersecurity — Milton Silas · Red Team · CTF Writeups</title>
<meta name="description" content="Cybersecurity analyst, red team specialist, and Cisco instructor. 9 CTF writeups, real labs, and fullstack projects.">
<link rel="stylesheet" href="style.css">
<script>
(function () {
  try {
    var t = localStorage.getItem("theme");
    if (!t) t = window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", t);
  } catch (e) {}
})();
</script>
</head>
<body>

<a class="skip-link" href="#main">Skip to content</a>

<header class="site-header">
  <div class="nav-inner">
    <a class="brand" href="index.html">somas3c<span>c</span>ybersecurity</a>
    <nav aria-label="Main navigation">
      <ul class="nav-links">
        <li><a href="index.html">Home</a></li>
        <li><a href="about.html">About</a></li>
        <li><a href="skills.html">Skills</a></li>
        <li><a href="writeups.html">Writeups</a></li>
        <li><a href="labs.html">Labs</a></li>
        <li><a href="projects.html">Projects</a></li>
        <li><a href="signal.html">Signal</a></li>
        <li><a href="roadmap.html">Roadmap</a></li>
        <li><a href="cv.html">CV</a></li>
        <li><a href="contact.html">Contact</a></li>
      </ul>
    </nav>
    <span class="nav-spacer"></span>
    <button class="kbd-hint" type="button" id="palette-trigger" aria-label="Open command palette">
      Search <kbd>Ctrl</kbd><kbd>K</kbd>
    </button>
    <button class="theme-toggle" type="button" onclick="toggleTheme()" aria-label="Toggle light and dark theme">☀ Light</button>
  </div>
</header>

<div class="progress-bar" id="progress-bar" aria-hidden="true"></div>
<div id="ninja" aria-hidden="true">🥷</div>

<div class="palette-overlay" id="palette-overlay" role="dialog" aria-modal="true" aria-label="Command palette">
  <div class="palette">
    <input type="text" id="palette-input" placeholder="Jump to a page or writeup…" autocomplete="off" />
    <ul class="palette-list" id="palette-list"></ul>
    <div class="palette-footer">
      <span><kbd>↑</kbd><kbd>↓</kbd> navigate</span>
      <span><kbd>↵</kbd> open</span>
      <span><kbd>Esc</kbd> close</span>
    </div>
  </div>
</div>

<main id="main">

  <!-- ============ HERO ============ -->
  <section class="reveal" style="padding: 40px 0 20px;">
    <p style="color: var(--accent-hi); font-weight: 800; letter-spacing: 3px; font-size: 0.8em; margin: 0 0 12px;">
      CYBERSECURITY · RED TEAM · TRAINING
    </p>

    <h1 class="hero-name" style="font-size: clamp(2.4em, 6vw, 4em); line-height: 1.05; margin-bottom: 18px; border: none; padding: 0;">
      <span id="typewriter">Milton Silas</span><span class="cursor" aria-hidden="true">▊</span>
    </h1>

    <p style="font-size: clamp(1.1em, 2vw, 1.35em); font-weight: 600; max-width: 720px; margin: 0 0 20px;">
      I break systems to make them safer — and teach others to do the same.
    </p>
    <p class="muted" style="font-size: 1.05em; max-width: 720px; margin: 0 0 32px;">
      Cybersecurity analyst, red team specialist, and Cisco IT Essentials instructor.
      I run hands-on labs, write up every challenge I solve, and help teams find
      what attackers will find first.
    </p>
    <div style="display: flex; gap: 14px; flex-wrap: wrap; align-items: center; margin-bottom: 40px;">
      <a class="btn" href="hire.html">Hire me →</a>
      <a class="btn btn-ghost" href="writeups.html">Read writeups</a>
    </div>

    <!-- ANIMATED COUNTERS -->
    <div class="counter-grid" id="counters">
      <a class="counter" href="writeups.html">
        <span class="counter-num" data-target="9">0</span>
        <span class="counter-label">CTF Writeups</span>
      </a>
      <a class="counter" href="writeups/echo-signature.html">
        <span class="counter-num" data-target="1">0</span>
        <span class="counter-label">First Blood</span>
      </a>
      <a class="counter" href="labs.html">
        <span class="counter-num" data-target="5">0</span>
        <span class="counter-label">Labs &amp; Workshops</span>
      </a>
      <a class="counter" href="projects.html">
        <span class="counter-num" data-target="3">0</span>
        <span class="counter-label">Shipped Projects</span>
      </a>
    </div>
  </section>

  <hr class="divider">

  <!-- ============ WHAT I DO ============ -->
  <section class="reveal">
    <h2>What I do</h2>
    <div class="grid grid-3">
      <div class="card">
        <span class="badge" style="margin-bottom: 12px;">Offensive</span>
        <h3>Red teaming &amp; pentesting</h3>
        <p class="muted" style="margin: 0;">
          Web apps, APIs, Android, and smart contracts. Full-report engagements
          with reproduction steps a developer can actually action.
        </p>
      </div>
      <div class="card">
        <span class="badge" style="margin-bottom: 12px;">Defensive</span>
        <h3>Detection &amp; hardening</h3>
        <p class="muted" style="margin: 0;">
          Threat detection, incident response, and secure code review. I find
          what attackers will find, then help you close it.
        </p>
      </div>
      <div class="card">
        <span class="badge" style="margin-bottom: 12px;">Training</span>
        <h3>Workshops &amp; labs</h3>
        <p class="muted" style="margin: 0;">
          Cisco IT Essentials instructor. I build hands-on labs that take learners
          from "I read about it" to "I did it."
        </p>
      </div>
    </div>
  </section>

  <hr class="divider">

  <!-- ============ FEATURED SHOWCASE ============ -->
  <section class="reveal">
    <div style="display: flex; justify-content: space-between; align-items: end; gap: 20px; flex-wrap: wrap;">
      <h2 style="margin-bottom: 0;">Featured work</h2>
      <a href="writeups.html" style="font-size: 0.9em; padding-bottom: 10px;">Browse everything →</a>
    </div>
    <div class="grid grid-3" style="margin-top: 24px;">

      <article class="card">
        <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px;">
          <span class="badge">Smart Contract</span>
          <span class="badge badge-muted">Medium · 200 pts</span>
          <span class="badge">🏆 First Blood</span>
        </div>
        <h3 style="margin-top: 0;">Echo Signature</h3>
        <p class="muted" style="margin: 0 0 12px; font-size: 0.92em;">
          ECDSA malleability enables signature replay. One authorization, paid
          twice — flag derived from the malleated hash.
        </p>
        <div class="card-foot"><a href="writeups/echo-signature.html" style="font-weight: 700;">Read →</a></div>
      </article>

      <article class="card">
        <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px;">
          <span class="badge">Cryptography</span>
          <span class="badge badge-muted">Medium · 150 pts</span>
        </div>
        <h3 style="margin-top: 0;">Oracle</h3>
        <p class="muted" style="margin: 0 0 12px; font-size: 0.92em;">
          CBC padding oracle against a silent binary. Full plaintext recovered
          byte-by-byte from exit codes alone.
        </p>
        <div class="card-foot"><a href="writeups/oracle.html" style="font-weight: 700;">Read →</a></div>
      </article>

      <article class="card">
        <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px;">
          <span class="badge">CCNP</span>
          <span class="badge badge-muted">Packet Tracer</span>
        </div>
        <h3 style="margin-top: 0;">Enterprise Multi-VLAN Network</h3>
        <p class="muted" style="margin: 0 0 12px; font-size: 0.92em;">
          Production-ready network design for a 500+ employee enterprise.
          5 VLANs, 802.1Q trunking, SVI routing, WAN serial link.
        </p>
        <div class="card-foot"><a href="https://github.com/Silasmil/inter-vlan-routing-lab" target="_blank" rel="noopener" style="font-weight: 700;">View on GitHub →</a></div>
      </article>

      <article class="card">
        <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px;">
          <span class="badge">Tool</span>
          <span class="badge badge-muted">v1.1 · MIT</span>
        </div>
        <h3 style="margin-top: 0;">Pentest Toolkit</h3>
        <p class="muted" style="margin: 0 0 12px; font-size: 0.92em;">
          Modular Python toolkit for recon, port scanning, and web security
          header analysis. Self-updating. Shipped as a release.
        </p>
        <div class="card-foot"><a href="https://github.com/Silasmil/pentest-toolkit" target="_blank" rel="noopener" style="font-weight: 700;">View on GitHub →</a></div>
      </article>

      <article class="card">
        <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px;">
          <span class="badge">Internship</span>
          <span class="badge badge-muted">3 tasks</span>
        </div>
        <h3 style="margin-top: 0;">FUTURE_CS_01</h3>
        <p class="muted" style="margin: 0 0 12px; font-size: 0.92em;">
          Three-task cybersecurity internship: OWASP Juice Shop assessment,
          phishing detection, and API security analysis.
        </p>
        <div class="card-foot"><a href="https://github.com/Silasmil/FUTURE_CS_01" target="_blank" rel="noopener" style="font-weight: 700;">View on GitHub →</a></div>
      </article>

      <article class="card">
        <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px;">
          <span class="badge">Platform</span>
          <span class="badge badge-muted">In development</span>
        </div>
        <h3 style="margin-top: 0;">SomaSec</h3>
        <p class="muted" style="margin: 0 0 12px; font-size: 0.92em;">
          Full-stack cybersecurity learning and creator platform. Flask, React,
          PostgreSQL, Docker. Building the reading-history and auth layer now.
        </p>
        <div class="card-foot"><span class="muted" style="font-size: 0.9em;">Private — <a href="contact.html">ask for a walkthrough</a></span></div>
      </article>

    </div>
  </section>

  <hr class="divider">

  <!-- ============ BY THE NUMBERS ============ -->
  <section class="reveal">
    <div class="numbers-band">
      <div><strong>9</strong><span>CTF writeups · 1 First Blood</span></div>
      <div><strong>5+</strong><span>Hands-on labs &amp; workshops</span></div>
      <div><strong>3</strong><span>Shipped projects · 1 in development</span></div>
      <div><strong>2</strong><span>Certifications in progress (OSCP, CRTP)</span></div>
    </div>
  </section>

  <hr class="divider">

  <!-- ============ SIGNAL TEASER ============ -->
  <section class="reveal">
    <div class="card" style="border-color: var(--accent);">
      <div style="display: flex; justify-content: space-between; gap: 20px; flex-wrap: wrap; align-items: center;">
        <div style="flex: 1; min-width: 260px;">
          <p style="color: var(--accent-hi); font-weight: 800; letter-spacing: 3px; font-size: 0.75em; margin: 0 0 8px;">NEW</p>
          <h3 style="margin-top: 0;">Signal — the feed I actually read</h3>
          <p class="muted" style="margin: 0; font-size: 0.95em;">
            Daily cybersecurity, IT, and opportunity news — Kenya and Africa first,
            then global. Updated every morning at 06:00 EAT. Free.
          </p>
        </div>
        <a class="btn" href="signal.html">Open Signal →</a>
      </div>
    </div>
  </section>

  <hr class="divider">

  <!-- ============ COMING SOON — HOME LAB PLAYBOOK ============ -->
  <section class="reveal">
    <div class="card" style="border-color: var(--border);">
      <div style="display: flex; justify-content: space-between; gap: 20px; flex-wrap: wrap; align-items: flex-start;">
        <div style="flex: 1; min-width: 260px;">
          <p style="color: var(--accent-hi); font-weight: 800; letter-spacing: 3px; font-size: 0.75em; margin: 0 0 8px;">COMING Q2 2026</p>
          <h3 style="margin-top: 0;">The Minimalist Home-Lab Playbook</h3>
          <p class="muted" style="margin: 0 0 16px; font-size: 0.95em;">
            From zero to a working red-team lab in one weekend — one laptop,
            $0 in software. Seven chapters covering the stack, the network,
            the first exploit, the pivot, and the blue-side detection to
            watch your own attack.
          </p>
          <div style="display: flex; gap: 10px; flex-wrap: wrap;">
            <a class="btn" href="playbook.html">Read chapter 1 free →</a>
            <a class="btn btn-ghost" href="playbook.html#notify">Notify me at launch</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <hr class="divider">

  <!-- ============ CTA ============ -->
  <section class="reveal">
    <div class="card center" style="border-color: var(--accent); box-shadow: 0 0 40px rgba(225,29,46,0.18);">
      <h2 style="border-bottom: none; margin-top: 0; padding-bottom: 0;">Let's work together</h2>
      <p class="muted" style="max-width: 560px; margin: 12px auto 28px;">
        Pentesting, training, or secure code review — I'll scope it, run it,
        and write it up so your team can act on it.
      </p>
      <div style="display: flex; gap: 14px; flex-wrap: wrap; justify-content: center;">
        <a class="btn" href="hire.html">See services &amp; pricing →</a>
        <a class="btn btn-ghost" href="contact.html">Contact</a>
      </div>
    </div>
  </section>

</main>

<footer class="site-footer">
  <div class="footer-inner">
    <div>
      <h4>somas3ccybersecurity</h4>
      <p class="muted" style="font-size: 0.9em; margin: 0;">
        Cybersecurity analyst · Red team specialist · Cisco instructor.
        Writeups from CTFs, hands-on labs, and real-world testing.
      </p>
    </div>
    <div>
      <h4>Explore</h4>
      <ul>
        <li><a href="writeups.html">Writeups</a></li>
        <li><a href="labs.html">Labs</a></li>
        <li><a href="projects.html">Projects</a></li>
        <li><a href="signal.html">Signal</a></li>
        <li><a href="playbook.html">Home-Lab Playbook</a></li>
      </ul>
    </div>
    <div>
      <h4>Connect</h4>
      <ul>
        <li><a href="mailto:cyberwiseafrica@gmail.com">Email</a></li>
        <li><a href="https://github.com/Silasmil" target="_blank" rel="noopener">GitHub</a></li>
        <li><a href="hire.html">Hire me</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <span>© 2026 somas3ccybersecurity · Built on GitHub Pages</span>
    <span><a href="https://github.com/Silasmil/silasmil.github.io" target="_blank" rel="noopener">Source</a></span>
  </div>
</footer>

<script src="main.js"></script>
<script src="home.js"></script>
</body>
</html>
'''

(ROOT / "index.html").write_text(HOME, encoding="utf-8")
print("✓ index.html rewritten")

# ---------------------------------------------------------------
# 3. home.js — typewriter + counters
# ---------------------------------------------------------------
HOME_JS = r'''/* home.js — typewriter + animated counters. No deps. */
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
'''

(ROOT / "home.js").write_text(HOME_JS, encoding="utf-8")
print("✓ home.js created")

# ---------------------------------------------------------------
# 4. CSS additions
# ---------------------------------------------------------------
CSS_ADD = r'''

/* ============ HERO TYPEWRITER ============ */
.hero-name {
  font-family: "JetBrains Mono", "Fira Code", Consolas, monospace;
  letter-spacing: -1.5px;
}
.hero-name .cursor {
  display: inline-block;
  margin-left: 4px;
  color: var(--accent-hi);
  animation: blink 1.1s step-end infinite;
  font-weight: 400;
}
@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

/* ============ ANIMATED COUNTERS ============ */
.counter-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin: 24px 0 0;
}
@media (min-width: 720px) {
  .counter-grid { grid-template-columns: repeat(4, 1fr); }
}
.counter {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
  padding: 20px 22px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius, 10px);
  text-decoration: none !important;
  color: var(--fg);
  transition: border-color 0.15s, transform 0.15s;
}
.counter:hover {
  border-color: var(--accent);
  transform: translateY(-2px);
}
.counter-num {
  font-size: clamp(2em, 4vw, 2.8em);
  font-weight: 900;
  line-height: 1;
  color: var(--accent-hi);
  font-family: "JetBrains Mono", "Fira Code", Consolas, monospace;
}
.counter-label {
  font-size: 0.8em;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: var(--fg-muted);
}

/* ============ NUMBERS BAND ============ */
.numbers-band {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  padding: 28px 24px;
  background: var(--accent-soft);
  border: 2px solid var(--accent);
  border-radius: var(--radius, 10px);
  text-align: center;
}
@media (min-width: 720px) {
  .numbers-band { grid-template-columns: repeat(4, 1fr); }
}
.numbers-band strong {
  display: block;
  font-size: 2em;
  font-weight: 900;
  color: var(--accent-hi);
  line-height: 1;
  margin-bottom: 6px;
  font-family: "JetBrains Mono", "Fira Code", Consolas, monospace;
}
.numbers-band span {
  font-size: 0.85em;
  color: var(--fg-muted);
  font-weight: 600;
}

/* ============ REDUCED MOTION ============ */
@media (prefers-reduced-motion: reduce) {
  .hero-name .cursor { animation: none; opacity: 1; }
}
'''

css = ROOT / "style.css"
if css.exists():
    src = css.read_text(encoding="utf-8")
    if "HERO TYPEWRITER" not in src:
        css.write_text(src + CSS_ADD, encoding="utf-8")
        print("✓ style.css appended")
    else:
        print("· style.css already has additions")

print("\ndone. Preview with: python3 -m http.server 8000")
