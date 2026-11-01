"""Photos libres pour les articles : chercher, choisir, nommer, créditer.

    python3 tools/autopilote.py photos chercher <slug> "<requête>" ["<autre requête>"…]
        Cherche dans l'ordre : Pixabay (si PIXABAY_API_KEY est dans setup/.env), Openverse, Wikimedia Commons.
        Ne garde que des photos paysage d'au moins 1 200 px, sous licence libre réutilisable
        (Pixabay, CC0, domaine public, CC BY, CC BY-SA). Télécharge les vignettes dans
        briefs/<slug>/photos/ pour qu'on les regarde avant de choisir.

    python3 tools/autopilote.py photos prendre <slug> <n°> <nom-descriptif> "<texte alternatif>" [600|banniere|large]
        Télécharge la photo n° en grand dans photos/<nom-descriptif>.jpg, note son crédit dans
        photos/credits.json et donne la ligne à coller dans l'article (légende avec le crédit).

Les requêtes se font plutôt en anglais (« pellet stove burn pot ») : les banques sont surtout anglophones.
Le choix se fait en regardant les vignettes : le sujet doit être exactement celui de la section.
"""
import os, re, json, html, urllib.request, urllib.parse

import config

UA = {"User-Agent": f"{config.SITE.get('nom', 'site')} (photos libres pour articles)"}
LICENCES = {"cc0": "CC0", "pdm": "Domaine public", "by": "CC BY", "by-sa": "CC BY-SA", "pixabay": "Licence Pixabay"}
MIN_LARGEUR, MIN_RATIO = 1200, 1.25
PAR_SOURCE, MAX_CANDIDATS = 8, 24   # assez pour choisir, sans attendre des minutes


def _get(url, timeout=30):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()


def _texte(h):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", h or "")).split())


def _env(cle):
    chemin = os.path.join(config.ROOT, "setup", ".env")
    if not os.path.exists(chemin):
        return None
    for l in open(chemin, encoding="utf-8"):
        if l.strip().startswith(cle + "="):
            return l.split("=", 1)[1].strip() or None
    return None


# ---------------------------------------------------------------- sources
def pixabay(q):
    cle = _env("PIXABAY_API_KEY")
    if not cle:
        return []
    d = json.loads(_get("https://pixabay.com/api/?" + urllib.parse.urlencode(
        {"key": cle, "q": q, "image_type": "photo", "orientation": "horizontal", "min_width": MIN_LARGEUR,
         "per_page": 20, "safesearch": "true"})))
    return [{"source": "Pixabay", "id": f"pixabay-{h['id']}", "titre": h.get("tags", ""), "auteur": h.get("user", ""),
             "licence": "pixabay", "page": h.get("pageURL", ""), "vignette": h.get("webformatURL") or h.get("previewURL"),
             "grande": h.get("largeImageURL"), "l": h.get("imageWidth", 0), "h": h.get("imageHeight", 0)} for h in d.get("hits", [])]


def openverse(q):
    d = json.loads(_get("https://api.openverse.org/v1/images/?" + urllib.parse.urlencode(
        {"q": q, "license": "cc0,pdm,by,by-sa", "aspect_ratio": "wide", "size": "large", "page_size": 20,
         "mature": "false"})))
    return [{"source": f"Openverse ({r.get('source', '')})", "id": f"openverse-{r['id']}", "titre": r.get("title") or "",
             "auteur": r.get("creator") or "", "licence": r.get("license", ""), "version": r.get("license_version") or "",
             "page": r.get("foreign_landing_url") or "", "vignette": r.get("thumbnail") or r.get("url"),
             "grande": r.get("url"), "l": r.get("width") or 0, "h": r.get("height") or 0} for r in d.get("results", [])]


def commons(q):
    d = json.loads(_get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(
        {"action": "query", "generator": "search", "gsrnamespace": 6, "gsrsearch": f"{q} filetype:bitmap", "gsrlimit": 25,
         "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiurlwidth": 2000, "format": "json"})))
    out = []
    for p in (d.get("query") or {}).get("pages", {}).values():
        ii = (p.get("imageinfo") or [{}])[0]
        m = ii.get("extmetadata", {})
        lic = (m.get("LicenseShortName", {}).get("value") or "").lower()
        code = ("cc0" if "cc0" in lic else "pdm" if "public domain" in lic else "by-sa" if "by-sa" in lic
                else "by" if re.search(r"\bcc by\b", lic) else None)
        if not code:
            continue
        out.append({"source": "Wikimedia Commons", "id": f"commons-{p['pageid']}", "titre": p["title"].replace("File:", ""),
                    "auteur": _texte(m.get("Artist", {}).get("value")), "licence": code,
                    "version": re.sub(r"[^0-9.]", "", lic.split()[-1]) if code in ("by", "by-sa") else "",
                    "page": ii.get("descriptionurl", ""), "vignette": re.sub(r"/\d+px-", "/400px-", ii.get("thumburl") or ""),
                    "grande": ii.get("thumburl") or ii.get("url"),
                    "l": ii.get("width", 0), "h": ii.get("height", 0)})
    return out


