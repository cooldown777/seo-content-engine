#!/usr/bin/env python3
"""Carousel renderer: python3 render.py queue/<date>/deck.json -> queue/<date>/slides/NN_type.png + .jpg
All y values are CAP-TOPS @1080x1440 (per Carousel Blueprint); JS converts them to CSS top."""
import json, sys, pathlib, html
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = pathlib.Path(__file__).parent.resolve()
W, H = 1080, 1440

def css(accent):
    f = (ROOT / "fonts").as_uri()
    return f"""
@font-face{{font-family:Archivo;font-weight:400;src:url({f}/archivo-latin-400-normal.woff2)}}
@font-face{{font-family:Archivo;font-weight:500;src:url({f}/archivo-latin-500-normal.woff2)}}
@font-face{{font-family:Archivo;font-weight:700;src:url({f}/archivo-latin-700-normal.woff2)}}
@font-face{{font-family:Archivo;font-weight:800;src:url({f}/archivo-latin-800-normal.woff2)}}
@font-face{{font-family:Inter;font-weight:400;src:url({f}/inter-latin-400-normal.woff2)}}
@font-face{{font-family:JBM;font-weight:800;src:url({f}/jetbrains-mono-latin-800-normal.woff2)}}
:root{{--bg-dark:#0E0E0C;--ink-dark:#F4F2EE;--muted-dark:#8A8C86;--rule-dark:#2A2C26;--ghost:#30312C;--accent:{accent}}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;overflow:hidden}}
.slide{{position:relative;width:{W}px;height:{H}px;background:var(--bg-dark);color:var(--ink-dark);font-family:Archivo}}
.t{{position:absolute;white-space:nowrap}}
.wrap{{white-space:normal}}
.rule{{position:absolute;height:2px;background:var(--rule-dark)}}
.mono{{font-family:JBM;font-weight:800;letter-spacing:.17em;font-size:32px;line-height:1.3}}
.eyebrow{{font-weight:500;font-size:33px;letter-spacing:.12em;color:var(--muted-dark);line-height:1}}
.body{{font-family:Inter;font-weight:400;font-size:36px;line-height:1.39}}
.foot{{font-weight:700;font-size:22px;line-height:1;letter-spacing:.06em}}
.acc{{color:var(--accent)}}
"""

def T(y, x, cls, inner, style="", right=False, width=None):
    pos = f"right:{x}px;" if right else f"left:{x}px;"
    w = f"width:{width}px;" if width else ""
    return f'<div class="t {cls}" data-cap="{y}" style="{pos}{w}{style}">{inner}</div>'

def footer(b, M, line_y, text_y, last=False):
    right = "" if last else T(text_y, M, "foot", "Swipe →", right=True)
    return (f'<div class="rule" style="left:{M}px;right:{M}px;top:{line_y}px"></div>'
            + T(text_y, M, "foot", html.escape(b["handle"]), "color:var(--muted-dark)") + right)

def checkHook(s, b):
    M = 70
    return (T(304, M, "mono acc", "<br>".join(s["eyebrow"]))
            + T(437, M, "", s["title"], "font-weight:700;font-size:100px;line-height:1.12")
            + T(1108, M, "wrap acc", s["accentLine"], "font-weight:700;font-size:44px;line-height:1.2", width=W-2*M)
            + footer(b, M, 1311, 1345))

def checkItem(s, b):
    M = 70
    n = f'{s["n"]:02d}'
    return (T(190, M, "", n, "font-family:JBM;font-weight:800;font-size:150px;line-height:1;color:var(--ghost)", right=True)
            + T(226, M, "mono", f'CHECK {n} OF {s["total"]:02d}', "font-size:31px")
            + T(295, M, "", f'{s["title"]}<br><span class="acc">{s["titleAccent"]}</span>',
                "font-weight:700;font-size:79px;line-height:1.14")
            + f'<div class="rule" style="left:{M}px;right:{M}px;top:553px"></div>'
            + T(588, M, "wrap body", s["body"], width=W-2*M)
            + T(787, M, "mono acc", "ACTION", "font-size:31px")
            + T(840, M, "wrap body", s["action"], width=W-2*M)
            + T(1015, M, "mono", "EXAMPLE", "font-size:31px;color:var(--muted-dark)")
            + T(1068, M, "wrap body", s["example"], "color:var(--muted-dark)", width=W-2*M)
            + footer(b, M, 1311, 1345))

