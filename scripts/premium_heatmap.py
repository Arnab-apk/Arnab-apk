#!/usr/bin/env python3
"""
Premium Contribution Heatmap - Sophisticated animated contribution calendar
with diagonal wave reveal, tooltip-style stats, and premium styling.
"""
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# ─── Configuration ──────────────────────────────────────────────
BOX_SIZE = 13
BOX_RADIUS = 3
BOX_GAP = 4
WEEKS = 53
DAYS = 7

MARGIN_LEFT = 50
MARGIN_TOP = 50
TITLE_H = 44
LEGEND_H = 40
STATS_H = 100

# Premium color palette - GitHub-inspired but elevated
PALETTE = [
    "#0d1520",  # Level 0 - deep void
    "#162a1e",  # Level 1 - subtle green tint
    "#0e4429",  # Level 2 - github green dark
    "#006d32",  # Level 3 - github green
    "#26a641",  # Level 4 - github green bright
    "#39d353",  # Level 5 - github green brighter
    "#69f0a0",  # Level 6 - neon accent
]

# Premium theme colors
BG_DEEP = "#05080e"
BG_CARD = "#0a0f1a"
BORDER = "#1a2a3a"
BORDER_GLOW = "#00d4ff"

ACCENT_CYAN = "#00d4ff"
ACCENT_GREEN = "#00ff88"
ACCENT_GOLD = "#ffd700"
ACCENT_CORAL = "#ff6b6b"

TEXT_PRIMARY = "#f0f4f9"
TEXT_SECONDARY = "#a0b0c0"
TEXT_MUTED = "#5a6a7a"
TEXT_DIM = "#3a4a5a"

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DAY_LABELS = ["Mon", "Wed", "Fri"]


def level_for(count: int) -> int:
    if count == 0:
        return 0
    elif count <= 3:
        return 1
    elif count <= 6:
        return 2
    elif count <= 10:
        return 3
    elif count <= 15:
        return 4
    elif count <= 25:
        return 5
    else:
        return 6


def load_data():
    """Load contribution data from JSON."""
    path = Path("data/contributions.json")
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {"contributions": [], "total_contributions": 0, "current_streak": 0, "longest_streak": 0, "best_day": {"date": "", "count": 0}}


def build_grid(contributions):
    """Build 53x7 grid from contributions list."""
    contrib_map = {c["date"]: c["count"] for c in contributions}

    today = datetime.now().date()
    start_date = today - timedelta(weeks=53)
    start_date = start_date - timedelta(days=start_date.weekday())  # Start on Sunday

    grid = []
    for week in range(WEEKS):
        week_data = []
        for day in range(DAYS):
            current_date = start_date + timedelta(weeks=week, days=day)
            date_str = current_date.isoformat()
            count = contrib_map.get(date_str, 0)
            color = PALETTE[level_for(count)]
            week_data.append({"date": date_str, "count": count, "color": color, "level": level_for(count)})
        grid.append(week_data)

    return grid, start_date


