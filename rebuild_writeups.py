#!/usr/bin/env python3
"""
rebuild_writeups.py
Regenerate writeups/*.html from the .md sources, wrapped in the
somas3ccybersecurity header/footer, with the flag blurred until the
reader scrolls enough.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
WDIR = ROOT / "writeups"

# ---- Markdown -> HTML (minimal, no deps) ----
def md_to_html(md: str) -> str:
    """Very small Markdown renderer: headings, code fences (~~~ and ```),
    paragraphs, bold, inline code, blockquotes, bullet lists, hr, links."""
    lines = md.splitlines()
    out = []
    in_code = False
    code_buf = []
    in_list = False
    in_quote = False
    para = []

    def flush_para():
        if para:
            text = " ".join(para).strip()
            if text:
                text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
                text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
                text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
                out.append("<p>" + text + "</p>")
            para.clear()

    def flush_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    def flush_quote():
        nonlocal in_quote
        if in_quote:
            out.append("</blockquote>")
            in_quote = False

    for raw in lines:
        line = raw.rstrip()
        # Code fence start/end
        if line.startswith("~~~") or line.startswith("```"):
            if not in_code:
                flush_para(); flush_list(); flush_quote()
                in_code = True; code_buf = []
                lang = line[3:].strip()
            else:
                body = "\n".join(code_buf)
                out.append('<pre><code>' + _esc(body) + "</code></pre>")
                in_code = False
            continue
        if in_code:
            code_buf.append(line); continue

        if not line.strip():
            flush_para(); flush_list(); flush_quote(); continue

        # Headings
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            flush_para(); flush_list(); flush_quote()
            level = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (level, _inline(m.group(2)), level))
            continue

        # Horizontal rule
        if re.match(r"^-{3,}\s*$", line) or re.match(r"^\*{3,}\s*$", line):
            flush_para(); flush_list(); flush_quote()
            out.append("<hr>")
            continue

        # Blockquote
        if line.startswith(">"):
            flush_para(); flush_list()
            if not in_quote:
                out.append("<blockquote>"); in_quote = True
            out.append("<p>" + _inline(line.lstrip("> ").strip()) + "</p>")
            continue
        else:
            flush_quote()

        # List
        if re.match(r"^\s*[-*]\s+", line):
            flush_para()
            if not in_list:
                out.append("<ul>"); in_list = True
            item = re.sub(r"^\s*[-*]\s+", "", line)
            out.append("<li>" + _inline(item) + "</li>")
            continue
        else:
            flush_list()

        # Indented code block (4 spaces)
        if line.startswith("    "):
            flush_para()
            out.append("<pre><code>" + _esc(line[4:]) + "</code></pre>")
            continue

        para.append(line)

    flush_para(); flush_list(); flush_quote()
    if in_code:
        out.append('<pre><code>' + _esc("\n".join(code_buf)) + "</code></pre>")
    return "\n".join(out)

def _esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def _inline(s):
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    return s

