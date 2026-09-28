#!/usr/bin/env python3
"""
Premium ASCII Portrait Generator - Creates a sophisticated animated ASCII portrait
with multiple animation layers: scanline reveal, character-by-character typing,
and subtle glow effects.
"""
import os
from pathlib import Path

# ─── Configuration ──────────────────────────────────────────────
WIDTH_CHARS = 80
HEIGHT_CHARS = 45
FONT_SIZE = 7.5
LINE_HEIGHT = 9.5
CHAR_WIDTH = 5.2
MARGIN = 24

CANVAS_W = MARGIN * 2 + WIDTH_CHARS * CHAR_WIDTH
CANVAS_H = MARGIN * 2 + HEIGHT_CHARS * LINE_HEIGHT + 40  # +40 for title bar

# ─── Color Palette (Premium Terminal Theme) ─────────────────────
BG_DEEP = "#080c14"
BG_CARD = "#0d131f"
BORDER = "#1e2a3a"
ACCENT_CYAN = "#00d4ff"
ACCENT_GREEN = "#00ff88"
ACCENT_GOLD = "#ffd700"
ACCENT_CORAL = "#ff6b6b"
TEXT_PRIMARY = "#e8edf3"
TEXT_SECONDARY = "#8899aa"
TEXT_MUTED = "#556677"
GLOW_CYAN = "rgba(0, 212, 255, 0.4)"
GLOW_GREEN = "rgba(0, 255, 136, 0.3)"

# ─── Portrait Art (High-contrast, clean lines) ──────────────────
PORTRAIT = [
    "                                                                            ",
    "        ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄        ",
    "       █                                            █       ",
    "       █   ███╗   ███╗ █████╗ ██████╗ ███████╗      █       ",
    "       █   ████╗ ████║██╔══██╗██╔══██╗██╔════╝      █       ",
    "       █   ██╔████╔██║███████║██████╔╝███████╗      █       ",
    "       █   ██║╚██╔╝██║██╔══██║██╔══██╗╚════██║      █       ",
    "       █   ██║ ╚═╝ ██║██║  ██║██║  ██║███████║      █       ",
    "       █   ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝      █       ",
    "       █                                            █       ",
    "       █   A R N A B   M A N D A L   •   @ M r . I n v i c t u s   █       ",
    "       █                                            █       ",
    "       ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀        ",
    "                                                                            ",
    "    ╔═══════════════════════════════════════════════════════════════════╗   ",
    "    ║  ████████████████████████████████████████████████████████████████  ║   ",
    "    ║  █  🧠  AI ENGINEER    █  💻  FULL STACK    █  📱  MOBILE DEV  █  ║   ",
    "    ║  █  🎮  UNITY AR       █  ☁️  CLOUD NATIVE   █  🔬  RESEARCH   █  ║   ",
    "    ║  ████████████████████████████████████████████████████████████████  ║   ",
    "    ╚═══════════════════════════════════════════════════════════════════╝   ",
    "                                                                            ",
    "    ┌────────────────────────────────────────────────────────────────┐   ",
    "    │  STACK  ████████████████████████████████████████████████  98%  │   ",
    "    │  Python ████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  92%  │   ",
    "    │  TypeScript ██████████████████████░░░░░░░░░░░░░░░░░░░░░░  88%  │   ",
    "    │  Go █████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░  82%  │   ",
    "    │  Kotlin ███████████████████████░░░░░░░░░░░░░░░░░░░░░░░  80%  │   ",
    "    │  C++ ████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░  75%  │   ",
    "    │  Dart ███████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░  78%  │   ",
    "    └────────────────────────────────────────────────────────────────┘   ",
    "                                                                            ",
    "    ╔═══════════════════════════════════════════════════════════════════╗   ",
    "    ║  ▶ B.Tech CSE  •  Academy of Technology, Kolkata  •  3rd Year    ║   ",
    "    ║  ▶ 21 years  •  Builder  •  Dreamer  •  Open Source Contributor  ║   ",
    "    ╚═══════════════════════════════════════════════════════════════════╝   ",
    "                                                                            ",
    "    ┌────────────────────────────────────────────────────────────────┐   ",
    "    │  🌐  github.com/Arnab-apk      💼  linkedin.com/in/arnab-mandal │   ",
    "    │  📧  arnabmandal.dev@gmail.com  🐦  @_mr.invictus__             │   ",
    "    └────────────────────────────────────────────────────────────────┘   ",
    "                                                                            ",
    "    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄",
    "    █  \"From concept to commit — elevating innovation.\"  █",
    "    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀",
]