def generate_heatmap(static: bool = False) -> str:
    """Generate the premium animated heatmap SVG."""
    data = load_data()
    contributions = data.get("contributions", [])
    total = data.get("total_contributions", 0)
    current_streak = data.get("current_streak", 0)
    longest_streak = data.get("longest_streak", 0)
    best_day = data.get("best_day", {"date": "", "count": 0})
    username = "Arnab-apk"

    grid, start_date = build_grid(contributions)
    n_cols = len(grid)

    # Calculate dimensions
    grid_w = n_cols * (BOX_SIZE + BOX_GAP) - BOX_GAP
    grid_h = DAYS * (BOX_SIZE + BOX_GAP) - BOX_GAP

    CANVAS_W = MARGIN_LEFT * 2 + grid_w + 40
    CANVAS_H = TITLE_H + MARGIN_TOP + grid_h + LEGEND_H + STATS_H + MARGIN_TOP

    # ─── Animation CSS ──────────────────────────────────────────
    if not static:
        css = f"""
  <style>
    @keyframes waveReveal {{
      0% {{ opacity: 0; transform: translate(-8px, -8px) scale(0.7); filter: blur(2px); }}
      50% {{ opacity: 0.8; transform: translate(0, 0) scale(1.05); filter: blur(0); }}
      100% {{ opacity: 1; transform: translate(0, 0) scale(1); filter: blur(0); }}
    }}
    @keyframes fadeInUp {{
      from {{ opacity: 0; transform: translateY(10px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes countUp {{
      from {{ opacity: 0; transform: scale(0.5); }}
      to {{ opacity: 1; transform: scale(1); }}
    }}
    @keyframes pulseGlow {{
      0%, 100% {{ opacity: 0.3; }}
      50% {{ opacity: 1; }}
    }}
    .contrib-box {{
      opacity: 0;
      animation: waveReveal 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }}
    .stat-value {{
      opacity: 0;
      animation: countUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }}
    .legend-item {{
      opacity: 0;
      animation: fadeInUp 0.4s ease-out forwards;
    }}
    .month-label {{
      opacity: 0;
      animation: fadeInUp 0.4s ease-out forwards;
    }}
    .day-label {{
      opacity: 0;
      animation: fadeInUp 0.4s ease-out forwards;
    }}
    .title-text {{
      opacity: 0;
      animation: fadeInUp 0.5s ease-out 0.1s forwards;
    }}
    .wave-line {{
      stroke-dasharray: 1000;
      stroke-dashoffset: 1000;
      animation: drawWave 2s ease-out forwards;
    }}
    @keyframes drawWave {{
      to {{ stroke-dashoffset: 0; }}
    }}
    .mono {{
      font-family: 'ui-monospace', 'SFMono-Regular', 'Menlo', 'Consolas', monospace;
    }}
  </style>
"""
    else:
        css = f"""
  <style>
    .mono {{
      font-family: 'ui-monospace', 'SFMono-Regular', 'Menlo', 'Consolas', monospace;
    }}
    .contrib-box, .stat-value, .legend-item, .month-label, .day-label {{ opacity: 1; }}
  </style>
"""

    grid_left = MARGIN_LEFT
    grid_top = TITLE_H + MARGIN_TOP

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" viewBox="0 0 {CANVAS_W} {CANVAS_H}" role="img" aria-label="GitHub Contribution Graph for {username}">',
        css,
        # Defs
        f'<defs>',
        f'<linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="1">',
        f'<stop offset="0%" stop-color="{BG_CARD}"/>',
        f'<stop offset="100%" stop-color="{BG_DEEP}"/>',
        f'</linearGradient>',
        f'<linearGradient id="titleGrad" x1="0" y1="0" x2="1" y2="0">',
        f'<stop offset="0%" stop-color="{ACCENT_CYAN}"/>',
        f'<stop offset="50%" stop-color="{ACCENT_GREEN}"/>',
        f'<stop offset="100%" stop-color="{ACCENT_GOLD}"/>',
        f'</linearGradient>',
        f'<filter id="boxGlow" x="-50%" y="-50%" width="200%" height="200%">',
        f'<feGaussianBlur stdDeviation="2" result="blur"/>',
        f'<feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>',
        f'</filter>',
        f'<filter id="textGlow" x="-50%" y="-50%" width="200%" height="200%">',
        f'<feGaussianBlur stdDeviation="1.5" result="blur"/>',
        f'<feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>',
        f'</filter>',
        f'<pattern id="subtleGrid" width="40" height="40" patternUnits="userSpaceOnUse">',
        f'<rect width="40" height="40" fill="{BG_DEEP}"/>',
        f'<path d="M40,0 L0,0 0,40" fill="none" stroke="{BORDER}" stroke-width="0.2" opacity="0.2"/>',
        f'</pattern>',
        f'</defs>',

        # Background
        f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="20" fill="url(#bgGrad)"/>',
        f'<rect x="0.5" y="0.5" width="{CANVAS_W - 1}" height="{CANVAS_H - 1}" rx="19.5" fill="none" stroke="{BORDER}" stroke-width="1" opacity="0.4"/>',
        f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="20" fill="url(#subtleGrid)"/>',

        # Top accent bar
        f'<rect width="{CANVAS_W}" height="4" rx="20 20 0 0">',
        f'<animate attributeName="fill" values="{ACCENT_CYAN};{ACCENT_GREEN};{ACCENT_GOLD};{ACCENT_CORAL};{ACCENT_CYAN}" dur="8s" repeatCount="indefinite"/>',
        f'</rect>',

        # Title bar
        f'<rect x="0" y="0" width="{CANVAS_W}" height="{TITLE_H}" rx="20 20 0 0" fill="{BG_DEEP}"/>',
        f'<line x1="0" y1="{TITLE_H}" x2="{CANVAS_W}" y2="{TITLE_H}" stroke="{BORDER}" stroke-width="0.5"/>',

        # Window controls
        f'<circle cx="18" cy="{TITLE_H/2}" r="7" fill="#ff5f56"/>',
        f'<circle cx="38" cy="{TITLE_H/2}" r="7" fill="#ffbd2e"/>',
        f'<circle cx="58" cy="{TITLE_H/2}" r="7" fill="#27c93f"/>',

        # Title
        f'<text class="title-text mono" x="{MARGIN_LEFT}" y="{TITLE_H - 12}" font-size="14" font-weight="600" fill="{TEXT_SECONDARY}">'
        f'<tspan class="accent-green">{username.split("-")[0]}</tspan>'
        f'<tspan fill="{TEXT_MUTED}">@</tspan>'
        f'<tspan class="accent-cyan">github</tspan>'
        f'<tspan fill="{TEXT_MUTED}"> ~ $ contributions --graph --premium</tspan>'
        f'</text>',

        # Live indicator
        f'<circle cx="{CANVAS_W - 80}" cy="{TITLE_H/2}" r="5" fill="{ACCENT_GREEN}">',
        f'<animate attributeName="opacity" values="1;0.3;1" dur="1.5s" repeatCount="indefinite"/>',
        f'</circle>',
        f'<text class="title-text mono" x="{CANVAS_W - 65}" y="{TITLE_H - 10}" font-size="11" font-weight="600" fill="{ACCENT_GREEN}">LIVE</text>',
    ]

    # Month labels (top of grid)
    seen_months = set()
    for ci, column in enumerate(grid):
        for cell in column:
            if cell is None:
                continue
            date = datetime.fromisoformat(cell["date"]).date()
            key = (date.year, date.month)
            if key not in seen_months and date.day <= 7:
                seen_months.add(key)
                x = grid_left + ci * (BOX_SIZE + BOX_GAP) + BOX_SIZE / 2
                delay = ci * 0.01
                anim = f'style="animation-delay: {delay:.2f}s"' if not static else ''
                svg.append(
                    f'<text class="month-label mono" x="{x}" y="{grid_top - 8}" text-anchor="middle" font-size="10" fill="{TEXT_MUTED}" {anim}>{MONTHS[date.month - 1]}</text>'
                )
            break

    # Day labels (left of grid)
    for day_idx, day_name in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        y = grid_top + day_idx * (BOX_SIZE + BOX_GAP) + BOX_SIZE * 0.7
        delay = day_idx * 0.02
        anim = f'style="animation-delay: {delay:.2f}s"' if not static else ''
        svg.append(
            f'<text class="day-label mono" x="{MARGIN_LEFT - 10}" y="{y:.1f}" text-anchor="end" font-size="9" fill="{TEXT_DIM}" {anim}>{day_name}</text>'
        )

    # ─── Contribution Boxes with Diagonal Wave Animation ──────────
    base_delay = 0.008  # Fast wave propagation

    for ci, column in enumerate(grid):
        gx = grid_left + ci * (BOX_SIZE + BOX_GAP)
        for ri, cell in enumerate(column):
            gy = grid_top + ri * (BOX_SIZE + BOX_GAP)

            # Diagonal wave delay: column + row
            delay = (ci + ri) * base_delay
            anim = f'style="animation-delay: {delay:.3f}s"' if not static else ''

            plural = "s" if cell["count"] != 1 else ""
            tooltip = f'{cell["date"]}: {cell["count"]} contribution{plural}'

            # Level indicator for tooltip
            level_indicator = "●" * (cell["level"] + 1) + "○" * (6 - cell["level"])

            svg.append(
                f'<rect class="contrib-box" x="{gx}" y="{gy}" width="{BOX_SIZE}" height="{BOX_SIZE}" '
                f'rx="{BOX_RADIUS}" ry="{BOX_RADIUS}" fill="{cell["color"]}" {anim}>'
                f'<title>{tooltip} • Level {cell["level"]}/6 • {level_indicator}</title>'
                f'</rect>'
            )

    # ─── Legend ──────────────────────────────────────────────────
    legend_y = grid_top + grid_h + 20
    legend_x = MARGIN_LEFT

    delay = (WEEKS + DAYS) * base_delay
    anim = f'style="animation-delay: {delay:.2f}s"' if not static else ''
    svg.append(
        f'<text class="legend-item mono" x="{legend_x}" y="{legend_y + BOX_SIZE - 2}" font-size="11" fill="{TEXT_MUTED}" {anim}>Less</text>'
    )

    lx = legend_x + 45
    for lvl, color in enumerate(PALETTE):
        delay = (WEEKS + DAYS + lvl) * base_delay
        anim = f'style="animation-delay: {delay:.2f}s"' if not static else ''
        svg.append(
            f'<rect class="legend-item" x="{lx}" y="{legend_y}" width="{BOX_SIZE}" height="{BOX_SIZE}" '
            f'rx="{BOX_RADIUS}" ry="{BOX_RADIUS}" fill="{color}" {anim}/>'
        )
        lx += BOX_SIZE + 3

    delay = (WEEKS + DAYS + len(PALETTE)) * base_delay
    anim = f'style="animation-delay: {delay:.2f}s"' if not static else ''
    svg.append(
        f'<text class="legend-item mono" x="{lx + 8}" y="{legend_y + BOX_SIZE - 2}" font-size="11" fill="{TEXT_MUTED}" {anim}>More</text>'
    )

    # ─── Stats Footer ────────────────────────────────────────────
    stats_y = legend_y + LEGEND_H + 10

    # Separator line
    delay = (WEEKS + DAYS + len(PALETTE) + 1) * base_delay
    anim = f'style="animation-delay: {delay:.2f}s"' if not static else ''
    svg.append(
        f'<line class="divider" x1="{MARGIN_LEFT}" y1="{stats_y - 10}" x2="{CANVAS_W - MARGIN_LEFT}" y2="{stats_y - 10}" stroke="{BORDER}" stroke-width="1" stroke-dasharray="6,6" {anim}/>'
    )

    stat_items = [
        (f"{total:,}", "total contributions", ACCENT_GREEN, "in the last year"),
        (f"{current_streak}", "day streak", ACCENT_CYAN, "current"),
        (f"{longest_streak}", "day streak", ACCENT_GOLD, "longest ever"),
        (f"{best_day['count']}", "contributions", ACCENT_CORAL, f"best day: {best_day['date']}"),
    ]

    for i, (value, label, color, sublabel) in enumerate(stat_items):
        x = MARGIN_LEFT + i * (CANVAS_W // 4)
        delay = (WEEKS + DAYS + len(PALETTE) + 2 + i) * base_delay
        anim_val = f'style="animation-delay: {delay:.2f}s"' if not static else ''
        anim_lbl = f'style="animation-delay: {delay + 0.1:.2f}s"' if not static else ''

        svg.append(
            f'<text class="stat-value mono" x="{x}" y="{stats_y + 12}" font-size="22" font-weight="700" fill="{color}" {anim_val}>{value}</text>'
        )
        svg.append(
            f'<text class="stat-value mono" x="{x}" y="{stats_y + 36}" font-size="11" fill="{TEXT_SECONDARY}" {anim_lbl}>{label}</text>'
        )
        svg.append(
            f'<text class="stat-value mono" x="{x}" y="{stats_y + 52}" font-size="9" fill="{TEXT_MUTED}" {anim_lbl}>{sublabel}</text>'
        )

    # ─── Generation timestamp ────────────────────────────────────
    fetched_at = data.get("fetched_at", "")
    if fetched_at:
        try:
            dt = datetime.fromisoformat(fetched_at.replace("Z", "+00:00"))
            ts = dt.strftime("%b %d, %Y %H:%M UTC")
            svg.append(
                f'<text x="{CANVAS_W - MARGIN_LEFT}" y="{CANVAS_H - 16}" text-anchor="end" class="mono" font-size="9" fill="{TEXT_DIM}">Updated {ts}</text>'
            )
        except Exception:
            pass

    # Bottom accent bar
    svg.append(
        f'<rect x="0" y="{CANVAS_H - 4}" width="{CANVAS_W}" height="4" rx="0 0 20 20" fill="url(#titleGrad)"/>'
    )

    svg.append("</svg>")
    return "\n".join(svg)


def main():
    static = os.environ.get("STATIC") == "1"
    svg = generate_heatmap(static=static)
    output_path = Path("premium-heatmap.svg")
    output_path.write_text(svg)
    print(f"✓ Generated {output_path} ({'static' if static else 'animated'}) — {len(svg)} bytes")


if __name__ == "__main__":
    main()