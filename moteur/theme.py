"""Thème du site : un thème en blocs officiel (Twenty Twenty-Five) habillé uniquement par l'API REST.

Le thème lui-même n'est jamais modifié : polices, styles globaux, CSS, template parts et gabarits
sont enregistrés dans la base WordPress. Les sources vivent dans <site>/theme/ :

  styles.json        styles globaux (settings + styles) ; les polices y sont ajoutées à l'envoi
  site.css           CSS du site (cadre + composants des articles), rangé dans les styles globaux
  parts/<nom>.html   template parts (header, footer…)
  templates/<nom>.html  gabarits (single, page, archive, 404…)
  polices/*.woff2    fichiers déclarés dans site.json → theme.polices

Réglages : site.json → "theme": {"slug": "twentytwentyfive", "polices": [{"nom", "slug", "pile", "fichier", "graisse"}]}
(plusieurs graisses statiques : "fichiers": [{"fichier", "graisse"}] à la place de "fichier" et "graisse")

Tant que le thème n'est pas actif, tout est envoyé en aperçu (paramètre wp_theme_preview) :
le site en ligne ne change pas. Réservé aux sessions avec le propriétaire, jamais au pilote.
"""
import os, re, json, uuid, base64, urllib.request, urllib.error

import config
import wp

REGLAGES = config.SITE.get("theme") or {}
SLUG = REGLAGES.get("slug", "twentytwentyfive")
DOSSIER = os.path.join(config.ROOT, "theme")


def actif():
    c, t = wp.api("/wp-json/wp/v2/themes?status=active&_fields=stylesheet")
    return t[0]["stylesheet"] if c == 200 and t else None


def _q(chemin, apercu):
    if not apercu:
        return chemin
    return chemin + ("&" if "?" in chemin else "?") + f"wp_theme_preview={SLUG}"


def _multipart(chemin, champs, fichiers):
    """POST multipart/form-data : champs texte + fichiers {nom: (chemin_local, type)}."""
    borne = uuid.uuid4().hex
    corps = b""
    for k, v in champs.items():
        corps += f'--{borne}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
    for k, (p, mime) in fichiers.items():
        corps += (f'--{borne}\r\nContent-Disposition: form-data; name="{k}"; filename="{os.path.basename(p)}"\r\n'
                  f"Content-Type: {mime}\r\n\r\n").encode() + open(p, "rb").read() + b"\r\n"
    corps += f"--{borne}--\r\n".encode()
    req = urllib.request.Request(f"{wp.URL}{chemin}", data=corps, method="POST")
    req.add_header("Authorization", "Basic " + base64.b64encode(f"{wp.USER}:{wp.PW}".encode()).decode())
    req.add_header("User-Agent", config.USER_AGENT)
    req.add_header("Content-Type", f"multipart/form-data; boundary={borne}")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "null")


# ---------------------------------------------------------------- polices
def polices():
    """Installe les polices dans la bibliothèque de polices de WordPress (une fois) ; renvoie leurs déclarations."""
    c, existantes = wp.api("/wp-json/wp/v2/font-families?per_page=100")
    par_slug = {f["font_family_settings"]["slug"]: f for f in existantes} if c == 200 else {}
    decl = []
    for p in REGLAGES.get("polices", []):
        fam = par_slug.get(p["slug"])
        if not fam:
            reglage = {"name": p["nom"], "slug": p["slug"], "fontFamily": p["pile"]}
            c, fam = wp.api("/wp-json/wp/v2/font-families", "POST", {"font_family_settings": json.dumps(reglage)})
            if c not in (200, 201):
                raise SystemExit(f"Police {p['nom']} refusée ({c}) : {fam}")
            print(f"✔ police {p['nom']} créée")
        c, faces = wp.api(f"/wp-json/wp/v2/font-families/{fam['id']}/font-faces?per_page=100")
        # La liste peut renvoyer les fichiers d'autres familles : on ne garde que ceux de celle-ci.
        faces = [f for f in faces if f.get("parent") == fam["id"]] if c == 200 else []
        # Une police variable : "fichier" + "graisse". Plusieurs graisses statiques : "fichiers": [{"fichier", "graisse"}].
        plusieurs = "fichiers" in p
        fichiers = p["fichiers"] if plusieurs else [{"fichier": p["fichier"], "graisse": p.get("graisse", "400")}]
        decl_faces = []
        for fi in fichiers:
            if plusieurs:
                face = next((f for f in faces if f["font_face_settings"].get("fontWeight") == fi["graisse"]), None)
            else:
                face = faces[0] if faces else None
            if not face:
                reglage = {"fontFamily": p["nom"], "fontWeight": fi["graisse"], "fontStyle": "normal",
                           "fontDisplay": "swap", "src": "file-0"}
                c, face = _multipart(f"/wp-json/wp/v2/font-families/{fam['id']}/font-faces",
                                     {"font_face_settings": json.dumps(reglage)},
                                     {"file-0": (os.path.join(DOSSIER, fi["fichier"]), "font/woff2")})
                if c not in (200, 201):
                    raise SystemExit(f"Fichier de police {fi['fichier']} refusé ({c}) : {face}")
                print(f"✔ police {p['nom']} {fi['graisse']} : fichier envoyé")
            s = face["font_face_settings"]
            src = s["src"] if isinstance(s["src"], list) else [s["src"]]
            decl_faces.append({"fontFamily": p["nom"], "fontWeight": s.get("fontWeight", "400"),
                               "fontStyle": s.get("fontStyle", "normal"), "fontDisplay": "swap", "src": src})
        decl.append({"name": p["nom"], "slug": p["slug"], "fontFamily": p["pile"], "fontFace": decl_faces})
    return decl