def generate_premium_svg(static: bool = False) -> str:
    """Generate the premium animated ASCII portrait SVG."""

    if not static:
        css = f"""
  <style>
    @keyframes scanline {{
      0% {{ transform: translateY(-100%); opacity: 0; }}
      50% {{ opacity: 0.8; }}
      100% {{ transform: translateY(100%); opacity: 0; }}
    }}
    @keyframes typewriter {{
      from {{ width: 0; opacity: 0; }}
      to {{ width: 100%; opacity: 1; }}
    }}
    @keyframes fadeInUp {{
      from {{ opacity: 0; transform: translateY(8px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes pulseGlow {{
      0%, 100% {{ opacity: 0.3; }}
      50% {{ opacity: 0.8; }}
    }}
    @keyframes cursorBlink {{
      0%, 50% {{ opacity: 1; }}
      51%, 100% {{ opacity: 0; }}
    }}
    .portrait-line {{
      opacity: 0;
      animation: fadeInUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }}
    .scanline {{
      animation: scanline 3s linear infinite;
    }}
    .cursor {{
      animation: cursorBlink 1s step-end infinite;
      fill: {ACCENT_CYAN};
    }}
    .accent-cyan {{ fill: {ACCENT_CYAN}; }}
    .accent-green {{ fill: {ACCENT_GREEN}; }}
    .accent-gold {{ fill: {ACCENT_GOLD}; }}
    .accent-coral {{ fill: {ACCENT_CORAL}; }}
    .text-primary {{ fill: {TEXT_PRIMARY}; }}
    .text-secondary {{ fill: {TEXT_SECONDARY}; }}
    .text-muted {{ fill: {TEXT_MUTED}; }}
    .mono {{
      font-family: 'ui-monospace', 'SFMono-Regular', 'Menlo', 'Consolas', 'Monospace';
      font-size: {FONT_SIZE}px;
      line-height: {LINE_HEIGHT}px;
      white-space: pre;
    }}
    .title-bar {{
      opacity: 0;
      animation: fadeInUp 0.4s ease-out 0.1s forwards;
    }}
  </style>
"""
    else:
        css = f"""
  <style>
    .mono {{
      font-family: 'ui-monospace', 'SFMono-Regular', 'Menlo', 'Consolas', 'Monospace';
      font-size: {FONT_SIZE}px;
      line-height: {LINE_HEIGHT}px;
      white-space: pre;
      fill: {TEXT_PRIMARY};
    }}
    .accent-cyan {{ fill: {ACCENT_CYAN}; }}
    .accent-green {{ fill: {ACCENT_GREEN}; }}
    .accent-gold {{ fill: {ACCENT_GOLD}; }}
    .accent-coral {{ fill: {ACCENT_CORAL}; }}
    .text-secondary {{ fill: {TEXT_SECONDARY}; }}
    .text-muted {{ fill: {TEXT_MUTED}; }}
  </style>
"""

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" viewBox="0 0 {CANVAS_W} {CANVAS_H}" role="img" aria-label="Arnab Mandal - Premium ASCII Portrait">',
        css,
        # Deep background with subtle grid pattern
        f'<defs>',
        f'<pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">',
        f'<path d="M 20 0 L 0 0 0 20" fill="none" stroke="{BORDER}" stroke-width="0.3" opacity="0.3"/>',
        f'</pattern>',
        f'<linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="1">',
        f'<stop offset="0%" stop-color="{BG_DEEP}"/>',
        f'<stop offset="100%" stop-color="#05080e"/>',
        f'</linearGradient>',
        f'<filter id="glow" x="-50%" y="-50%" width="200%" height="200%">',
        f'<feGaussianBlur stdDeviation="3" result="coloredBlur"/>',
        f'<feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge>',
        f'</filter>',
        f'</defs>',
        f'<rect width="{CANVAS_W}" height="{CANVAS_H}" fill="url(#bgGrad)"/>',
        f'<rect width="{CANVAS_W}" height="{CANVAS_H}" fill="url(#grid)"/>',
        # Subtle vignette
        f'<rect width="{CANVAS_W}" height="{CANVAS_H}" fill="url(#vignette)"/>',
        # Title bar (terminal style)
        f'<rect x="0" y="0" width="{CANVAS_W}" height="36" fill="{BG_CARD}"/>',
        f'<line x1="0" y1="36" x2="{CANVAS_W}" y2="36" stroke="{BORDER}" stroke-width="1"/>',
        f'<circle cx="16" cy="18" r="6" fill="#ff5f56"/>',
        f'<circle cx="34" cy="18" r="6" fill="#ffbd2e"/>',
        f'<circle cx="52" cy="18" r="6" fill="#27c93f"/>',
        f'<text class="title-bar mono" x="{MARGIN}" y="24" font-size="12" font-weight="600" fill="{TEXT_SECONDARY}">arnab@github ~ $ cat premium_portrait.txt</text>',
        f'<text class="title-bar mono" x="{CANVAS_W - MARGIN}" y="24" text-anchor="end" font-size="11" fill="{TEXT_MUTED}">PREMIUM MODE • {WIDTH_CHARS}x{HEIGHT_CHARS}</text>',
    ]

    # Animated scanline overlay
    if not static:
        svg.append(
            f'<rect class="scanline" x="{MARGIN}" y="{MARGIN + 36}" width="{WIDTH_CHARS * CHAR_WIDTH}" height="4" '
            f'fill="{ACCENT_CYAN}" opacity="0" filter="url(#glow)"/>'
        )

    # Portrait lines with staggered animation
    y_start = MARGIN + 42
    for i, line in enumerate(PORTRAIT):
        if not line.strip():
            y_start += LINE_HEIGHT * 0.5
            continue

        delay = i * 0.035
        anim_attr = f'style="animation-delay: {delay:.3f}s"' if not static else ''

        # Determine styling based on content
        klass = "mono portrait-line"
        if "█" in line and "║" in line:
            klass += " accent-cyan"
        elif "████████" in line or "98%" in line or "92%" in line:
            klass += " accent-green"
        elif "▄" in line or "▀" in line:
            klass += " accent-gold"
        elif "╔" in line or "╚" in line or "═" in line:
            klass += " accent-cyan"
        elif "┌" in line or "└" in line or "│" in line:
            klass += " text-secondary"
        elif "@" in line or "github" in line or "linkedin" in line:
            klass += " accent-coral"

        # Escape XML
        escaped = line.replace("&", "&").replace("<", "<").replace(">", ">")

        svg.append(
            f'<text class="{klass}" x="{MARGIN}" y="{y_start}" {anim_attr}>{escaped}</text>'
        )
        y_start += LINE_HEIGHT

    # Blinking cursor at the end
    if not static:
        svg.append(
            f'<text class="mono cursor" x="{MARGIN}" y="{y_start - LINE_HEIGHT}">█</text>'
        )

    # Bottom status bar
    svg.append(
        f'<line x1="{MARGIN}" y1="{CANVAS_H - 28}" x2="{CANVAS_W - MARGIN}" y2="{CANVAS_H - 28}" stroke="{BORDER}" stroke-width="0.5"/>'
    )
    if not static:
        svg.append(
            f'<text class="mono" x="{MARGIN}" y="{CANVAS_H - 14}" font-size="10" fill="{TEXT_MUTED}">'
            f'<tspan class="accent-green">●</tspan> CONNECTED  '
            f'<tspan class="accent-cyan">⚡</tspan> ANIMATED  '
            f'<tspan class="accent-gold">◆</tspan> PREMIUM  '
            f'<tspan class="text-muted">|  Lines: {len(PORTRAIT)}  |  Chars: {WIDTH_CHARS}</tspan>'
            f'</text>'
        )
    else:
        svg.append(
            f'<text class="mono" x="{MARGIN}" y="{CANVAS_H - 14}" font-size="10" fill="{TEXT_MUTED}">'
            f'Lines: {len(PORTRAIT)}  |  Chars: {WIDTH_CHARS}'
            f'</text>'
        )

    svg.append("</svg>")
    return "\n".join(svg)


def main():
    static = os.environ.get("STATIC") == "1"
    svg = generate_premium_svg(static=static)
    output_path = Path("premium-ascii.svg")
    output_path.write_text(svg)
    print(f"✓ Generated {output_path} ({'static' if static else 'animated'}) — {len(svg)} bytes")


if __name__ == "__main__":
    main()