#!/usr/bin/env python3
"""
apply_flag_hide.py  (v2)
- Masks the flag on writeups.html cards.
- Injects a blur-gate + countdown + "Reveal now" into every writeups/*.html.
- Works with Pandoc's syntax-highlighted HTML (strips tags to find the flag,
  then edits only the visible text node).
"""
import re
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
INDEX = ROOT / "writeups.html"
WDIR = ROOT / "writeups"

# -------- 1. writeups.html: mask the flag in the JS card builder --------
def patch_index():
    if not INDEX.exists():
        print("!! writeups.html not found"); return
    src = INDEX.read_text(encoding="utf-8")
    old = 'meta.textContent = "Flag: " + w.flag;'
    new = (
        'meta.innerHTML = "Flag: <span class=\\"flag-hidden\\" '
        'data-flag=\\"" + w.flag.replace(/"/g,"&quot;") + "\\">"'
        ' + "•".repeat(12) + "</span>";'
    )
    if old in src:
        src = src.replace(old, new)
        INDEX.write_text(src, encoding="utf-8")
        print("✓ writeups.html: masked flag in card grid")
    elif "flag-hidden" in src:
        print("· writeups.html already patched")
    else:
        print("!! writeups.html: could not find flag line. First 200 chars of the builder:")
        m = re.search(r'function card\(w\) \{[\s\S]{0,400}', src)
        print(m.group(0) if m else "  (no match)")
        sys.exit(1)

# -------- 2. inject CSS + JS into each writeup page --------
GATE_CSS = """<style id="flag-gate-css">
.flag-gate{display:inline-block;filter:blur(6px);transition:filter .4s ease;
  cursor:pointer;user-select:none;background:var(--bg-alt,#141414);color:var(--fg,#f5f5f5);
  padding:4px 10px;border-radius:4px;border:1px solid var(--border,#242424)}
.flag-gate.unlocked{filter:none;background:var(--accent-soft,#2a0808);color:var(--accent-hi,#ff3344)}
.flag-banner{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);
  background:var(--bg-card,#171717);color:var(--fg,#f5f5f5);border:1px solid var(--accent,#e11d2e);
  border-radius:999px;padding:10px 20px;font-size:13px;font-weight:700;
  box-shadow:0 4px 24px rgba(0,0,0,.5);z-index:500;display:flex;gap:12px;align-items:center;
  font-family:"Inter",system-ui,sans-serif}
.flag-banner button{background:var(--accent,#e11d2e);color:#fff;border:none;border-radius:999px;
  padding:4px 12px;font-size:12px;font-weight:700;cursor:pointer;font-family:inherit}
.flag-banner button:hover{background:var(--accent-hi,#ff3344)}
@media (prefers-reduced-motion:reduce){.flag-gate{transition:none}}
</style>"""

GATE_JS = """<script id="flag-gate-js">
(function(){
  "use strict";
  var SEL=".flag-gate", WAIT_MS=3*60*1000, SCROLL_RATIO=0.6;
  var startedAt=Date.now(), scrolledEnough=false, unlocked=false;
  function article(){return document.querySelector(".writeup-body, article, main")||document.body;}
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
</script>"""

def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)

def find_flag_in_dom(src):
    """
    Return (start, end) index in src of the first r00t{...} occurrence,
    tolerant of tags between characters (Pandoc highlighting).
    Strategy: build a stripped copy, find the flag there, then map back.
    """
    # Walk the source, tracking how many visible chars we've emitted, and
    # record where each visible char lives. Then find the flag in the
    # visible string and map the start/end back to source positions.
    visible = []
    index_map = []  # index_map[k] = source index of k-th visible char
    i = 0
    in_tag = False
    while i < len(src):
        c = src[i]
        if c == "<":
            in_tag = True
            i += 1
            continue
        if c == ">":
            in_tag = False
            i += 1
            continue
        if not in_tag:
            visible.append(c)
            index_map.append(i)
        i += 1

    vis = "".join(visible)
    m = re.search(r"r00t\{[a-zA-Z0-9_\-]+\}", vis)
    if not m:
        return None
    src_start = index_map[m.start()]
    src_end   = index_map[m.end()-1] + 1
    return (src_start, src_end, m.group(0))

def patch_one(path):
    src = path.read_text(encoding="utf-8")
    if 'id="flag-gate-js"' in src:
        return "already patched"
    found = find_flag_in_dom(src)
    if not found:
        # Debug: show what visible text contains near r00t
        visible = strip_tags(src)
        idx = visible.find("r00t")
        snippet = visible[max(0,idx-40):idx+80].replace("\n"," ") if idx != -1 else "(no 'r00t' at all)"
        return "no flag — visible text near r00t: " + snippet

    s, e, flag = found
    wrapped = '<span class="flag-gate" data-flag="%s">%s</span>' % (flag, src[s:e])
    src = src[:s] + wrapped + src[e:]

    if "</head>" in src:
        src = src.replace("</head>", GATE_CSS + "\n</head>", 1)
    if "</body>" in src:
        src = src.replace("</body>", GATE_JS + "\n</body>", 1)

    path.write_text(src, encoding="utf-8")
    return "patched flag=" + flag

def patch_writeups():
    if not WDIR.exists():
        print("!! writeups/ not found"); return
    for f in sorted(WDIR.glob("*.html")):
        print(" -", f.name, "->", patch_one(f))

if __name__ == "__main__":
    print("== patching writeups.html ==")
    patch_index()
    print("== patching writeups/*.html ==")
    patch_writeups()
    print("done")
