"""Genera una animación SVG compacta con la actividad semanal de GitHub."""
import json, os, sys, urllib.request
from datetime import date

USER = os.environ.get("USERNAME", "luisbravobello")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = sys.argv[1] if len(sys.argv) > 1 else "dist/activity.svg"
WEEKS = 26

QUERY = """query($login:String!){user(login:$login){contributionsCollection{
contributionCalendar{totalContributions weeks{contributionDays{contributionCount date}}}}}}"""


def fetch():
    if os.environ.get("FAKE"):
        import random
        r = random.Random(3)
        return 268, [[r.choice([0, 0, 0, 1, 2, 3, 6, 9]) for _ in range(7)] for _ in range(53)]
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"},
    )
    cal = json.load(urllib.request.urlopen(req))["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    weeks = [[d["contributionCount"] for d in w["contributionDays"]] for w in cal["weeks"]]
    return cal["totalContributions"], weeks


def build(total, weeks):
    days = [c for w in weeks for c in w]
    active = sum(1 for c in days if c > 0)
    best_day = max(days) if days else 0
    recent = [sum(w) for w in weeks[-WEEKS:]]
    peak = max(recent) or 1

    W, H = 900, 200
    left, right, top, base = 330, 880, 40, 168
    slot = (right - left) / len(recent)
    bw = slot * 0.62
    bars = []
    for i, v in enumerate(recent):
        h = max(4, (base - top) * v / peak) if v else 4
        x = left + i * slot + (slot - bw) / 2
        fill = "url(#bar)" if v else "#2D1648"
        delay = i * 0.06
        bars.append(
            f'<rect class="b" x="{x:.1f}" y="{base - h:.1f}" width="{bw:.1f}" height="{h:.1f}" rx="{bw/2.6:.1f}" '
            f'fill="{fill}" style="animation-delay:{delay:.2f}s"/>'
        )
        if v == peak and v:
            bars.append(f'<circle class="p" cx="{x + bw/2:.1f}" cy="{base - h - 9:.1f}" r="3.5" fill="#FFC857"/>')

    stats = [("Contributions", total, "#FF2E97"), ("Active days", active, "#FF8C42"), ("Best day", best_day, "#FFC857")]
    st = []
    for i, (label, val, color) in enumerate(stats):
        y = 62 + i * 46
        st.append(
            f'<g class="s" style="animation-delay:{0.2 + i*0.15:.2f}s">'
            f'<rect x="28" y="{y-24}" width="4" height="34" rx="2" fill="{color}"/>'
            f'<text x="44" y="{y}" class="v" fill="{color}">{val}</text>'
            f'<text x="44" y="{y+15}" class="l">{label}</text></g>'
        )

    font = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1A0B2E"/><stop offset="1" stop-color="#2A0F45"/></linearGradient>
<linearGradient id="bar" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#7B2CBF"/><stop offset="0.55" stop-color="#FF2E97"/><stop offset="1" stop-color="#FF8C42"/></linearGradient>
<linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffffff" stop-opacity="0"/><stop offset="0.5" stop-color="#ffffff" stop-opacity="0.16"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient>
<clipPath id="area"><rect x="{left-6}" y="{top-14}" width="{right-left+12}" height="{base-top+18}"/></clipPath>
</defs>
<style>
text{{font-family:{font}}}
.v{{font-size:24px;font-weight:800}}
.l{{font-size:11px;fill:#C4B5FD;letter-spacing:1px;text-transform:uppercase}}
.t{{font-size:12px;fill:#C4B5FD;letter-spacing:1px}}
.b{{transform-box:fill-box;transform-origin:bottom;transform:scaleY(0);animation:grow .7s cubic-bezier(.2,.9,.3,1.2) forwards}}
.p{{opacity:0;animation:pop .5s 1.8s forwards, pulse 1.6s 2.3s ease-in-out infinite}}
.s{{opacity:0;animation:fade .6s forwards}}
.sw{{animation:sweep 3.5s 1.6s linear infinite;transform:translateX(-200px)}}
@keyframes grow{{to{{transform:scaleY(1)}}}}
@keyframes fade{{from{{opacity:0;transform:translateX(-8px)}}to{{opacity:1;transform:none}}}}
@keyframes pop{{to{{opacity:1}}}}
@keyframes pulse{{50%{{opacity:.25}}}}
@keyframes sweep{{to{{transform:translateX({right-left+200}px)}}}}
</style>
<rect width="{W}" height="{H}" rx="14" fill="url(#bg)"/>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="#7B2CBF" stroke-opacity="0.45"/>
<line x1="300" y1="28" x2="300" y2="172" stroke="#7B2CBF" stroke-opacity="0.4"/>
<text x="{left}" y="26" class="t">WEEKLY ACTIVITY · LAST {WEEKS} WEEKS</text>
<line x1="{left-6}" y1="{base+0.5}" x2="{right+6}" y2="{base+0.5}" stroke="#7B2CBF" stroke-opacity="0.5"/>
{''.join(st)}
<g clip-path="url(#area)">{''.join(bars)}<rect class="sw" x="{left-6}" y="{top-14}" width="120" height="{base-top+18}" fill="url(#sweep)"/></g>
<text x="{right}" y="188" class="t" text-anchor="end">Updated {date.today().isoformat()}</text>
</svg>'''


total, weeks = fetch()
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
open(OUT, "w").write(build(total, weeks))
print("wrote", OUT)
