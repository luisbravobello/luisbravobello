import math, random, sys, os

def bez(p0,p1,p2,t):
    x=(1-t)**2*p0[0]+2*(1-t)*t*p1[0]+t*t*p2[0]
    y=(1-t)**2*p0[1]+2*(1-t)*t*p1[1]+t*t*p2[1]
    dx=2*(1-t)*(p1[0]-p0[0])+2*t*(p2[0]-p1[0])
    dy=2*(1-t)*(p1[1]-p0[1])+2*t*(p2[1]-p1[1])
    n=math.hypot(dx,dy) or 1
    return x,y,dx/n,dy/n

def frond(p0,p1,p2,lmax,fill,op,rng,n=20,sweep=0.75):
    parts=[]
    for side in (1,-1):
        for i in range(2,n):
            t=i/n
            x,y,tx,ty=bez(p0,p1,p2,t)
            nx,ny=-ty*side,tx*side
            L=lmax*(math.sin(math.pi*min(1,t*1.15))**0.7)*rng.uniform(0.75,1.1)
            if L<4: continue
            # tip: along normal, swept back toward tangent
            ax=nx*math.cos(sweep)+tx*math.sin(sweep)
            ay=ny*math.cos(sweep)+ty*math.sin(sweep)
            tipx,tipy=x+ax*L,y+ay*L
            w=lmax*0.16*(1-t*0.45)
            b1=(x-tx*w,y-ty*w); b2=(x+tx*w*1.6,y+ty*w*1.6)
            # slightly curved leaflet
            cx=(x+tipx)/2+tx*w*1.2; cy=(y+tipy)/2+ty*w*1.2
            parts.append(f"M{b1[0]:.1f},{b1[1]:.1f} Q{cx:.1f},{cy:.1f} {tipx:.1f},{tipy:.1f} L{b2[0]:.1f},{b2[1]:.1f}Z")
    spine=f"M{p0[0]:.1f},{p0[1]:.1f} Q{p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return (f'<g fill="{fill}" fill-opacity="{op}"><path d="{" ".join(parts)}"/></g>'
            f'<path d="{spine}" fill="none" stroke="{fill}" stroke-opacity="{op}" stroke-width="{max(3,lmax*0.07):.1f}" stroke-linecap="round"/>')

def scene(w,h,seed,fronds):
    rng=random.Random(seed); out=[]
    for (p0,p1,p2,l,fill,op) in fronds:
        out.append(frond(p0,p1,p2,l,fill,op,rng))
    return "".join(out)

DEFS='''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#3A2FD6"/><stop offset="0.5" stop-color="#8A3FE0"/><stop offset="1" stop-color="#E45FD8"/></linearGradient>
<linearGradient id="glow" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#FF8C42" stop-opacity="0.35"/><stop offset="0.6" stop-color="#FF2E97" stop-opacity="0"/></linearGradient>
<linearGradient id="shade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#1A0B2E" stop-opacity="0.55"/><stop offset="0.7" stop-color="#1A0B2E" stop-opacity="0"/></linearGradient>
</defs>'''
FONT="font-family=\"'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif\""

DARK="#4B22C9"; LIGHT="#F3B8F0"; MID="#6A2BD9"

def banner():
    w,h=1200,340
    fr=[
     ((1300,420),(980,120),(560,90),260,DARK,0.7),
     ((-80,420),(200,150),(640,30),240,MID,0.55),
     ((860,-80),(1000,120),(1280,240),190,LIGHT,0.45),
     ((-60,-60),(180,50),(480,-40),170,LIGHT,0.35),
     ((420,460),(640,260),(1000,330),200,DARK,0.5),
    ]
    sv=scene(w,h,7,fr)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{DEFS}
<clipPath id="c"><rect width="{w}" height="{h}" rx="22"/></clipPath><g clip-path="url(#c)">
<rect width="{w}" height="{h}" fill="url(#bg)"/>{sv}<rect width="{w}" height="{h}" fill="url(#glow)"/><rect width="{w}" height="{h}" fill="url(#shade)"/>
<text x="70" y="160" {FONT} font-size="58" font-weight="800" fill="#ffffff" letter-spacing="1">Luis Alejandro Bravo Bello</text>
<rect x="72" y="185" width="120" height="5" rx="2.5" fill="#FF8C42"/><rect x="198" y="185" width="60" height="5" rx="2.5" fill="#FF2E97"/>
<text x="72" y="232" {FONT} font-size="24" font-weight="600" fill="#FFE8F3">Full Stack Developer  ·  Software Engineering Student @ UCE</text>
<text x="72" y="270" {FONT} font-size="18" fill="#FFE8F3" fill-opacity="0.85">C#  ·  .NET  ·  SQL  ·  OpenGL  ·  Punta Cana, Dominican Republic</text>
</g></svg>'''

def title(text,seed):
    w,h=1200,110
    rng=random.Random(seed)
    o=rng.uniform(-80,80)
    fr=[
     ((1260,170),(1020+o,30),(680+o,20),150,DARK,0.65),
     ((780+o,-50),(940,60),(1260,90),120,LIGHT,0.45),
     ((-60,160),(160,70),(460+o,100),110,MID,0.45),
    ]
    sv=scene(w,h,seed,fr)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{DEFS}
<clipPath id="c"><rect width="{w}" height="{h}" rx="16"/></clipPath><g clip-path="url(#c)">
<rect width="{w}" height="{h}" fill="url(#bg)"/>{sv}<rect width="{w}" height="{h}" fill="url(#shade)"/>
<rect x="40" y="34" width="6" height="42" rx="3" fill="#FF8C42"/>
<text x="64" y="70" {FONT} font-size="36" font-weight="800" fill="#ffffff" letter-spacing="0.5">{text}</text>
</g></svg>'''

def footer():
    w,h=1200,170
    fr=[
     ((-60,260),(300,50),(760,50),210,DARK,0.65),
     ((1270,250),(980,40),(580,80),200,MID,0.55),
     ((680,260),(860,130),(1180,160),140,LIGHT,0.45),
    ]
    sv=scene(w,h,21,fr)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{DEFS}
<clipPath id="c"><rect width="{w}" height="{h}" rx="22"/></clipPath><g clip-path="url(#c)">
<rect width="{w}" height="{h}" fill="url(#bg)"/>{sv}<rect width="{w}" height="{h}" fill="url(#glow)"/>
<text x="600" y="95" text-anchor="middle" {FONT} font-size="26" font-weight="700" fill="#ffffff">Thanks for visiting</text>
<text x="600" y="128" text-anchor="middle" {FONT} font-size="17" fill="#FFE8F3">Start with the problem, then choose the tool.</text>
</g></svg>'''

out=sys.argv[1]; os.makedirs(out,exist_ok=True)
open(f"{out}/banner.svg","w").write(banner())
open(f"{out}/footer.svg","w").write(footer())
for i,(slug,t) in enumerate([("about","About me"),("stack","Tech stack"),("projects","Featured projects"),("stats","GitHub stats"),("pacman","Contribution Pac-Man"),("connect","Let's connect")]):
    open(f"{out}/title-{slug}.svg","w").write(title(t,100+i*13))
