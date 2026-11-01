"""Images du site : images à la une générées, photos recadrées, envoi dans la médiathèque.

Motifs disponibles pour l'image à la une (site.json → "motif" de chaque verticale) :
bois, pellets, ramonage, local (collines boisées), formes (abstrait, aux couleurs du site).
Un site peut ajouter les siens dans <site>/tools/motifs.py : un dict MOTIFS {nom: fonction(r, w, h)}.

- une image à la une est un dessin SVG sans aucun texte, tiré du slug (même slug, même image),
  rendu par sips (macOS) puis compressé par cwebp ;
- une photo est redressée selon le sens de prise de vue du téléphone, recadrée au centre et
  réduite par sips ; cwebp n'en garde aucune métadonnée : ni appareil, ni date, ni position GPS.

Usage :
  python3 tools/images.py une <slug>          génère media/une/<slug>.webp
  python3 tools/images.py photo <fichier>     prépare media/photos/<nom>.webp
"""
import os, re, sys, math, random, hashlib, subprocess, tempfile, shutil, json, html

import config
from config import ROOT
MEDIA = os.path.join(ROOT, "media")
REGISTRE = os.path.join(ROOT, "autopilote", "medias.json")
SRGB = "/System/Library/ColorSync/Profiles/sRGB Profile.icc"

UNE = (1600, 900)      # 16:9, au-dessus des 1 200 px demandés par Discover
PHOTO = (1600, 1067)   # 3:2 pleine largeur du texte
# Formats d'image dans un article : préparés au double de leur taille d'affichage (écrans haute définition)
FORMATS = {"600": (1200, 800),        # image descriptive 600 × 400, centrée dans le texte
           "banniere": (1800, 600),   # bannière 3:1 qui ouvre ou coupe une section
           "large": PHOTO}            # pleine largeur du texte
FORMAT_DEFAUT = "600"
QUALITE = 78


