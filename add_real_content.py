#!/usr/bin/env python3
"""
add_real_content.py
- Rebuilds labs.html with the real labs: Inter-VLAN Routing, FUTURE_CS_01, CTF.
- Rebuilds projects.html with pentest-toolkit and SomaSec.
- Adds a Fullstack section to skills.html.
- Updates about.html with the "also building" line.
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent

HEADER = '''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="nav-inner">
    <a class="brand" href="index.html">somas3c<span>c</span>ybersecurity</a>
    <nav aria-label="Main navigation"><ul class="nav-links">
      <li><a href="index.html">Home</a></li><li><a href="about.html">About</a></li><li><a href="skills.html">Skills</a></li>
      <li><a href="writeups.html">Writeups</a></li><li><a href="labs.html">Labs</a></li><li><a href="projects.html">Projects</a></li>
      <li><a href="roadmap.html">Roadmap</a></li><li><a href="cv.html">CV</a></li><li><a href="contact.html">Contact</a></li>
    </ul></nav>
    <span class="nav-spacer"></span>
    <button class="kbd-hint" type="button" id="palette-trigger" aria-label="Open command palette">Search <kbd>Ctrl</kbd><kbd>K</kbd></button>
    <button class="theme-toggle" type="button" onclick="toggleTheme()" aria-label="Toggle light and dark theme">☀ Light</button>
  </div>
</header>
<div class="progress-bar" id="progress-bar" aria-hidden="true"></div>
<div id="ninja" aria-hidden="true">🥷</div>
<div class="palette-overlay" id="palette-overlay" role="dialog" aria-modal="true" aria-label="Command palette">
  <div class="palette">
    <input type="text" id="palette-input" placeholder="Jump to a page or writeup…" autocomplete="off" />
    <ul class="palette-list" id="palette-list"></ul>
    <div class="palette-footer"><span><kbd>↑</kbd><kbd>↓</kbd> navigate</span><span><kbd>↵</kbd> open</span><span><kbd>Esc</kbd> close</span></div>
  </div>
</div>
'''

FOOTER = '''
<footer class="site-footer">
  <div class="footer-inner">
    <div><h4>somas3ccybersecurity</h4><p class="muted" style="font-size: 0.9em; margin: 0;">Cybersecurity analyst · Red team specialist · Cisco instructor.</p></div>
    <div><h4>Explore</h4><ul><li><a href="writeups.html">Writeups</a></li><li><a href="labs.html">Labs</a></li><li><a href="projects.html">Projects</a></li><li><a href="roadmap.html">Roadmap</a></li></ul></div>
    <div><h4>Connect</h4><ul><li><a href="mailto:cyberwiseafrica@gmail.com">Email</a></li><li><a href="https://github.com/Milton511" target="_blank" rel="noopener">GitHub</a></li><li><a href="hire.html">Hire me</a></li></ul></div>
  </div>
  <div class="footer-bottom"><span>© 2026 somas3ccybersecurity · Built on GitHub Pages</span><span><a href="https://github.com/Milton511/milton511.github.io" target="_blank" rel="noopener">Source</a></span></div>
</footer>
'''

THEME_SCRIPT = '''<script>
(function(){try{var t=localStorage.getItem("theme");if(!t)t=window.matchMedia&&window.matchMedia("(prefers-color-scheme: light)").matches?"light":"dark";document.documentElement.setAttribute("data-theme",t);}catch(e){}})();
</script>
'''

def page(title, body):
    return f'''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — somas3ccybersecurity</title>
<link rel="stylesheet" href="style.css">
{THEME_SCRIPT}
</head>
<body>
{HEADER}
<main id="main">
{body}
</main>
{FOOTER}
<script src="main.js"></script>
</body>
</html>
'''

# ---------------------------------------------------------------
# LABS
# ---------------------------------------------------------------
labs_body = '''
<section class="reveal">
  <p style="color: var(--accent-hi); font-weight: 800; letter-spacing: 3px; font-size: 0.8em; margin: 0 0 12px;">HANDS-ON</p>
  <h1>Labs &amp; Workshops</h1>
  <p class="muted" style="font-size: 1.05em; max-width: 720px;">Hands-on labs and training I've designed and delivered. These are the projects where I take beginners from "I read about it" to "I did it."</p>
</section>
<hr class="divider">

<section class="reveal">
  <h2>Networking labs</h2>
  <div class="grid grid-2">
    <div class="card" style="border-color: var(--accent);">
      <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px;">
        <span class="badge">CCNP</span>
        <span class="badge badge-muted">Packet Tracer</span>
        <span class="badge badge-muted">Verified</span>
      </div>
      <h3 style="margin-top: 0;">Enterprise Multi-VLAN Network</h3>
      <p class="muted" style="margin: 0 0 12px;">Production-ready network design for a 500+ employee enterprise. 5 VLANs (HR, Finance, Engineering, QA), 802.1Q trunking, SVI routing on a Layer 3 switch, Router-on-a-Stick at the branch, and a WAN serial link. Full verification with live ping tests and routing tables.</p>
      <p class="muted" style="font-size: 0.9em; margin: 0 0 12px;"><strong>Skills:</strong> VLAN creation · SVI · 802.1Q · Static routing · WAN · Cisco IOS CLI</p>
      <div style="display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 12px;"><span class="badge badge-muted">Cisco IOS-XE</span><span class="badge badge-muted">ISR4331</span><span class="badge badge-muted">3650-24PS</span></div>
      <div class="card-foot"><a href="https://github.com/Silasmil/inter-vlan-routing-lab" target="_blank" rel="noopener">View on GitHub →</a></div>
    </div>
    <div class="card">
      <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px;">
        <span class="badge">Cisco</span>
        <span class="badge badge-muted">Instructor</span>
      </div>
      <h3 style="margin-top: 0;">Cisco IT Essentials</h3>
      <p class="muted" style="margin: 0 0 12px;">Full course instruction covering hardware, OS, networking, and security fundamentals. Hands-on lab component built around real equipment and troubleshooting scenarios.</p>
      <p class="muted" style="font-size: 0.9em; margin: 0;"><strong>Audience:</strong> beginners to IT · <strong>Format:</strong> weekly, instructor-led</p>
    </div>
  </div>
</section>
<hr class="divider">

<section class="reveal">
  <h2>Internship &amp; CTF</h2>
  <div class="grid grid-2">
    <div class="card" style="border-color: var(--accent);">
      <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px;">
        <span class="badge">Future Interns</span>
        <span class="badge badge-muted">3 tasks completed</span>
      </div>
      <h3 style="margin-top: 0;">FUTURE_CS_01 — Cyber Security Internship</h3>
      <p class="muted" style="margin: 0 0 12px;">Three-task internship with a full portfolio per task:</p>
      <ul style="margin: 0 0 12px; padding-left: 20px; color: var(--fg-muted); font-size: 0.92em;">
        <li><strong>Task 1 — Vulnerability assessment:</strong> OWASP Juice Shop SQLi login bypass, Nmap scan, risk classification, remediation.</li>
        <li><strong>Task 2 — Phishing detection:</strong> analysed 4 email samples (3 phishing, 1 legit), detection checklist, prevention guidelines.</li>
        <li><strong>Task 3 — API security:</strong> SQLi to admin token, exposed /api/Users (22 records leaked), risk write-up.</li>
      </ul>
      <p class="muted" style="font-size: 0.9em; margin: 0 0 12px;"><strong>Eligibility:</strong> ✅ Certificate · ✅ Letter of recommendation</p>
      <div class="card-foot"><a href="https://github.com/Silasmil/FUTURE_CS_01" target="_blank" rel="noopener">View portfolio on GitHub →</a></div>
    </div>
    <div class="card">
      <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px;">
        <span class="badge">AfricaHackon</span>
        <span class="badge badge-muted">Participant</span>
      </div>
      <h3 style="margin-top: 0;">Perfect Root CTF</h3>
      <p class="muted" style="margin: 0 0 12px;">Solved 9 challenges across web, mobile, smart contract, crypto, and forensics. 🏆 First Blood on Echo Signature (ECDSA malleability). Every solve documented as a full writeup with defensive fixes.</p>
      <p class="muted" style="font-size: 0.9em; margin: 0;"><a href="writeups.html">See all 9 writeups →</a></p>
    </div>
  </div>
</section>
<hr class="divider">

<section class="reveal">
  <h2>Workshops in development</h2>
  <div class="grid grid-2">
    <div class="card">
      <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px;"><span class="badge">Workshop</span><span class="badge badge-muted">Coming soon</span></div>
      <h3 style="margin-top: 0;">Web Exploitation for Beginners</h3>
      <p class="muted" style="margin: 0 0 12px;">Hands-on lab where learners exploit SQLi, XSS, and SSTI on a deliberately vulnerable app — then fix each one and re-test. Emphasis on the fix, not just the exploit.</p>
      <p class="muted" style="font-size: 0.9em; margin: 0;">Want early access? <a href="contact.html">Get in touch</a>.</p>
    </div>
    <div class="card">
      <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px;"><span class="badge">Workshop</span><span class="badge badge-muted">Coming soon</span></div>
      <h3 style="margin-top: 0;">Mobile App Security Lab</h3>
      <p class="muted" style="margin: 0 0 12px;">Static analysis of an Android APK: apktool decompilation, smali reading, hardcoded secret recovery, root-check bypass, and re-implementation of the decryption logic in Python.</p>
      <p class="muted" style="font-size: 0.9em; margin: 0;"><a href="contact.html">Email me</a> to be notified.</p>
    </div>
  </div>
</section>
<hr class="divider">

<section class="reveal center">
  <div class="card" style="border-color: var(--accent);">
    <h2 style="border: none; padding-bottom: 0; margin-top: 0;">Want a lab for your team?</h2>
    <p class="muted" style="max-width: 560px; margin: 12px auto 24px;">I design and deliver hands-on security and networking training — remote or in-person.</p>
    <div style="display: flex; gap: 12px; flex-wrap: wrap; justify-content: center;">
      <a class="btn" href="hire.html">See services →</a>
      <a class="btn btn-ghost" href="contact.html">Contact</a>
    </div>
  </div>
</section>
'''

(ROOT / "labs.html").write_text(page("Labs & Workshops", labs_body), encoding="utf-8")
print("✓ labs.html rebuilt")

# ---------------------------------------------------------------
# PROJECTS
# ---------------------------------------------------------------
projects_body = '''
<section class="reveal">
  <p style="color: var(--accent-hi); font-weight: 800; letter-spacing: 3px; font-size: 0.8em; margin: 0 0 12px;">THINGS I'VE BUILT</p>
  <h1>Projects</h1>
  <p class="muted" style="font-size: 1.05em; max-width: 720px;">Tools and platforms I've built and shipped. All open source or documented, all in active use.</p>
</section>
<hr class="divider">

<section class="reveal">
  <h2>Shipped</h2>
  <div class="grid grid-2">
    <div class="card" style="border-color: var(--accent);">
      <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px;">
        <span class="badge">Released</span>
        <span class="badge badge-muted">v1.1</span>
        <span class="badge badge-muted">MIT</span>
      </div>
      <h3 style="margin-top: 0;">Pentest Toolkit</h3>
      <p class="muted" style="margin: 0 0 12px;">Modular Python-based ethical hacking toolkit for recon, port scanning, and web security header analysis. Self-updating from GitHub. Shipped as a release.</p>
      <div style="display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 12px;">
        <span class="badge badge-muted">Python</span>
        <span class="badge badge-muted">Shell</span>
        <span class="badge badge-muted">Conda</span>
      </div>
      <div class="card-foot"><a href="https://github.com/Silasmil/pentest-toolkit" target="_blank" rel="noopener">View on GitHub →</a></div>
    </div>
    <div class="card">
      <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px;">
        <span class="badge">Tool</span>
        <span class="badge badge-muted">Python</span>
      </div>
      <h3 style="margin-top: 0;">CTF Writeup Engine</h3>
      <p class="muted" style="margin: 0 0 12px;">Markdown-to-HTML pipeline that turns every CTF solve into a themed, indexed writeup. Powers all 9 Perfect Root writeups on this site.</p>
      <div style="display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 12px;">
        <span class="badge badge-muted">Python</span>
        <span class="badge badge-muted">Markdown</span>
      </div>
      <div class="card-foot"><a href="https://github.com/Milton511/milton511.github.io" target="_blank" rel="noopener">Source on GitHub →</a></div>
    </div>
    <div class="card">
      <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px;">
        <span class="badge">Site</span>
        <span class="badge badge-muted">Static</span>
      </div>
      <h3 style="margin-top: 0;">This Portfolio</h3>
      <p class="muted" style="margin: 0 0 12px;">Plain HTML + CSS + vanilla JS. No build step, no framework, no tracking. Deploys to GitHub Pages.</p>
      <div style="display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 12px;">
        <span class="badge badge-muted">HTML</span>
        <span class="badge badge-muted">CSS</span>
        <span class="badge badge-muted">JavaScript</span>
      </div>
      <div class="card-foot"><a href="https://github.com/Milton511/milton511.github.io" target="_blank" rel="noopener">Source on GitHub →</a></div>
    </div>
  </div>
</section>
<hr class="divider">

<section class="reveal">
  <h2>In development</h2>
  <div class="grid grid-2">
    <div class="card">
      <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px;">
        <span class="badge">Platform</span>
        <span class="badge badge-muted">Active dev</span>
        <span class="badge badge-muted">Private</span>
      </div>
      <h3 style="margin-top: 0;">SomaSec</h3>
      <p class="muted" style="margin: 0 0 12px;">Full-stack cybersecurity learning and creator platform. Flask backend, React frontend, PostgreSQL, Docker. Building the reading-history and auth layer now.</p>
      <div style="display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 12px;">
        <span class="badge badge-muted">Flask</span>
        <span class="badge badge-muted">React</span>
        <span class="badge badge-muted">TypeScript</span>
        <span class="badge badge-muted">PostgreSQL</span>
        <span class="badge badge-muted">Docker</span>
      </div>
      <p class="muted" style="font-size: 0.9em; margin: 0;"><strong>Private repo</strong> — ask if you want a walkthrough.</p>
    </div>
    <div class="card">
      <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 12px;">
        <span class="badge">Training</span>
        <span class="badge badge-muted">In development</span>
      </div>
      <h3 style="margin-top: 0;">Training Lab Materials</h3>
      <p class="muted" style="margin: 0 0 12px;">Lab exercises for Cisco IT Essentials and beginner security workshops. Includes vulnerable VMs, worksheets, and answer keys.</p>
      <p class="muted" style="font-size: 0.9em; margin: 0;"><strong>Available for licensed use</strong> — <a href="contact.html">contact me</a>.</p>
    </div>
  </div>
</section>
<hr class="divider">

<section class="reveal center">
  <div class="card" style="border-color: var(--accent);">
    <h2 style="border: none; padding-bottom: 0; margin-top: 0;">Need a tool built?</h2>
    <p class="muted" style="max-width: 560px; margin: 12px auto 24px;">Security automation, custom recon tooling, or a small platform — if it saves your team time, I'll scope and build it.</p>
    <div style="display: flex; gap: 12px; flex-wrap: wrap; justify-content: center;">
      <a class="btn" href="hire.html">See services →</a>
      <a class="btn btn-ghost" href="contact.html">Contact</a>
    </div>
  </div>
</section>
'''

(ROOT / "projects.html").write_text(page("Projects", projects_body), encoding="utf-8")
print("✓ projects.html rebuilt")

# ---------------------------------------------------------------
# SKILLS — add a Fullstack section if not there
# ---------------------------------------------------------------
skills_path = ROOT / "skills.html"
if skills_path.exists():
    src = skills_path.read_text(encoding="utf-8")
    if "Fullstack" not in src:
        block = '''
  <section class="reveal">
    <h2>Fullstack (in development)</h2>
    <div class="card">
      <div class="skill-row"><span class="name">Python / Flask</span><div class="skill-bar"><span data-level="80"></span></div></div>
      <div class="skill-row"><span class="name">React / TypeScript</span><div class="skill-bar"><span data-level="70"></span></div></div>
      <div class="skill-row"><span class="name">PostgreSQL</span><div class="skill-bar"><span data-level="65"></span></div></div>
      <div class="skill-row"><span class="name">Docker / docker-compose</span><div class="skill-bar"><span data-level="70"></span></div></div>
      <div class="skill-row"><span class="name">CI/CD (GitHub Actions)</span><div class="skill-bar"><span data-level="65"></span></div></div>
    </div>
  </section>
'''
        src = src.replace("</main>", block + "\n</main>", 1)
        skills_path.write_text(src, encoding="utf-8")
        print("✓ skills.html — added Fullstack section")
    else:
        print("· skills.html already has Fullstack")
else:
    print("!! skills.html not found")

# ---------------------------------------------------------------
# ABOUT — add the "also building" line if not there
# ---------------------------------------------------------------
about_path = ROOT / "about.html"
if about_path.exists():
    src = about_path.read_text(encoding="utf-8")
    if "SomaSec" not in src:
        block = '''
  <section class="reveal">
    <h2>Also building</h2>
    <div class="card">
      <p class="muted" style="margin: 0;">Outside of security work, I'm a fullstack developer in progress — currently building <strong>SomaSec</strong>, a cybersecurity learning platform (Flask + React + PostgreSQL + Docker). Not just consuming security tooling, but shipping my own. It sharpens the code-review and architecture side of pentesting, and it's the clearest way to prove I understand what developers face when they try to fix what I find.</p>
    </div>
  </section>
'''
        src = src.replace("</main>", block + "\n</main>", 1)
        about_path.write_text(src, encoding="utf-8")
        print("✓ about.html — added 'Also building' section")
    else:
        print("· about.html already mentions SomaSec")
else:
    print("!! about.html not found")

# ---------------------------------------------------------------
# CONTACT — add phone number (single place only)
# ---------------------------------------------------------------
contact_path = ROOT / "contact.html"
if contact_path.exists():
    src = contact_path.read_text(encoding="utf-8")
    if "0790480098" not in src:
        block = '''
  <section class="reveal">
    <h2>Direct line</h2>
    <div class="card">
      <p class="muted" style="margin: 0 0 8px;">If you'd rather call than email (business hours, EAT):</p>
      <p style="margin: 0; font-size: 1.1em; font-weight: 700;">
        <a href="tel:+254790480098">+254 790 480 098</a>
      </p>
      <p class="muted" style="margin: 8px 0 0; font-size: 0.9em;">Please use email first for project inquiries — faster for both of us.</p>
    </div>
  </section>
'''
        src = src.replace("</main>", block + "\n</main>", 1)
        contact_path.write_text(src, encoding="utf-8")
        print("✓ contact.html — added phone number")
    else:
        print("· contact.html already has phone")
else:
    print("!! contact.html not found")

print("\ndone. Preview with: python3 -m http.server 8000")