# ---- Wrap Markdown-derived body in the site shell ----
PAGE_HEAD = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — somas3ccybersecurity</title>
<link rel="stylesheet" href="../style.css">
<script>
(function(){{try{{var t=localStorage.getItem("theme");if(!t)t=window.matchMedia&&window.matchMedia("(prefers-color-scheme: light)").matches?"light":"dark";document.documentElement.setAttribute("data-theme",t);}}catch(e){{}}}})();
</script>
<style>
.flag-gate{{display:inline-block;filter:blur(6px);transition:filter .4s ease;
  cursor:pointer;user-select:none;background:var(--bg-alt,#141414);color:var(--fg,#f5f5f5);
  padding:4px 10px;border-radius:4px;border:1px solid var(--border,#242424)}}
.flag-gate.unlocked{{filter:none;background:var(--accent-soft,#2a0808);color:var(--accent-hi,#ff3344)}}
.flag-banner{{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);
  background:var(--bg-card,#171717);color:var(--fg,#f5f5f5);border:1px solid var(--accent,#e11d2e);
  border-radius:999px;padding:10px 20px;font-size:13px;font-weight:700;
  box-shadow:0 4px 24px rgba(0,0,0,.5);z-index:500;display:flex;gap:12px;align-items:center;
  font-family:"Inter",system-ui,sans-serif}}
.flag-banner button{{background:var(--accent,#e11d2e);color:#fff;border:none;border-radius:999px;
  padding:4px 12px;font-size:12px;font-weight:700;cursor:pointer;font-family:inherit}}
.flag-banner button:hover{{background:var(--accent-hi,#ff3344)}}
@media (prefers-reduced-motion:reduce){{.flag-gate{{transition:none}}}}
</style>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="nav-inner">
    <a class="brand" href="../index.html">somas3c<span>c</span>ybersecurity</a>
    <nav aria-label="Main navigation"><ul class="nav-links">
      <li><a href="../index.html">Home</a></li><li><a href="../about.html">About</a></li><li><a href="../skills.html">Skills</a></li>
      <li><a href="../writeups.html">Writeups</a></li><li><a href="../labs.html">Labs</a></li><li><a href="../projects.html">Projects</a></li>
      <li><a href="../roadmap.html">Roadmap</a></li><li><a href="../cv.html">CV</a></li><li><a href="../contact.html">Contact</a></li>
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
<main id="main">
<p style="margin-bottom: 20px;"><a href="../writeups.html">← Back to all writeups</a></p>
<article class="writeup-body">
"""

PAGE_TAIL = """
</article>
</main>
<footer class="site-footer">
  <div class="footer-inner">
    <div><h4>somas3ccybersecurity</h4><p class="muted" style="font-size: 0.9em; margin: 0;">Cybersecurity analyst · Red team specialist · Cisco instructor.</p></div>
    <div><h4>Explore</h4><ul><li><a href="../writeups.html">Writeups</a></li><li><a href="../labs.html">Labs</a></li><li><a href="../projects.html">Projects</a></li><li><a href="../roadmap.html">Roadmap</a></li></ul></div>
    <div><h4>Connect</h4><ul><li><a href="mailto:miltonsilas564@gmail.com">Email</a></li><li><a href="https://github.com/Milton511" target="_blank" rel="noopener">GitHub</a></li><li><a href="../hire.html">Hire me</a></li></ul></div>
  </div>
  <div class="footer-bottom"><span>© 2026 somas3ccybersecurity · Built on GitHub Pages</span><span><a href="https://github.com/Milton511/milton511.github.io" target="_blank" rel="noopener">Source</a></span></div>
</footer>
<script src="../main.js"></script>
<script>
(function(){
  "use strict";
  var SEL=".flag-gate", WAIT_MS=3*60*1000, SCROLL_RATIO=0.6;
  var startedAt=Date.now(), scrolledEnough=false, unlocked=false;
  function article(){return document.querySelector(".writeup-body")||document.body;}
  function onScroll(){
    var a=article(),r=a.getBoundingClientRect();
    var visible=Math.max(0,Math.min(a.offsetHeight,window.innerHeight-r.top));
    if(visible/a.offsetHeight>=SCROLL_RATIO)scrolledEnough=true;
    maybeUnlock();
  }
  function maybeUnlock(force){
    if(unlocked)return;
    if(force||(Date.now()-startedAt>=WAIT_MS&&scrolledEnough)){
      unlocked=true;
      document.querySelectorAll(SEL).forEach(function(e){e.classList.add("unlocked");});
      var b=document.getElementById("flag-banner");if(b)b.remove();
    }
  }
  function tick(){
    if(unlocked)return;
    var left=Math.max(0,Math.ceil((WAIT_MS-(Date.now()-startedAt))/1000));
    var m=Math.floor(left/60),s=("0"+(left%60)).slice(-2);
    var el=document.getElementById("flag-countdown");
    if(el)el.textContent=(scrolledEnough?"unlock in ":"keep reading — ")+m+":"+s;
    setTimeout(tick,500);
  }
  document.addEventListener("DOMContentLoaded",function(){
    if(!document.querySelector(SEL))return;
    var b=document.createElement("div");
    b.id="flag-banner";b.className="flag-banner";
    b.innerHTML='<span>🔒 Flag locked — <span id="flag-countdown">3:00</span></span>'+
                '<button type="button" id="flag-skip">Reveal now</button>';
    document.body.appendChild(b);
    document.getElementById("flag-skip").onclick=function(){maybeUnlock(true);};
    document.querySelectorAll(SEL).forEach(function(e){
      e.onclick=function(){maybeUnlock(true);};
      e.title="Click to reveal";
    });
    window.addEventListener("scroll",onScroll,{passive:true});
    tick();
  });
})();
</script>
</body>
</html>
"""

def wrap_flag(html):
    # wrap the first r00t{...} occurrence anywhere in the rendered body
    m = re.search(r"(r00t\{[a-zA-Z0-9_\-]+\})", html)
    if not m:
        return html, None
    flag = m.group(1)
    wrapped = '<span class="flag-gate" data-flag="%s">%s</span>' % (flag, flag)
    return html[:m.start()] + wrapped + html[m.end():], flag

def rebuild_one(md_path):
    md = md_path.read_text(encoding="utf-8")
    # Title: first H1
    m = re.search(r"^#\s+(.+)$", md, re.M)
    title = m.group(1).strip() if m else md_path.stem
    body_html = md_to_html(md)
    body_html, flag = wrap_flag(body_html)
    page = PAGE_HEAD.format(title=title) + body_html + PAGE_TAIL
    out = md_path.with_suffix(".html")
    out.write_text(page, encoding="utf-8")
    return out.name, flag

if __name__ == "__main__":
    mds = sorted(WDIR.glob("*.md"))
    if not mds:
        print("!! no .md files in", WDIR); sys.exit(1)
    for md in mds:
        name, flag = rebuild_one(md)
        print(" -", name, "->", "flag=" + flag if flag else "NO FLAG FOUND (md)")
    print("done")
