"""Motifs d'image à la une propres à ce site, chargés par moteur/images.py (dict MOTIFS {nom: fonction(r, w, h)}).

poele-bois     un poêle en fonte, la vitre sur un feu de bûches, dans une pièce sombre
poele-pellets  un poêle à pellets droit et moderne, la flamme courte au fond du foyer
fournisseur    des palettes de sacs et des stères empilés devant un hangar
"""
import math


def _mix(a, b, t):
    a, b = a.lstrip("#"), b.lstrip("#")
    ca = [int(a[i:i + 2], 16) for i in (0, 2, 4)]
    cb = [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(ca, cb))


def _piece(r, w, h, sol):
    """Mur sombre réchauffé par le feu, sol en planches, halo autour du foyer."""
    defs = ('<radialGradient id="halo" cx="50%" cy="62%" r="55%"><stop offset="0" stop-color="#f08a3c" stop-opacity=".45"/>'
            '<stop offset="1" stop-color="#f08a3c" stop-opacity="0"/></radialGradient>'
            '<radialGradient id="vig" cx="50%" cy="50%" r="75%"><stop offset="50%" stop-color="#000" stop-opacity="0"/>'
            '<stop offset="100%" stop-color="#000" stop-opacity=".6"/></radialGradient>'
            '<filter id="flou" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>')
    out = [f'<rect width="{w}" height="{h}" fill="{r.choice(["#2a211c", "#262420", "#2d2420"])}"/>']
    for i in range(int(w / 140) + 1):   # lambris du mur
        out.append(f'<rect x="{i * 140}" y="0" width="2" height="{sol:.0f}" fill="#000" opacity=".25"/>')
    out.append(f'<rect x="0" y="{sol:.0f}" width="{w}" height="{h - sol:.0f}" fill="#3b2b20"/>')
    y = sol
    while y < h:
        out.append(f'<rect x="0" y="{y:.0f}" width="{w}" height="2" fill="#000" opacity=".3"/>')
        y += 26 + (y - sol) * .35
    out.append(f'<rect width="{w}" height="{h}" fill="url(#halo)"/>')
    return defs, out


def _flammes(r, x, y, larg, haut, n):
    out = []
    for _ in range(n):
        fx, fh, fl = x + r.uniform(.1, .9) * larg, haut * r.uniform(.5, 1), larg * r.uniform(.12, .22)
        for c, k in (("#e0501e", 1), ("#f5a33a", .7), ("#ffe08a", .4)):
            out.append(f'<path d="M{fx - fl * k:.0f} {y:.0f} Q{fx - fl * k * .4:.0f} {y - fh * k * .6:.0f} {fx + r.uniform(-8, 8):.0f} {y - fh * k:.0f} '
                       f'Q{fx + fl * k * .4:.0f} {y - fh * k * .6:.0f} {fx + fl * k:.0f} {y:.0f}Z" fill="{c}" opacity=".9"/>')
    return out


