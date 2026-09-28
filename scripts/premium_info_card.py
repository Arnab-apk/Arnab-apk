#!/usr/bin/env python3
"""
Premium Neofetch-style Info Card - Sophisticated animated system info card
with layered animations, progress bars, and premium styling.
"""
import os
from pathlib import Path

# ─── Configuration ──────────────────────────────────────────────
CARD_W = 520
PADDING = 24
LINE_H = 22
TITLE_H = 40
SECTION_GAP = 14

# Colors - Premium Terminal Palette
BG = "#080c14"
BG_ELEVATED = "#0d131f"
BORDER = "#1e2a3a"
BORDER_GLOW = "#00d4ff"

ACCENT_CYAN = "#00d4ff"
ACCENT_GREEN = "#00ff88"
ACCENT_GOLD = "#ffd700"
ACCENT_CORAL = "#ff6b6b"
ACCENT_PURPLE = "#c084fc"
ACCENT_ORANGE = "#fb923c"

TEXT_PRIMARY = "#f0f4f9"
TEXT_SECONDARY = "#a0b0c0"
TEXT_MUTED = "#5a6a7a"
TEXT_DIM = "#3a4a5a"

# ─── Content Data ───────────────────────────────────────────────
INFO_DATA = {
    "user": "arnab",
    "host": "github",
    "os": "Arch Linux (btw) • Kernel 6.10+",
    "uptime": "21 years, 8 months, 12 days",
    "shell": "zsh • starship prompt",
    "editor": "Neovim • VS Code",
    "terminal": "Ghostty • Kitty",
    "wm": "Hyprland • Wayland",
    "": "",
    "title": "AI ENGINEER & FULL STACK DEVELOPER",
    "location": "Kolkata, WB, India",
    "education": "B.Tech CSE @ Academy of Technology",
    "focus": "GenAI • Agentic Systems • RAG • LLM Ops",
    "": " ",
    "skills": [
        ("AI/ML", "Python, PyTorch, LangGraph, LlamaIndex, Ollama, Gemini API", ACCENT_GREEN, 95),
        ("LLM Ops", "LangChain, LangGraph, RAG, Fine-tuning, Evaluation, Guardrails", ACCENT_CYAN, 90),
        ("Backend", "FastAPI, Node.js, Go, PostgreSQL, MongoDB, Redis, WebSockets", ACCENT_ORANGE, 88),
        ("Frontend", "Next.js 15, React 19, TypeScript, Tailwind, Framer Motion", ACCENT_CYAN, 92),
        ("Mobile", "Flutter, Dart, Kotlin, Android SDK, Jetpack Compose", ACCENT_PURPLE, 85),
        ("DevOps", "Docker, Kubernetes, GitHub Actions, Vercel, Firebase, Linux", ACCENT_GOLD, 82),
        ("Data", "Pinecone, Weaviate, FAISS, Vector DBs, Embeddings, SQL", ACCENT_CORAL, 80),
        ("Tools", "Neovim, Git, Docker, Postman, Figma, Obsidian, Raycast", TEXT_SECONDARY, 75),
    ],
    "projects": [
        ("Uma", "Pujo Parikrama", "330+ pandals • Live GPS • Group sync • Flutter + Firebase", "🌺", ACCENT_CORAL),
        ("Roomi", "Shared Music", "Real-time queue • Democratic voting • Next.js + Socket.io", "🎵", ACCENT_PURPLE),
        ("Chimera-CLI", "AI Docker Gen", "Multi-LLM • Auto-detect frameworks • Go + Bubble Tea", "🐉", ACCENT_GREEN),
        ("Code_CollabV2", "CRDT Editor", "Yjs • Monaco • Real-time cursors • React + FastAPI", "👨‍💻", ACCENT_CYAN),
        ("Model-StudyPlace", "3D Education", "Google Model Viewer • Gemini AI Tutor • Vanilla JS", "🧠", ACCENT_GOLD),
        ("CredVault", "Decentralized ID", "Merkle proofs • Solidity • Polygon • Next.js", "🔐", ACCENT_ORANGE),
    ],
    "stats": {
        "contributions": "2,847+",
        "repos": "47",
        "stars": "1.2k+",
        "followers": "380+",
        "streak": "12 days",
        "longest_streak": "45 days",
    },
    "links": [
        ("GitHub", "github.com/Arnab-apk", "https://github.com/Arnab-apk"),
        ("LinkedIn", "linkedin.com/in/arnab-mandal", "https://linkedin.com/in/arnab-mandal-00200131a"),
        ("Email", "arnabmandal.dev@gmail.com", "mailto:arnabmandal.dev@gmail.com"),
        ("LeetCode", "leetcode.com/u/6IDfCDzl1s", "https://leetcode.com/u/6IDfCDzl1s"),
    ]
}


