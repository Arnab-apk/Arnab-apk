"""
Build a neofetch-style info card SVG (Andrew6rant style) to sit to the RIGHT of
the ASCII portrait: colored key/value rows for work experience, tech stack, and
highlights -- NOT GitHub stats (the contribution graph covers those).

Static content, hand-authored below. Lines fade/slide in on a short stagger so
it feels like the panel is printing alongside the portrait. STATIC=1 emits the
frozen state for Quick Look previews.
"""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "info-card.svg")
STATIC = bool(os.environ.get("STATIC"))

W, H = 490, 480
PAD = 20
TITLEBAR_H = 30
KEY_X = PAD
VAL_X = PAD + 95
LINE_H = 19.5

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
INK = "#c9d1d9"
KEY = "#ffa657"      # orange keys
SECTION = "#58a6ff"  # blue section headers
GREEN = "#3fb950"
ACCENT = "#22d3ee"

# ===========================================================================
# Configuration for Arnab Mandal
# ===========================================================================
HOST = "arnab"   # shown as  arnab@github  in the header

ROWS = [
    ("host",),
    ("kv", "Name", "Arnab Mandal (Mr.Invictus)"),
    ("kv", "Role", "AI Engineer & Full Stack Dev"),
    ("kv", "Edu", "B.Tech CSE @ AOT, Kolkata"),
    ("kv", "Loc", "Kolkata, WB, India"),
    ("kv", "Site", "github.com/Arnab-apk"),
    ("gap",),
    ("sec", "Core Stack"),
    ("kv", "AI & ML", "Python, PyTorch, LangGraph, Ollama"),
    ("kv", "Web Dev", "Next.js, React, TypeScript, FastAPI"),
    ("kv", "Mobile", "Flutter, Dart, Kotlin, Android"),
    ("kv", "Storage", "PostgreSQL, MongoDB, Pinecone, FAISS"),
    ("gap",),
    ("sec", "Featured Projects"),
    ("bul", "Uma (Pujo Parikrama): Live GPS navigation & sync"),
    ("bul", "Roomi: Real-time shared music queue & voting"),
    ("bul", "Chimera-CLI: AI Docker config generator"),
    ("bul", "Code_CollabV2: Real-time CRDT code editor"),
]


def esc(s):
    return html.escape(s)


def rise(inner, i):
    """fade + slight upward slide, staggered by row index; freezes visible."""
    if STATIC:
        return f"<g>{inner}</g>"
    delay = 0.15 + i * 0.05
    return (f'<g opacity="0" transform="translate(0,5)">{inner}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.32s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0,5" to="0,0" '
            f'begin="{delay:.2f}s" dur="0.32s" fill="freeze"/></g>')


def main():
    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">'
    )
    parts.append(
        '<defs>'
        f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
        f'</linearGradient></defs>'
    )
    parts.append(f'<rect width="{W}" height="{H}" rx="12" fill="url(#bg)"/>')
    parts.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" '
                 f'stroke="{FRAME}" stroke-width="1"/>')

    # titlebar
    parts.append(f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>')
    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
    parts.append(
        f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" text-anchor="middle">'
        f'{esc(HOST)}@github: ~$ neofetch</text>'
    )

    # rows
    y = TITLEBAR_H + 24
    for i, r in enumerate(ROWS):
        kind = r[0]
        if kind == "gap":
            y += 6
            continue

        if kind == "host":
            content = (
                f'<text x="{PAD}" y="{y}" font-size="13" font-weight="700">'
                f'<tspan fill="{GREEN}">{esc(HOST)}</tspan>'
                f'<tspan fill="{MUTED}">@</tspan>'
                f'<tspan fill="{ACCENT}">github</tspan></text>'
                f'<line x1="{PAD}" y1="{y+5}" x2="{W-PAD}" y2="{y+5}" stroke="{FRAME}"/>'
            )
            parts.append(rise(content, i))
            y += LINE_H + 1
            continue

        if kind == "sec":
            title = esc(r[1])
            content = (
                f'<text x="{PAD}" y="{y}" fill="{SECTION}" font-size="11" font-weight="700" '
                f'letter-spacing="1">-- {title.upper()} {"-" * max(1, 28 - len(title))}</text>'
            )
            parts.append(rise(content, i))
            y += LINE_H
            continue

        if kind == "kv":
            k, v = esc(r[1]), esc(r[2])
            content = (
                f'<text x="{KEY_X}" y="{y}" fill="{KEY}" font-size="12" font-weight="600">{k}</text>'
                f'<text x="{VAL_X}" y="{y}" fill="{INK}" font-size="12">{v}</text>'
            )
            parts.append(rise(content, i))
            y += LINE_H
            continue

        if kind == "bul":
            txt = esc(r[1])
            content = (
                f'<text x="{KEY_X}" y="{y}" fill="{GREEN}" font-size="12">*</text>'
                f'<text x="{KEY_X + 16}" y="{y}" fill="{INK}" font-size="12">{txt}</text>'
            )
            parts.append(rise(content, i))
            y += LINE_H
            continue

    parts.append("</svg>")
    svg = "".join(parts)

    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote {OUT} ({len(svg)} bytes, {W}x{H})")


if __name__ == "__main__":
    main()