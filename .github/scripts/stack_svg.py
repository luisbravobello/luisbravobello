"""Genera el panel animado de Tech stack con íconos de skillicons.dev incrustados."""
import os, re, sys, urllib.request
from html import escape

OUT = sys.argv[1] if len(sys.argv) > 1 else "dist/stack.svg"

GROUPS = [
    ("Backend", "APIs, business logic and architecture", "#FF2E97", ["cs", "dotnet", "nodejs", "express"]),
    ("Databases", "Modeling, queries and persistence", "#FF8C42", ["mysql", "postgres", "sqlite"]),
    ("Web", "Structure, styling and interaction", "#FFC857", ["html", "css", "js"]),
    ("Graphics & 3D", "OpenGL rendering and 3D modeling", "#FF2E97", ["c", "blender"]),
    ("Tools & DevOps", "Version control, containers and CI", "#FF8C42", ["git", "github", "githubactions", "docker", "vscode", "visualstudio"]),
    ("Learning now", "What I'm adding to my toolkit", "#FFC857", ["java", "spring", "js", "blender"]),
]

_cache = {}


def icon(name, k):
    """Devuelve el contenido interno del SVG del ícono con ids únicos."""
    if name not in _cache:
        url = f"https://skillicons.dev/icons?i={name}&theme=dark"
        req = urllib.request.Request(url, headers={"User-Agent": "profile-readme"})
        _cache[name] = urllib.request.urlopen(req, timeout=30).read().decode()
    svg = _cache[name]
    inner = re.search(r"<svg[^>]*>(.*)</svg>", svg, re.S).group(1)
    # Los íconos están dentro de un <svg> anidado: prefijamos ids para evitar choques.
    p = f"i{k}_"
    inner = re.sub(r'id="([^"]+)"', lambda m: f'id="{p}{m.group(1)}"', inner)
    inner = re.sub(r"url\(#([^)]+)\)", lambda m: f"url(#{p}{m.group(1)})", inner)
    inner = re.sub(r'href="#([^"]+)"', lambda m: f'href="#{p}{m.group(1)}"', inner)
    vb = re.search(r'viewBox="([^"]+)"', svg)
    vb = vb.group(1) if vb else "0 0 256 256"
    # skillicons devuelve un lienzo con padding; nos quedamos con el primer ícono (256x256).
    return inner, vb


def build():
    W = 900
    cols, card_w, card_h, gap, pad = 2, 438, 128, 20, 2
    rows = (len(GROUPS) + cols - 1) // cols
    H = pad * 2 + rows * card_h + (rows - 1) * gap
    font = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
    parts, k = [], 0
    for gi, (title, sub, color, icons) in enumerate(GROUPS):
        r, c = divmod(gi, cols)
        x = pad + c * (card_w + gap)
        y = pad + r * (card_h + gap)
        d = 0.12 * gi
        parts.append(f'<g class="card" style="animation-delay:{d:.2f}s">')
        parts.append(f'<rect x="{x}" y="{y}" width="{card_w}" height="{card_h}" rx="14" fill="#2D1648" fill-opacity="0.75" stroke="{color}" stroke-opacity="0.28"/>')
        parts.append(f'<rect x="{x}" y="{y+18}" width="4" height="34" rx="2" fill="{color}"/>')
        parts.append(f'<text x="{x+20}" y="{y+36}" class="h">{escape(title)}</text>')
        parts.append(f'<text x="{x+20}" y="{y+54}" class="s">{escape(sub)}</text>')
        size, step = 42, 52
        for ii, name in enumerate(icons):
            inner, vb = icon(name, k); k += 1
            ix = x + 20 + ii * step
            iy = y + card_h - size - 16
            parts.append(
                f'<g class="ic" style="animation-delay:{d + 0.35 + ii*0.07:.2f}s">'
                f'<svg x="{ix}" y="{iy}" width="{size}" height="{size}" viewBox="{vb}">{inner}</svg></g>'
            )
        parts.append("</g>")

    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1A0B2E"/><stop offset="1" stop-color="#2A0F45"/></linearGradient>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FF8C42"/><stop offset="0.5" stop-color="#FF2E97"/><stop offset="1" stop-color="#7B2CBF"/></linearGradient>
</defs>
<style>
text{{font-family:{font}}}
.h{{font-size:19px;font-weight:800;fill:#ffffff}}
.s{{font-size:12.5px;fill:#C4B5FD}}
.card{{opacity:0;animation:in .6s ease-out forwards}}
.ic{{opacity:0;animation:pop .45s cubic-bezier(.2,.9,.3,1.4) forwards}}
@keyframes in{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
@keyframes pop{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
</style>
{''.join(parts)}
</svg>'''


os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
open(OUT, "w").write(build())
print("wrote", OUT)