def _une_poele_bois(r, w, h):
    """Poêle en fonte sur pieds : corps noir, vitre cintrée sur un feu de bûches, buse qui monte."""
    sol = h * .74
    defs, out = _piece(r, w, h, sol)
    cx = w * r.choice([.38, .5, .62])
    pw, ph = r.uniform(380, 440), r.uniform(400, 450)
    x0, y0 = cx - pw / 2, sol - ph - 30
    fonte = "#1c1c1e"
    out.append(f'<ellipse cx="{cx:.0f}" cy="{sol + 8:.0f}" rx="{pw * .7:.0f}" ry="26" fill="#000" opacity=".45" filter="url(#flou)"/>')
    out.append(f'<rect x="{cx - 34:.0f}" y="0" width="68" height="{y0:.0f}" fill="{fonte}"/>')
    out.append(f'<rect x="{cx - 34:.0f}" y="0" width="16" height="{y0:.0f}" fill="#fff" opacity=".05"/>')
    for dx in (-pw / 2 + 30, pw / 2 - 50):   # pieds
        out.append(f'<rect x="{cx + dx:.0f}" y="{sol - 34:.0f}" width="20" height="36" fill="{fonte}"/>')
    out.append(f'<rect x="{x0 - 16:.0f}" y="{y0 - 22:.0f}" width="{pw + 32:.0f}" height="26" rx="4" fill="#232325"/>')
    out.append(f'<rect x="{x0:.0f}" y="{y0:.0f}" width="{pw:.0f}" height="{ph:.0f}" rx="10" fill="{fonte}"/>')
    vx, vy, vw, vh = x0 + 50, y0 + 50, pw - 100, ph * .62
    out.append(f'<path d="M{vx:.0f} {vy + vh:.0f} L{vx:.0f} {vy + 60:.0f} Q{cx:.0f} {vy - 40:.0f} {vx + vw:.0f} {vy + 60:.0f} '
               f'L{vx + vw:.0f} {vy + vh:.0f}Z" fill="#2a120a"/>')
    for i in range(3):   # bûches
        by = vy + vh - 22 - i * 12
        out.append(f'<rect x="{vx + 20 + i * 18:.0f}" y="{by:.0f}" width="{vw - 40 - i * 36:.0f}" height="22" rx="11" '
                   f'fill="{_mix("#6b3b1e", "#000000", i * .15)}" transform="rotate({r.uniform(-6, 6):.1f} {cx:.0f} {by:.0f})"/>')
    out += _flammes(r, vx + 30, vy + vh - 30, vw - 60, vh * .7, 6)
    out.append(f'<path d="M{vx:.0f} {vy + vh:.0f} L{vx:.0f} {vy + 60:.0f} Q{cx:.0f} {vy - 40:.0f} {vx + vw:.0f} {vy + 60:.0f} '
               f'L{vx + vw:.0f} {vy + vh:.0f}Z" fill="none" stroke="#3a3a3c" stroke-width="12"/>')
    out.append(f'<rect x="{x0 + 40:.0f}" y="{vy + vh + 30:.0f}" width="{pw - 80:.0f}" height="10" rx="5" fill="#2e2e30"/>')
    out.append(f'<rect width="{w}" height="{h}" fill="url(#vig)"/>')
    return defs, out


def _une_poele_pellets(r, w, h):
    """Poêle à pellets droit, habillage clair ou anthracite, vitre étroite et flamme courte, écran de commande."""
    sol = h * .78
    defs, out = _piece(r, w, h, sol)
    cx = w * r.choice([.36, .5, .64])
    pw, ph = r.uniform(300, 340), r.uniform(560, 610)
    x0, y0 = cx - pw / 2, sol - ph
    corps = r.choice(["#3a3d40", "#d9d4cb", "#7a2f22"])
    out.append(f'<ellipse cx="{cx:.0f}" cy="{sol + 6:.0f}" rx="{pw * .75:.0f}" ry="22" fill="#000" opacity=".45" filter="url(#flou)"/>')
    out.append(f'<rect x="{cx + pw / 2 - 70:.0f}" y="0" width="34" height="{y0 + 10:.0f}" fill="#202022"/>')
    out.append(f'<rect x="{x0:.0f}" y="{y0:.0f}" width="{pw:.0f}" height="{ph:.0f}" rx="18" fill="{corps}"/>')
    out.append(f'<rect x="{x0:.0f}" y="{y0:.0f}" width="{pw * .18:.0f}" height="{ph:.0f}" rx="18" fill="#fff" opacity=".07"/>')
    out.append(f'<rect x="{x0 + 24:.0f}" y="{y0 + 18:.0f}" width="{pw - 48:.0f}" height="34" rx="6" fill="{_mix(corps, "#000000", .25)}"/>')
    out.append(f'<rect x="{x0 + pw / 2 - 40:.0f}" y="{y0 + 26:.0f}" width="80" height="18" rx="3" fill="#0f1a1c"/>')
    out.append(f'<rect x="{x0 + pw / 2 - 30:.0f}" y="{y0 + 32:.0f}" width="34" height="6" rx="2" fill="#5fd0c0" opacity=".8"/>')
    vx, vy, vw, vh = x0 + 36, y0 + 90, pw - 72, ph * .5
    out.append(f'<rect x="{vx:.0f}" y="{vy:.0f}" width="{vw:.0f}" height="{vh:.0f}" rx="8" fill="#140b07"/>')
    out.append(f'<rect x="{vx + vw * .3:.0f}" y="{vy + vh - 26:.0f}" width="{vw * .4:.0f}" height="14" rx="4" fill="#4a2a18"/>')
    out += _flammes(r, vx + vw * .3, vy + vh - 22, vw * .4, vh * .45, 4)
    out.append(f'<rect x="{vx:.0f}" y="{vy:.0f}" width="{vw:.0f}" height="{vh:.0f}" rx="8" fill="none" stroke="#111" stroke-width="10"/>')
    for i in range(4):   # grille d'air chaud
        out.append(f'<rect x="{x0 + 50:.0f}" y="{vy + vh + 40 + i * 16:.0f}" width="{pw - 100:.0f}" height="5" rx="2" '
                   f'fill="{_mix(corps, "#000000", .35)}"/>')
    out.append(f'<rect width="{w}" height="{h}" fill="url(#vig)"/>')
    return defs, out