def generate_card(static: bool = False) -> str:
    """Generate the premium animated info card SVG."""

    # Calculate height dynamically
    lines_count = (
        8 +  # header section
        1 +  # title
        4 +  # info rows
        1 +  # divider
        len(INFO_DATA["skills"]) +  # skills
        1 +  # divider
        len(INFO_DATA["projects"]) * 2 +  # projects (2 lines each)
        1 +  # divider
        2 +  # stats
        1 +  # divider
        len(INFO_DATA["links"]) +  # links
        2  # padding
    )
    CARD_H = TITLE_H + PADDING * 2 + lines_count * LINE_H + 20

    if not static:
        css = f"""
  <style>
    @keyframes slideIn {{
      from {{ opacity: 0; transform: translateX(-15px); }}
      to {{ opacity: 1; transform: translateX(0); }}
    }}
    @keyframes fadeIn {{
      from {{ opacity: 0; }}
      to {{ opacity: 1; }}
    }}
    @keyframes barGrow {{
      from {{ width: 0; }}
      to {{ width: var(--bar-width); }}
    }}
    @keyframes countUp {{
      from {{ opacity: 0; transform: scale(0.8); }}
      to {{ opacity: 1; transform: scale(1); }}
    }}
    @keyframes pulse {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0.5; }}
    }}
    .card-row {{
      opacity: 0;
      animation: slideIn 0.45s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }}
    .stat-value {{
      opacity: 0;
      animation: countUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }}
    .skill-bar-bg {{
      fill: {BG};
    }}
    .skill-bar-fill {{
      transform-origin: left center;
      transform: scaleX(0);
      animation: barGrow 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }}
    .title-bar {{
      opacity: 0;
      animation: fadeIn 0.3s ease-out 0.05s forwards;
    }}
    .divider {{
      opacity: 0;
      animation: fadeIn 0.3s ease-out forwards;
    }}
    .project-icon {{
      animation: pulse 2s ease-in-out infinite;
    }}
    .mono {{
      font-family: 'ui-monospace', 'SFMono-Regular', 'Menlo', 'Consolas', monospace;
    }}
    .interactive:hover {{
      cursor: pointer;
    }}
  </style>
"""
    else:
        css = f"""
  <style>
    .mono {{
      font-family: 'ui-monospace', 'SFMono-Regular', 'Menlo', 'Consolas', monospace;
    }}
  </style>
"""

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}" role="img" aria-label="Arnab Mandal - System Info">',
        css,
        # Defs for gradients and filters
        f'<defs>',
        f'<linearGradient id="cardBg" x1="0" y1="0" x2="0" y2="1">',
        f'<stop offset="0%" stop-color="{BG_ELEVATED}"/>',
        f'<stop offset="100%" stop-color="{BG}"/>',
        f'</linearGradient>',
        f'<linearGradient id="cyanGrad" x1="0" y1="0" x2="1" y2="0">',
        f'<stop offset="0%" stop-color="{ACCENT_CYAN}"/>',
        f'<stop offset="100%" stop-color="#0099cc"/>',
        f'</linearGradient>',
        f'<linearGradient id="greenGrad" x1="0" y1="0" x2="1" y2="0">',
        f'<stop offset="0%" stop-color="{ACCENT_GREEN}"/>',
        f'<stop offset="100%" stop-color="#00cc66"/>',
        f'</linearGradient>',
        f'<linearGradient id="goldGrad" x1="0" y1="0" x2="1" y2="0">',
        f'<stop offset="0%" stop-color="{ACCENT_GOLD}"/>',
        f'<stop offset="100%" stop-color="#ccaa00"/>',
        f'</linearGradient>',
        f'<filter id="cardGlow" x="-20%" y="-20%" width="140%" height="140%">',
        f'<feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="{ACCENT_CYAN}" flood-opacity="0.15"/>',
        f'</filter>',
        f'<filter id="textGlow" x="-50%" y="-50%" width="200%" height="200%">',
        f'<feGaussianBlur stdDeviation="2" result="blur"/>',
        f'<feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>',
        f'</filter>',
        f'</defs>',

        # Background with subtle glow
        f'<rect width="{CARD_W}" height="{CARD_H}" rx="16" fill="url(#cardBg)" filter="url(#cardGlow)"/>',
        f'<rect x="0.5" y="0.5" width="{CARD_W - 1}" height="{CARD_H - 1}" rx="15.5" fill="none" stroke="{BORDER}" stroke-width="1" opacity="0.6"/>',

        # Top accent bar
        f'<rect width="{CARD_W}" height="3" rx="16 16 0 0">',
        f'<animate attributeName="opacity" values="1;0.6;1" dur="3s" repeatCount="indefinite"/>',
        f'<animate attributeName="fill" values="{ACCENT_CYAN};{ACCENT_GREEN};{ACCENT_GOLD};{ACCENT_CYAN}" dur="6s" repeatCount="indefinite"/>',
        f'</rect>',
    ]

    y = TITLE_H

    # Title bar
    svg.append(
        f'<rect x="0" y="0" width="{CARD_W}" height="{TITLE_H}" rx="16 16 0 0" fill="{BG}"/>'
    )
    svg.append(
        f'<line x1="0" y1="{TITLE_H}" x2="{CARD_W}" y2="{TITLE_H}" stroke="{BORDER}" stroke-width="0.5"/>'
    )
    # Window controls
    for i, (color, cx) in enumerate([("#ff5f56", 18), ("#ffbd2e", 36), ("#27c93f", 54)]):
        svg.append(f'<circle cx="{cx}" cy="{TITLE_H/2}" r="6" fill="{color}"/>')

    # Title text
    if not static:
        svg.append(
            f'<text class="title-bar mono" x="{PADDING}" y="{TITLE_H - 10}" font-size="13" font-weight="600" fill="{TEXT_PRIMARY}">'
            f'<tspan class="accent-green">{INFO_DATA["user"]}</tspan>'
            f'<tspan fill="{TEXT_MUTED}">@</tspan>'
            f'<tspan class="accent-cyan">{INFO_DATA["host"]}</tspan>'
            f'<tspan fill="{TEXT_MUTED}"> ~ $ neofetch --premium</tspan>'
            f'</text>'
        )
    else:
        svg.append(
            f'<text class="mono" x="{PADDING}" y="{TITLE_H - 10}" font-size="13" font-weight="600" fill="{TEXT_PRIMARY}">'
            f'<tspan fill="{ACCENT_GREEN}">{INFO_DATA["user"]}</tspan>'
            f'<tspan fill="{TEXT_MUTED}">@</tspan>'
            f'<tspan fill="{ACCENT_CYAN}">{INFO_DATA["host"]}</tspan>'
            f'</text>'
        )

    y += 16

    # ─── Helper: Add animated row ─────────────────────────────────
    def add_row(idx: int, label: str, value: str, label_color: str = ACCENT_CORAL, value_color: str = TEXT_PRIMARY, indent: int = 0, extra: str = ""):
        nonlocal y
        delay = idx * 0.04
        anim = f'style="animation-delay: {delay:.2f}s"' if not static else ''
        x = PADDING + indent
        svg.append(
            f'<g class="card-row" {anim}>'
            f'<text x="{x}" y="{y}" font-size="12" font-weight="600" fill="{label_color}" class="mono">{label}</text>'
            f'<text x="{x + 100}" y="{y}" font-size="12" fill="{value_color}" class="mono">{value}</text>'
            f'{extra}'
            f'</g>'
        )
        y += LINE_H

    # ─── System Info Section ─────────────────────────────────────
    sys_info = [
        ("OS", INFO_DATA["os"], ACCENT_CORAL, TEXT_PRIMARY),
        ("Uptime", INFO_DATA["uptime"], ACCENT_GOLD, TEXT_SECONDARY),
        ("Shell", INFO_DATA["shell"], ACCENT_CYAN, TEXT_SECONDARY),
        ("Editor", INFO_DATA["editor"], ACCENT_PURPLE, TEXT_SECONDARY),
        ("Terminal", INFO_DATA["terminal"], ACCENT_GREEN, TEXT_SECONDARY),
        ("WM", INFO_DATA["wm"], ACCENT_ORANGE, TEXT_SECONDARY),
    ]
    for i, (label, value, lc, vc) in enumerate(sys_info):
        add_row(i, label, value, lc, vc)

    y += SECTION_GAP * 0.5

    # Title row
    delay = len(sys_info) * 0.04
    anim = f'style="animation-delay: {delay:.2f}s"' if not static else ''
    svg.append(
        f'<text class="card-row mono" x="{PADDING}" y="{y}" font-size="11" font-weight="700" fill="{ACCENT_GOLD}" letter-spacing="1.5" {anim}>{INFO_DATA["title"]}</text>'
    )
    y += LINE_H + 4

    # Location & Education
    for i, (label, value, icon) in enumerate([
        ("📍", INFO_DATA["location"], ""),
        ("🎓", INFO_DATA["education"], ""),
        ("🎯", INFO_DATA["focus"], ""),
    ]):
        delay = (len(sys_info) + 1 + i) * 0.04
        anim = f'style="animation-delay: {delay:.2f}s"' if not static else ''
        svg.append(
            f'<text class="card-row mono" x="{PADDING}" y="{y}" font-size="11" fill="{TEXT_SECONDARY}" {anim}>'
            f'<tspan fill="{ACCENT_CYAN}">{icon}</tspan> {value}'
            f'</text>'
        )
        y += LINE_H

    y += SECTION_GAP * 0.5

    # Divider
    delay = (len(sys_info) + 5) * 0.04
    anim = f'style="animation-delay: {delay:.2f}s"' if not static else ''
    svg.append(
        f'<line class="divider card-row" x1="{PADDING}" y1="{y}" x2="{CARD_W - PADDING}" y2="{y}" stroke="{BORDER}" stroke-width="1" stroke-dasharray="4,4" {anim}/>'
    )
    y += SECTION_GAP

    # ─── Skills with Animated Bars ───────────────────────────────
    skill_section_start = len(sys_info) + 6
    skill_header_delay = skill_section_start * 0.04
    anim = f'style="animation-delay: {skill_header_delay:.2f}s"' if not static else ''
    svg.append(
        f'<text class="card-row mono" x="{PADDING}" y="{y}" font-size="11" font-weight="700" fill="{ACCENT_CYAN}" letter-spacing="1" {anim}>CORE COMPETENCIES</text>'
    )
    y += LINE_H + 4

    for i, (category, desc, color, pct) in enumerate(INFO_DATA["skills"]):
        idx = skill_section_start + 1 + i
        delay = idx * 0.04
        anim = f'style="animation-delay: {delay:.2f}s"' if not static else ''

        bar_w = 180
        bar_h = 6
        bar_x = PADDING + 110
        bar_y = y - 10
        fill_w = bar_w * pct / 100

        svg.append(
            f'<g class="card-row" {anim}>'
            f'<text x="{PADDING}" y="{y}" font-size="11" font-weight="600" fill="{color}" class="mono">{category}</text>'
            f'<text x="{PADDING + 100}" y="{y}" font-size="10" fill="{TEXT_MUTED}" class="mono">{pct}%</text>'
            # Bar background
            f'<rect class="skill-bar-bg" x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="3" fill="{BG}"/>'
            # Bar fill - animated
            f'<rect class="skill-bar-fill" x="{bar_x}" y="{bar_y}" width="{fill_w}" height="{bar_h}" rx="3" fill="{color}" style="--bar-width: {fill_w}px; animation-delay: {delay + 0.15:.2f}s"/>'
            f'</g>'
        )
        y += LINE_H

    y += SECTION_GAP * 0.5

    # Divider
    delay = (skill_section_start + len(INFO_DATA["skills"]) + 1) * 0.04
    anim = f'style="animation-delay: {delay:.2f}s"' if not static else ''
    svg.append(
        f'<line class="divider card-row" x1="{PADDING}" y1="{y}" x2="{CARD_W - PADDING}" y2="{y}" stroke="{BORDER}" stroke-width="1" stroke-dasharray="4,4" {anim}/>'
    )
    y += SECTION_GAP

    # ─── Featured Projects ───────────────────────────────────────
    proj_section_start = skill_section_start + len(INFO_DATA["skills"]) + 2
    header_delay = proj_section_start * 0.04
    anim = f'style="animation-delay: {header_delay:.2f}s"' if not static else ''
    svg.append(
        f'<text class="card-row mono" x="{PADDING}" y="{y}" font-size="11" font-weight="700" fill="{ACCENT_GOLD}" letter-spacing="1" {anim}>FEATURED PROJECTS</text>'
    )
    y += LINE_H + 4

    for i, (name, subtitle, desc, icon, color) in enumerate(INFO_DATA["projects"]):
        idx = proj_section_start + 1 + i * 2
        delay = idx * 0.04
        anim = f'style="animation-delay: {delay:.2f}s"' if not static else ''

        # Project header
        svg.append(
            f'<g class="card-row" {anim}>'
            f'<text x="{PADDING}" y="{y}" font-size="14" fill="{color}" class="project-icon">{icon}</text>'
            f'<text x="{PADDING + 24}" y="{y}" font-size="12" font-weight="700" fill="{TEXT_PRIMARY}" class="mono">{name}</text>'
            f'<text x="{PADDING + 24 + len(name) * 7.5 + 8}" y="{y}" font-size="11" fill="{color}" class="mono">{subtitle}</text>'
            f'</g>'
        )
        y += LINE_H

        # Project description
        delay2 = (idx + 1) * 0.04
        anim2 = f'style="animation-delay: {delay2:.2f}s"' if not static else ''
        svg.append(
            f'<text class="card-row mono" x="{PADDING + 24}" y="{y}" font-size="10" fill="{TEXT_SECONDARY}" {anim2}>{desc}</text>'
        )
        y += LINE_H + 2

    y += SECTION_GAP * 0.5

    # Divider
    delay = (proj_section_start + len(INFO_DATA["projects"]) * 2 + 1) * 0.04
    anim = f'style="animation-delay: {delay:.2f}s"' if not static else ''
    svg.append(
        f'<line class="divider card-row" x1="{PADDING}" y1="{y}" x2="{CARD_W - PADDING}" y2="{y}" stroke="{BORDER}" stroke-width="1" stroke-dasharray="4,4" {anim}/>'
    )
    y += SECTION_GAP

    # ─── GitHub Stats ────────────────────────────────────────────
    stats_section = proj_section_start + len(INFO_DATA["projects"]) * 2 + 2
    header_delay = stats_section * 0.04
    anim = f'style="animation-delay: {header_delay:.2f}s"' if not static else ''
    svg.append(
        f'<text class="card-row mono" x="{PADDING}" y="{y}" font-size="11" font-weight="700" fill="{ACCENT_GREEN}" letter-spacing="1" {anim}>GITHUB METRICS</text>'
    )
    y += LINE_H + 6

    stats_items = [
        ("Contributions", INFO_DATA["stats"]["contributions"], ACCENT_GREEN),
        ("Repositories", INFO_DATA["stats"]["repos"], ACCENT_CYAN),
        ("Stars Earned", INFO_DATA["stats"]["stars"], ACCENT_GOLD),
        ("Followers", INFO_DATA["stats"]["followers"], ACCENT_PURPLE),
        ("Current Streak", INFO_DATA["stats"]["streak"], ACCENT_CORAL),
        ("Longest Streak", INFO_DATA["stats"]["longest_streak"], ACCENT_ORANGE),
    ]

    for i, (label, value, color) in enumerate(stats_items):
        idx = stats_section + 1 + i
        delay = idx * 0.04
        anim = f'style="animation-delay: {delay:.2f}s"' if not static else ''

        col = i % 3
        row = i // 3
        x = PADDING + col * 160
        row_y = y + row * 36

        svg.append(
            f'<g class="card-row" {anim} transform="translate({x}, {row_y - y})">'
            f'<text x="0" y="0" font-size="20" font-weight="700" fill="{color}" class="mono stat-value">{value}</text>'
            f'<text x="0" y="20" font-size="10" fill="{TEXT_MUTED}" class="mono">{label}</text>'
            f'</g>'
        )

    y += 72

    y += SECTION_GAP * 0.5

    # Divider
    delay = (stats_section + len(stats_items) + 1) * 0.04
    anim = f'style="animation-delay: {delay:.2f}s"' if not static else ''
    svg.append(
        f'<line class="divider card-row" x1="{PADDING}" y1="{y}" x2="{CARD_W - PADDING}" y2="{y}" stroke="{BORDER}" stroke-width="1" stroke-dasharray="4,4" {anim}/>'
    )
    y += SECTION_GAP

    # ─── Links ────────────────────────────────────────────────────
    links_section = stats_section + len(stats_items) + 2
    header_delay = links_section * 0.04
    anim = f'style="animation-delay: {header_delay:.2f}s"' if not static else ''
    svg.append(
        f'<text class="card-row mono" x="{PADDING}" y="{y}" font-size="11" font-weight="700" fill="{ACCENT_PURPLE}" letter-spacing="1" {anim}>CONNECT</text>'
    )
    y += LINE_H + 4

    for i, (label, value, url) in enumerate(INFO_DATA["links"]):
        idx = links_section + 1 + i
        delay = idx * 0.04
        anim = f'style="animation-delay: {delay:.2f}s"' if not static else ''

        svg.append(
            f'<a href="{url}" target="_blank" class="card-row interactive" {anim}>'
            f'<text x="{PADDING}" y="{y}" font-size="11" font-weight="600" fill="{ACCENT_CYAN}" class="mono">{label}</text>'
            f'<text x="{PADDING + 80}" y="{y}" font-size="11" fill="{TEXT_SECONDARY}" class="mono">{value}</text>'
            f'<text x="{CARD_W - PADDING - 16}" y="{y}" font-size="10" fill="{TEXT_MUTED}" class="mono">↗</text>'
            f'</a>'
        )
        y += LINE_H

    # Bottom accent bar
    svg.append(
        f'<rect x="0" y="{CARD_H - 3}" width="{CARD_W}" height="3" rx="0 0 16 16" fill="url(#cyanGrad)"/>'
    )

    svg.append("</svg>")
    return "\n".join(svg)


def main():
    static = os.environ.get("STATIC") == "1"
    svg = generate_card(static=static)
    output_path = Path("premium-info-card.svg")
    output_path.write_text(svg)
    print(f"✓ Generated {output_path} ({'static' if static else 'animated'}) — {len(svg)} bytes")


if __name__ == "__main__":
    main()