SOURCES = [("Pixabay", pixabay), ("Openverse", openverse), ("Wikimedia Commons", commons)]


# ---------------------------------------------------------------- chercher
def chercher(slug, requetes):
    d = os.path.join(config.ROOT, "briefs", slug, "photos")
    os.makedirs(d, exist_ok=True)
    cands, vus = [], set()
    for q in requetes:
        for nom, f in SOURCES:
            try:
                res = f(q)
            except Exception as e:
                print(f"  ↷ {nom} « {q} » : {str(e)[:60]}")
                continue
            gardees = 0
            for c in res:
                if gardees >= PAR_SOURCE or len(cands) >= MAX_CANDIDATS:
                    break
                cle = re.sub(r"\W+", "", (c["titre"] or "").lower())[:40] or c["id"]
                if c["id"] in vus or cle in vus or not c.get("vignette") or c["licence"] not in LICENCES:
                    continue
                if c["l"] < MIN_LARGEUR or (c["h"] and c["l"] / c["h"] < MIN_RATIO):
                    continue
                vus.update({c["id"], cle})
                c["requete"] = q
                cands.append(c)
                gardees += 1
            print(f"  {nom} « {q} » : {gardees} retenue(s) sur {len(res)}")
    for i, c in enumerate(cands, 1):
        c["n"] = i
        for essai in range(3):  # Wikimedia limite les téléchargements rapprochés : on réessaie
            try:
                donnees = _get(c["vignette"])
                if donnees:
                    open(os.path.join(d, f"c{i:02d}.jpg"), "wb").write(donnees)
                    break
            except Exception:
                pass
            import time
            time.sleep(2 * (essai + 1))
        else:
            c["vignette_ko"] = True
    json.dump(cands, open(os.path.join(d, "candidats.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for c in cands:
        print(f"  {c['n']:>2}. [{LICENCES[c['licence']]}] {c['l']}×{c['h']} {c['source']} — {c['titre'][:70]}")
    print(f"✔ {len(cands)} candidate(s) ; vignettes : briefs/{slug}/photos/cNN.jpg")


# ---------------------------------------------------------------- prendre
def nom_fichier(nom):
    t = nom.lower()
    for a, b in (("àâä", "a"), ("éèêë", "e"), ("îï", "i"), ("ôö", "o"), ("ùûü", "u"), ("ç", "c"), ("œ", "oe")):
        t = re.sub(f"[{a}]", b, t)
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def credit(c):
    lic = LICENCES[c["licence"]] + (f" {c['version']}" if c.get("version") else "")
    auteur = c["auteur"] or "auteur inconnu"
    if c["licence"] in ("cc0", "pdm"):
        return f"Photo : {auteur}, {lic}, {c['source'].split(' (')[0]}"
    return f"Photo : {auteur}, {lic}, via {c['source'].split(' (')[0]}"


def prendre(slug, n, nom, alt, fmt="600"):
    d = os.path.join(config.ROOT, "briefs", slug, "photos")
    cands = json.load(open(os.path.join(d, "candidats.json"), encoding="utf-8"))
    c = next((x for x in cands if x["n"] == int(n)), None)
    if not c:
        raise SystemExit(f"candidate n° {n} introuvable")
    fichier = nom_fichier(nom)
    if len(fichier.split("-")) < 3:
        raise SystemExit("nom trop vague : 3 mots au moins, qui décrivent l'image (ex. creuset-poele-a-pellets-encrasse)")
    dest = os.path.join(config.ROOT, "photos", fichier + ".jpg")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, "wb").write(_get(c["grande"], timeout=90))
    reg_path = os.path.join(config.ROOT, "photos", "credits.json")
    reg = json.load(open(reg_path, encoding="utf-8")) if os.path.exists(reg_path) else {}
    reg[fichier + ".jpg"] = {"credit": credit(c), "licence": c["licence"], "page": c["page"], "source": c["source"],
                             "titre": c["titre"], "article": slug}
    json.dump(reg, open(reg_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"✔ photos/{fichier}.jpg ({os.path.getsize(dest) // 1024} Ko) — {credit(c)}")
    print("Ligne à placer dans l'article (complétez la légende) :")
    print(f"![[photos/{fichier}.jpg|<légende> — {credit(c)}|{alt}|{fmt}]]")
    print(f"URL de la page source (notes de production) : {c['page']}")


def main(args):
    if len(args) >= 3 and args[0] == "chercher":
        chercher(args[1], args[2:])
    elif len(args) >= 5 and args[0] == "prendre":
        prendre(args[1], args[2], args[3], args[4], args[5] if len(args) > 5 else "600")
    else:
        print(__doc__)