def _une_fournisseur(r, w, h):
    """Cour d'un dépôt : hangar en bardage, palettes de sacs de pellets, stères de bûches."""
    defs = ('<linearGradient id="ciel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfd8d2"/>'
            '<stop offset="1" stop-color="#f1ece2"/></linearGradient>'
            '<radialGradient id="vig" cx="50%" cy="50%" r="75%"><stop offset="55%" stop-color="#000" stop-opacity="0"/>'
            '<stop offset="100%" stop-color="#000" stop-opacity=".35"/></radialGradient>')
    sol = h * .72
    out = [f'<rect width="{w}" height="{h}" fill="url(#ciel)"/>']
    hx, hw = w * r.uniform(.05, .2), w * r.uniform(.55, .7)
    toit = h * .18
    forme = (f'M{hx:.0f} {sol:.0f} L{hx:.0f} {toit + 80:.0f} L{hx + hw / 2:.0f} {toit:.0f} L{hx + hw:.0f} {toit + 80:.0f} '
             f'L{hx + hw:.0f} {sol:.0f}Z')
    defs += f'<clipPath id="hangar"><path d="{forme}"/></clipPath>'
    out.append(f'<path d="{forme}" fill="#2f4a3a"/>')
    out.append('<g clip-path="url(#hangar)">')
    x = hx
    while x < hx + hw:   # bardage
        out.append(f'<rect x="{x:.0f}" y="{toit:.0f}" width="3" height="{sol - toit:.0f}" fill="#000" opacity=".18"/>')
        x += 22
    out.append('</g>')
    out.append(f'<rect x="{hx + hw * .3:.0f}" y="{sol - 260:.0f}" width="{hw * .4:.0f}" height="260" fill="#1d2b23"/>')
    out.append(f'<rect x="0" y="{sol:.0f}" width="{w}" height="{h - sol:.0f}" fill="#9a9184"/>')
    # palettes de sacs
    sacs = ["#e7dcc6", "#d8c9a8", "#c94f2b", "#2f6b4a"]
    px = w * r.uniform(.08, .2)
    for p in range(2):
        teinte = r.choice(sacs)
        bx, by = px + p * 260, sol + 60
        out.append(f'<rect x="{bx:.0f}" y="{by:.0f}" width="220" height="16" fill="#b08a5a"/>')
        for rang in range(5):
            for s in range(3):
                out.append(f'<rect x="{bx + 4 + s * 72:.0f}" y="{by - 34 - rang * 34:.0f}" width="68" height="32" rx="8" '
                           f'fill="{_mix(teinte, "#000000", r.uniform(0, .12))}"/>')
    # stère de bûches
    sx, sy, R = w * r.uniform(.66, .74), sol + 76, 19
    for rang in range(6):
        for k in range(7):
            cx, cy = sx + k * R * 2 + (R if rang % 2 else 0), sy - rang * R * 1.75
            out.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{R:.0f}" fill="{_mix("#c58a4f", "#5a3216", r.uniform(0, .5))}"/>')
            out.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{R * .35:.0f}" fill="none" stroke="#7a4a22" stroke-opacity=".5"/>')
    out.append(f'<rect width="{w}" height="{h}" fill="url(#vig)"/>')
    return defs, out


MOTIFS = {"poele-bois": _une_poele_bois, "poele-pellets": _une_poele_pellets, "fournisseur": _une_fournisseur}