# ---------------------------------------------------------------- rendu
def _webp(png, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    subprocess.run(["cwebp", "-quiet", "-q", str(QUALITE), "-m", "6", "-metadata", "none", png, "-o", dest],
                   check=True)
    return dest


POIDS_MAX = 100 * 1024   # cible des images d'article


def _webp_leger(png, dest, poids_max=POIDS_MAX):
    """WebP sous `poids_max` : qualité 78, puis 72, 66, 60 ; si ça ne suffit pas, image réduite de 15 % et on recommence."""
    for _ in range(3):
        for q in (QUALITE, 72, 66, 60):
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            subprocess.run(["cwebp", "-quiet", "-q", str(q), "-m", "6", "-metadata", "none", png, "-o", dest], check=True)
            if os.path.getsize(dest) <= poids_max:
                return dest
        w, h = int(_sips_prop(png, "pixelWidth")), int(_sips_prop(png, "pixelHeight"))
        subprocess.run(["sips", "-z", str(round(h * .85)), str(round(w * .85)), png], check=True, capture_output=True)
    return dest


# ---------------------------------------------------------------- images à la une
def _rng(slug):
    return random.Random(int(hashlib.sha256(slug.encode()).hexdigest()[:12], 16))


def _mix(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(a, b))


def _une_bois(r, w, h):
    """Un tas de bûches vu de face : les sections, leurs cernes et leurs fentes de séchage."""
    fond = "#1c120b"
    ecorce = ["#4a2e1b", "#3d2616", "#5a3a22", "#4f3320", "#34200f"]
    aubier = ["#e9c89a", "#e2bb86", "#edd2a8", "#dcb27a", "#e6c08c"]
    coeur = ["#c98f55", "#b87a42", "#d39c62", "#a86a36", "#bf8448"]
    out = [f'<rect width="{w}" height="{h}" fill="{fond}"/>']
    rmoy = r.uniform(78, 105)
    buches = []
    y, rang = h + rmoy * 0.3, 0
    while y > -rmoy * 1.2:
        x = -r.uniform(0, rmoy) + (rmoy * 0.9 if rang % 2 else 0)
        while x < w + rmoy:
            R = rmoy * r.uniform(0.7, 1.15)
            buches.append((x + R, y + r.uniform(-10, 10), R))
            x += R * 2 + r.uniform(-6, 4)
        y -= rmoy * 1.62
        rang += 1
    r.shuffle(buches)
    for cx, cy, R in buches:
        i = r.randrange(5)
        out.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{R:.0f}" fill="{ecorce[i]}"/>')
        out.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{R * r.uniform(.84, .9):.0f}" fill="{aubier[r.randrange(5)]}"/>')
        ox, oy = r.uniform(-0.18, 0.18) * R, r.uniform(-0.18, 0.18) * R
        out.append(f'<circle cx="{cx + ox * .5:.0f}" cy="{cy + oy * .5:.0f}" r="{R * r.uniform(.4, .62):.0f}" '
                   f'fill="{coeur[r.randrange(5)]}" opacity=".7"/>')
        for k in range(1, r.randint(8, 14)):
            rr = R * 0.84 * k / 14
            out.append(f'<circle cx="{cx + ox * k / 14:.1f}" cy="{cy + oy * k / 14:.1f}" r="{rr:.1f}" fill="none" '
                       f'stroke="#7a4e2a" stroke-opacity="{r.uniform(.2, .4):.2f}" stroke-width="{r.uniform(.6, 1.6):.1f}"/>')
        for _ in range(r.choice([0, 0, 1, 1, 2])):
            # fente de séchage : large à l'écorce, qui s'affine vers le cœur
            a = r.uniform(0, 2 * math.pi)
            d0, d1 = r.uniform(.3, .55), .87
            ep = r.uniform(2.5, 5)
            px, py = -math.sin(a) * ep, math.cos(a) * ep
            x0, y0 = cx + math.cos(a) * R * d0, cy + math.sin(a) * R * d0
            x1, y1 = cx + math.cos(a) * R * d1, cy + math.sin(a) * R * d1
            out.append(f'<path d="M{x0:.0f} {y0:.0f} L{x1 + px:.0f} {y1 + py:.0f} L{x1 - px:.0f} {y1 - py:.0f}Z" '
                       f'fill="#3a2212" opacity=".75"/>')
    out.append(f'<rect width="{w}" height="{h}" fill="url(#lum)"/>')
    out.append(f'<rect width="{w}" height="{h}" fill="url(#vig)"/>')
    defs = ('<linearGradient id="lum" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffd9a0" stop-opacity=".12"/>'
            '<stop offset="1" stop-color="#000" stop-opacity=".25"/></linearGradient>'
            '<radialGradient id="vig" cx="50%" cy="45%" r="75%"><stop offset="55%" stop-color="#000" stop-opacity="0"/>'
            '<stop offset="100%" stop-color="#000" stop-opacity=".5"/></radialGradient>')
    return defs, out


def _une_pellets(r, w, h):
    """Un tas de granulés vu de près : dense, avec une bande nette et le reste flou."""
    teintes = ["#c89a5c", "#b98748", "#d6ac6f", "#a8773d", "#caa06a", "#bd8f55"]
    defs = ('<filter id="flou" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4"/></filter>'
            '<filter id="flou2" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="1.6"/></filter>'
            '<linearGradient id="lum" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".3"/>'
            '<stop offset=".5" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".25"/></linearGradient>'
            '<radialGradient id="vig" cx="50%" cy="50%" r="75%"><stop offset="50%" stop-color="#000" stop-opacity="0"/>'
            '<stop offset="100%" stop-color="#000" stop-opacity=".55"/></radialGradient>')
    out = [f'<rect width="{w}" height="{h}" fill="#2b1d10"/>']
    net = r.uniform(0.35, 0.65) * h
    echelle = r.uniform(1.5, 1.9)
    for couche in range(5):
        n = 900 if couche < 4 else 500
        for _ in range(n):
            x, y = r.uniform(-60, w + 60), r.uniform(-60, h + 60)
            dist = abs(y - net) / h
            filtre = "flou" if dist > 0.3 else ("flou2" if dist > 0.16 else "")
            L, d = r.uniform(30, 58) * echelle, r.uniform(14, 17) * echelle
            a = r.uniform(0, 180)
            c = teintes[r.randrange(6)]
            if couche < 3:
                c = _mix(c, "#000000", .35 - couche * .1)
            g = f' filter="url(#{filtre})"' if filtre else ""
            out.append(f'<g transform="translate({x:.0f} {y:.0f}) rotate({a:.0f})"{g}>'
                       f'<rect x="{-L / 2:.1f}" y="{-d / 2:.1f}" width="{L:.1f}" height="{d:.1f}" rx="{d / 2.2:.1f}" fill="{c}"/>'
                       f'<rect x="{-L / 2:.1f}" y="{-d / 2:.1f}" width="{L:.1f}" height="{d:.1f}" rx="{d / 2.2:.1f}" fill="url(#lum)"/>'
                       f'<ellipse cx="{L / 2 - d / 3.4:.1f}" cy="0" rx="{d / 3.4:.1f}" ry="{d / 2.1:.1f}" fill="{_mix(c, "#000000", .22)}"/>'
                       f'<line x1="{-L / 2 + 6:.1f}" y1="{-d / 5:.1f}" x2="{L / 2 - 10:.1f}" y2="{-d / 6:.1f}" '
                       f'stroke="{_mix(c, "#000000", .3)}" stroke-width="1" stroke-opacity=".5"/></g>')
    out.append(f'<rect width="{w}" height="{h}" fill="url(#vig)"/>')
    return defs, out


def _une_ramonage(r, w, h):
    """Un conduit de briques dans la nuit, la fumée qui s'en échappe."""
    defs = ('<linearGradient id="ciel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b2433"/>'
            '<stop offset="1" stop-color="#3d3a3f"/></linearGradient>'
            '<filter id="fumee" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="14"/></filter>'
            '<radialGradient id="braise" cx="50%" cy="100%" r="60%"><stop offset="0" stop-color="#e0662a" stop-opacity=".55"/>'
            '<stop offset="1" stop-color="#e0662a" stop-opacity="0"/></radialGradient>')
    out = [f'<rect width="{w}" height="{h}" fill="url(#ciel)"/>']
    cx = w * r.choice([0.28, 0.36, 0.64, 0.72])
    cw = r.uniform(170, 230)
    top = h * r.uniform(0.34, 0.46)
    for k in range(9):
        path = [f"M{cx + r.uniform(-30, 30):.0f} {top:.0f}"]
        x, y = cx, top
        for _ in range(5):
            x2, y2 = x + r.uniform(-60, 200) * (1 if cx < w / 2 else -1), y - r.uniform(60, 120)
            path.append(f"Q{(x + x2) / 2 + r.uniform(-80, 80):.0f} {(y + y2) / 2:.0f} {x2:.0f} {y2:.0f}")
            x, y = x2, y2
        out.append(f'<path d="{" ".join(path)}" fill="none" stroke="#b9b6b8" stroke-opacity="{r.uniform(.08, .2):.2f}" '
                   f'stroke-width="{r.uniform(40, 90):.0f}" stroke-linecap="round" filter="url(#fumee)"/>')
    briques = ["#8a3b26", "#7a3322", "#94452d", "#6f2f1f", "#9c4a31"]
    bh, bw = 28, 62
    out.append(f'<rect x="{cx - cw / 2 - 14:.0f}" y="{top - 26:.0f}" width="{cw + 28:.0f}" height="30" fill="#5d5552"/>')
    row, y = 0, top + 4
    while y < h:
        x = cx - cw / 2 - (bw / 2 if row % 2 else 0)
        while x < cx + cw / 2:
            x0, x1 = max(x, cx - cw / 2), min(x + bw, cx + cw / 2)
            if x1 - x0 > 4:
                out.append(f'<rect x="{x0 + 1.5:.0f}" y="{y + 1.5:.0f}" width="{x1 - x0 - 3:.0f}" height="{bh - 3}" '
                           f'fill="{briques[r.randrange(5)]}"/>')
            x += bw
        y += bh
        row += 1
    out.append(f'<rect x="{cx - cw / 2:.0f}" y="{top + 4:.0f}" width="{cw * .22:.0f}" height="{h:.0f}" fill="#000" opacity=".18"/>')
    out.append(f'<rect width="{w}" height="{h}" fill="url(#braise)"/>')
    for _ in range(40):
        out.append(f'<circle cx="{r.uniform(0, w):.0f}" cy="{r.uniform(0, h * .55):.0f}" r="{r.uniform(.6, 1.6):.1f}" '
                   f'fill="#fff" opacity="{r.uniform(.2, .6):.2f}"/>')
    return defs, out


def _une_local(r, w, h):
    """Les collines boisées de l'Ardenne, plan après plan."""
    ciel_h, ciel_b = r.choice([("#f3d9b8", "#f7eee0"), ("#e8cfb4", "#f4ece2"), ("#dfe3dc", "#f3efe6")])
    defs = (f'<linearGradient id="ciel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{ciel_h}"/>'
            f'<stop offset="1" stop-color="{ciel_b}"/></linearGradient>')
    out = [f'<rect width="{w}" height="{h}" fill="url(#ciel)"/>',
           f'<circle cx="{w * r.uniform(.15, .85):.0f}" cy="{h * r.uniform(.18, .3):.0f}" r="{r.uniform(40, 60):.0f}" '
           f'fill="#fbf1de" opacity=".9"/>']
    plans = ["#b7c2b0", "#8ea08a", "#627a63", "#3f5a45", "#233a2c"]
    for i, c in enumerate(plans):
        base = h * (0.42 + i * 0.11)
        pts, x = [f"M0 {h}", f"L0 {base:.0f}"], 0
        amp, per, ph = r.uniform(20, 55), r.uniform(260, 520), r.uniform(0, 6.3)
        crete = []
        while x <= w + 20:
            y = base - amp * math.sin(x / per + ph) - amp * .4 * math.sin(x / per * 2.3 + ph * 1.7)
            crete.append((x, y))
            pts.append(f"L{x:.0f} {y:.0f}")
            x += 20
        pts.append(f"L{w} {h}Z")
        out.append(f'<path d="{" ".join(pts)}" fill="{c}"/>')
        taille = 14 + i * 9
        for (x, y) in crete[::max(1, 3 - i // 2)]:
            if r.random() < 0.8:
                t = taille * r.uniform(.7, 1.3)
                out.append(f'<path d="M{x:.0f} {y - t * 2.2:.0f} L{x - t * .55:.0f} {y + 2:.0f} L{x + t * .55:.0f} {y + 2:.0f}Z" fill="{c}"/>')
    return defs, out


def _une_formes(r, w, h):
    """Motif neutre pour un nouveau site : grands disques et bandes aux couleurs du site."""
    k = config.COULEURS
    fond, accent = k.get("fond_une", "#1f2328"), k["accent"]
    teintes = [accent, k.get("accent_fonce", accent), k.get("fond", "#f5f1ea"), _mix(accent, "#ffffff", .35)]
    defs = ('<radialGradient id="vig" cx="50%" cy="50%" r="75%"><stop offset="50%" stop-color="#000" stop-opacity="0"/>'
            '<stop offset="100%" stop-color="#000" stop-opacity=".45"/></radialGradient>')
    out = [f'<rect width="{w}" height="{h}" fill="{fond}"/>']
    for _ in range(r.randint(5, 9)):
        R = r.uniform(80, 420)
        out.append(f'<circle cx="{r.uniform(0, w):.0f}" cy="{r.uniform(0, h):.0f}" r="{R:.0f}" '
                   f'fill="{r.choice(teintes)}" opacity="{r.uniform(.15, .55):.2f}"/>')
    for _ in range(r.randint(2, 4)):
        y, e = r.uniform(0, h), r.uniform(20, 90)
        out.append(f'<rect x="0" y="{y:.0f}" width="{w}" height="{e:.0f}" fill="{r.choice(teintes)}" opacity="{r.uniform(.1, .3):.2f}" '
                   f'transform="rotate({r.uniform(-12, 12):.1f} {w / 2:.0f} {h / 2:.0f})"/>')
    out.append(f'<rect width="{w}" height="{h}" fill="url(#vig)"/>')
    return defs, out


DESSINS = {"bois": _une_bois, "pellets": _une_pellets, "ramonage": _une_ramonage, "local": _une_local,
           "formes": _une_formes}
_motifs_site = os.path.join(ROOT, "tools", "motifs.py")
if os.path.exists(_motifs_site):
    import importlib.util
    _spec = importlib.util.spec_from_file_location("motifs_site", _motifs_site)
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    DESSINS.update(getattr(_mod, "MOTIFS", {}))


def theme(fm):
    """Motif de l'image à la une : celui de la page locale, de la catégorie, de la page mère, sinon le motif par défaut."""
    if config.est_locale(fm):
        return config.LOCAL["motif"]
    for v in config.VERTICALES:
        if fm.get("categorie") == v["categorie"]:
            return v["motif"]
    for v in config.VERTICALES:
        if fm.get("slug", "") == v["mere"]:
            return v["motif"]
    return config.SITE.get("motif_defaut", "formes")


def svg_une(slug, dessin):
    w, h = UNE
    defs, corps = DESSINS[dessin](_rng(slug), w, h)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<defs>{defs}</defs>{"".join(corps)}</svg>')


def generer_une(slug, dessin):
    """Image à la une du slug, sans texte. Renvoie le chemin du WebP."""
    dest = os.path.join(MEDIA, "une", f"{slug}.webp")
    w, h = UNE
    with tempfile.TemporaryDirectory() as d:
        svg, png = os.path.join(d, "une.svg"), os.path.join(d, "une.png")
        open(svg, "w", encoding="utf-8").write(svg_une(slug, dessin))
        subprocess.run(["sips", "-s", "format", "png", svg, "--out", png], check=True, capture_output=True)
        return _webp(png, dest)


# ---------------------------------------------------------------- photos
def _nom(fichier):
    base = os.path.splitext(os.path.basename(fichier))[0].lower()
    base = re.sub(r"[àâä]", "a", base)
    base = re.sub(r"[éèêë]", "e", base)
    base = re.sub(r"[îï]", "i", base)
    base = re.sub(r"[ôö]", "o", base)
    base = re.sub(r"[ùûü]", "u", base)
    return re.sub(r"[^a-z0-9]+", "-", base).strip("-")


def chemin_photo(fichier, fmt=None):
    """Chemin (relatif au projet) du WebP préparé pour une photo source. Le nom vient du fichier source :
    c'est lui qui part dans la médiathèque, il doit décrire l'image (voir la charte)."""
    suffixe = "" if (fmt or FORMAT_DEFAUT) == FORMAT_DEFAUT else f"-{fmt}"
    return os.path.join("media", "photos", _nom(fichier) + suffixe + ".webp")


ALT_UNE = {"bois": "Illustration : sections de bûches de bois de chauffage empilées",
           "pellets": "Illustration : granulés de bois en vrac, vus de près",
           "ramonage": "Illustration : conduit de cheminée en briques d'où s'échappe la fumée",
           "local": "Illustration : collines boisées",
           "formes": "Illustration abstraite",
           **config.SITE.get("alt_images_une", {})}


def appel_image(interieur):
    """« chemin | légende | alt | format » → (chemin, légende, alt, format). Format : 600, banniere ou large."""
    p = [x.strip() for x in interieur.split("|")] + ["", "", "", ""]
    fmt = p[3] if p[3] in FORMATS else FORMAT_DEFAUT
    return p[0], p[1], p[2], fmt


def photos_article(body):
    """[(source, légende, alt, format)] des photos appelées par ![[…]] dans un article (hors SVG et notes)."""
    visible = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    return [appel_image(m.group(1)) for m in re.finditer(r"^!\[\[(.+?)\]\]\s*$", visible, re.M)
            if not m.group(1).split("|")[0].strip().lower().endswith(".svg")]


def _sips_prop(path, cle):
    r = subprocess.run(["sips", "-g", cle, path], capture_output=True, text=True)
    m = re.search(rf"{cle}:\s*(\S+)", r.stdout)
    return m.group(1) if m else None


def preparer_photo(fichier, taille=PHOTO, fmt=None):
    """Redresse, recadre au centre au format voulu, réduit et convertit une photo. Renvoie le chemin du WebP."""
    src = os.path.join(ROOT, fichier) if not os.path.isabs(fichier) else fichier
    if fmt:
        taille = FORMATS[fmt]
    dest = os.path.join(ROOT, chemin_photo(src, fmt))
    W, H = taille
    with tempfile.TemporaryDirectory() as d:
        png = os.path.join(d, "photo.png")
        subprocess.run(["sips", "-s", "format", "png", "-m", SRGB, src, "--out", png], check=True, capture_output=True)
        rot = {"3": 180, "6": 90, "8": 270}.get(_sips_prop(src, "orientation") or "1")
        if rot:
            subprocess.run(["sips", "-r", str(rot), png], check=True, capture_output=True)
        w, h = int(_sips_prop(png, "pixelWidth")), int(_sips_prop(png, "pixelHeight"))
        if w / h > W / H:
            cw, ch = round(h * W / H), h
        else:
            cw, ch = w, round(w * H / W)
        subprocess.run(["sips", "-c", str(ch), str(cw), png], check=True, capture_output=True)
        if cw > W:
            subprocess.run(["sips", "-z", str(H), str(W), png], check=True, capture_output=True)
        return _webp_leger(png, dest) if fmt else _webp(png, dest)


# ---------------------------------------------------------------- médiathèque
def _empreinte_fichier(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()[:16]


def registre():
    try:
        return json.load(open(REGISTRE, encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def televerser(path, alt, titre=""):
    """Envoie un WebP dans la médiathèque, une seule fois par version du fichier.
    Renvoie {"id", "url", "w", "h"}."""
    import wp
    cle = os.path.relpath(path, ROOT)
    reg = registre()
    emp = _empreinte_fichier(path)
    if reg.get(cle, {}).get("empreinte") == emp:
        m = reg[cle]
        if m.get("alt") != alt:
            wp.api(f"/wp-json/wp/v2/media/{m['id']}", "POST", {"alt_text": alt})
            m["alt"] = alt
            json.dump(reg, open(REGISTRE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        return m
    s, r = wp.envoyer_fichier(path, "image/webp")
    if s not in (200, 201):
        raise RuntimeError(f"envoi de {cle} refusé : HTTP {s} {str(r)[:200]}")
    wp.api(f"/wp-json/wp/v2/media/{r['id']}", "POST", {"alt_text": alt, "title": titre or alt[:80]})
    d = r.get("media_details", {})
    reg[cle] = {"id": r["id"], "url": r["source_url"], "w": d.get("width"), "h": d.get("height"),
                "empreinte": emp, "alt": alt}
    json.dump(reg, open(REGISTRE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return reg[cle]


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) >= 2 and a[0] == "une":
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import wp
        fm, _ = wp.parse_article(os.path.join(ROOT, "articles", f"{a[1]}.md"))
        p = generer_une(a[1], a[2] if len(a) > 2 else theme(fm))
        print(p, f"{os.path.getsize(p) // 1024} Ko")
    elif len(a) >= 2 and a[0] == "photo":
        p = preparer_photo(a[1])
        print(p, f"{os.path.getsize(p) // 1024} Ko")
    else:
        print(__doc__)