def checkSummary(s, b):
    M = 70
    rows = ""
    y0, step = 600, 100
    for i, it in enumerate(s["items"]):
        y = y0 + i * step
        rows += T(y, M, "mono", f"{i+1:02d}", "font-size:31px;color:var(--muted-dark)")
        rows += T(y - 2, M + 100, "", it, "font-weight:700;font-size:40px;line-height:1")
        if i < len(s["items"]) - 1:
            rows += f'<div class="rule" style="left:{M}px;right:{M}px;top:{y + 66}px;height:1.5px"></div>'
    return (T(200, M, "eyebrow", s["eyebrow"])
            + T(277, M, "", f'{s["title"]}<br><span class="acc">{s["titleAccent"]}</span>',
                "font-weight:700;font-size:79px;line-height:1.14")
            + f'<div class="rule" style="left:{M}px;right:{M}px;top:500px"></div>'
            + rows
            + T(1230, M, "wrap body", s["seed"], "color:var(--muted-dark);font-size:34px", width=W-2*M)
            + footer(b, M, 1311, 1345))

def darkCTA(s, b):
    M = 72
    h = html.escape(b["handle"])
    return (T(192, M, "eyebrow", s["eyebrow"])
            + T(247, M, "", "Comment this word", "font-weight:700;font-size:70px;line-height:1")
            + '<div style="position:absolute;left:0;right:0;top:350px;height:230px;background:var(--accent)"></div>'
            + T(393, M - 6, "", html.escape(s["keyword"]),
                "font-weight:800;font-size:170px;letter-spacing:-.02em;line-height:1;color:var(--bg-dark)")
            + T(640, M, "wrap", s["body"], "font-weight:400;font-size:40px;line-height:1.35", width=W-2*M)
            + f'<div class="rule" style="left:{M}px;right:{M}px;top:889px"></div>'
            + T(924, M, "eyebrow", "AND")
            + T(977, M, "", f'Follow <span class="acc">{h}</span>', "font-weight:800;font-size:63px;line-height:1")
            + T(1063, M, "wrap", s["sub"], "font-weight:400;font-size:36px;line-height:1.35;color:var(--muted-dark)", width=W-2*M)
            + f'<div class="rule" style="left:{M}px;right:{M}px;top:1199px"></div>'
            + T(1230, M, "foot", html.escape(b["series"]), "color:var(--muted-dark)")
            + T(1230, M, "foot", h, right=True))

TEMPLATES = {"checkHook": checkHook, "checkItem": checkItem, "checkSummary": checkSummary, "darkCTA": darkCTA}

# cap-top -> CSS top, using real font metrics of the first line
CAP_JS = """
() => { const c=document.createElement('canvas').getContext('2d');
  for (const el of document.querySelectorAll('[data-cap]')) {
    const cs=getComputedStyle(el); const size=parseFloat(cs.fontSize);
    const first = el.querySelector('span') && el.firstChild.nodeType!==3 ? el.firstChild : el;
    c.font = `${cs.fontWeight} ${size}px ${cs.fontFamily}`;
    const m=c.measureText('H'); const asc=m.fontBoundingBoxAscent, desc=m.fontBoundingBoxDescent;
    let lh = cs.lineHeight==='normal' ? (asc+desc) : parseFloat(cs.lineHeight);
    const baseline=(lh-(asc+desc))/2+asc; const cap=m.actualBoundingBoxAscent;
    el.style.top = (parseFloat(el.dataset.cap) - (baseline-cap)) + 'px';
  } }
"""

def main(deck_path, out_dir=None):
    deck_path = pathlib.Path(deck_path).resolve()
    deck = json.loads(deck_path.read_text(encoding="utf-8"))
    cfg = ROOT / "config.json"
    b = {**(json.loads(cfg.read_text())["brand"] if cfg.exists() else {}), **deck.get("brand", {})}
    out = pathlib.Path(out_dir).resolve() if out_dir else deck_path.parent / "slides"
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width": W, "height": H})
        for i, s in enumerate(deck["slides"], 1):
            doc = f'<html><head><meta charset="utf-8"><style>{css(b.get("accent", "#C8F034"))}</style></head><body><div class="slide">{TEMPLATES[s["type"]](s, b)}</div></body></html>'
            tmp = out / "_tmp.html"; tmp.write_text(doc, encoding="utf-8")
            pg.goto(tmp.as_uri()); pg.evaluate("document.fonts.ready.then(()=>1)")
            pg.wait_for_timeout(150); pg.evaluate(CAP_JS)
            f = out / f"{i:02d}_{s['type']}.png"
            pg.screenshot(path=str(f), clip={"x": 0, "y": 0, "width": W, "height": H})
            Image.open(f).convert("RGB").save(f.with_suffix(".jpg"), quality=95)  # Instagram API needs JPEG
            print(f)
        (out / "_tmp.html").unlink()
        br.close()

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