# ---------------------------------------------------------------- styles globaux
def styles(apercu, familles):
    c, t = wp.api(_q("/wp-json/wp/v2/themes?status=active&_fields=stylesheet,_links", apercu))
    if c != 200 or not t or t[0]["stylesheet"] != SLUG:
        raise SystemExit(f"Thème {SLUG} introuvable (installé ?)")
    lien = t[0]["_links"]["wp:user-global-styles"][0]["href"]
    gid = lien.rstrip("/").rsplit("/", 1)[1]
    data = json.load(open(os.path.join(DOSSIER, "styles.json"), encoding="utf-8"))
    data.setdefault("settings", {}).setdefault("typography", {})["fontFamilies"] = {"custom": familles}
    css = os.path.join(DOSSIER, "site.css")
    if os.path.exists(css):
        data.setdefault("styles", {})["css"] = open(css, encoding="utf-8").read().strip()
    c, r = wp.api(_q(f"/wp-json/wp/v2/global-styles/{gid}", apercu), "POST",
                  {"settings": data["settings"], "styles": data.get("styles", {})})
    if c != 200:
        raise SystemExit(f"Styles globaux refusés ({c}) : {r}")
    print(f"✔ styles globaux ({len(data.get('styles', {}).get('css', ''))} caractères de CSS)")


# ---------------------------------------------------------------- template parts et gabarits
ZONES = {"header": "header", "footer": "footer"}


def gabarits(apercu):
    for genre, route in (("parts", "template-parts"), ("templates", "templates")):
        d = os.path.join(DOSSIER, genre)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if not f.endswith(".html"):
                continue
            nom = f[:-5]
            contenu = open(os.path.join(d, f), encoding="utf-8").read().strip()
            corps = {"content": contenu}
            if genre == "parts":
                corps["area"] = ZONES.get(nom, "uncategorized")
            ident = f"{SLUG}//{nom}"
            c, _ = wp.api(_q(f"/wp-json/wp/v2/{route}/{ident}?_fields=id", apercu))
            if c == 200:
                c, r = wp.api(_q(f"/wp-json/wp/v2/{route}/{ident}", apercu), "POST", corps)
            else:
                corps.update(slug=nom, title=nom.replace("-", " ").capitalize())
                c, r = wp.api(_q(f"/wp-json/wp/v2/{route}", apercu), "POST", corps)
            print(("✔" if c in (200, 201) else f"⛔ {c}"), f"{genre}/{f}", "" if c in (200, 201) else r)


def retirer(apercu):
    """Remet les gabarits et template parts du thème d'origine (les versions modifiées sont supprimées)."""
    for route in ("template-parts", "templates"):
        c, t = wp.api(_q(f"/wp-json/wp/v2/{route}?context=edit&_fields=id,source", apercu))
        for x in t if c == 200 else []:
            if x["source"] == "custom":
                c2, _ = wp.api(_q(f"/wp-json/wp/v2/{route}/{x['id']}?force=true", apercu), "DELETE")
                print("✔ retiré" if c2 == 200 else f"⛔ {c2}", x["id"])


def etat():
    a = actif()
    apercu = a != SLUG
    print(f"Thème actif : {a} · thème du site : {SLUG}" + (" (préparé en aperçu, pas encore actif)" if apercu else ""))
    for route in ("template-parts", "templates"):
        c, t = wp.api(_q(f"/wp-json/wp/v2/{route}?context=edit&_fields=id,source", apercu))
        perso = [x["id"].split("//")[1] for x in t if x["source"] == "custom"] if c == 200 else []
        print(f"{route} modifiés : {', '.join(perso) or 'aucun'}")


def main(args):
    sous = args[0] if args else "etat"
    apercu = actif() != SLUG
    if sous == "pousser":
        if apercu:
            print(f"{SLUG} n'est pas actif : envoi en aperçu, le site en ligne ne change pas.")
        styles(apercu, polices())
        gabarits(apercu)
    elif sous == "retirer":
        retirer(apercu)
    else:
        etat()
