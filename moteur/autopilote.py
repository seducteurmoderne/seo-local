#!/usr/bin/env python3
"""Pilote automatique d'un site WordPress de contenu (moteur commun, réglages dans site.json)

  python3 tools/autopilote.py etat                 état du site, rattrapage des publications en retard
  python3 tools/autopilote.py suivant              prochain slug de la file d'attente
  python3 tools/autopilote.py verifier <slug>      contrôle qualité de articles/<slug>.md
  python3 tools/autopilote.py publier <slug>       programme l'article à une heure aléatoire
  python3 tools/autopilote.py publier <slug> --brouillon
  python3 tools/autopilote.py publier <slug> --urgent    programme l'article sur le premier créneau, les autres glissent d'un jour
  python3 tools/autopilote.py replanifier [<slug>…]    remet en tête les articles programmés cités, les autres glissent
  python3 tools/autopilote.py bloquer <slug> "raison"
  python3 tools/autopilote.py debloquer <slug>
  python3 tools/autopilote.py maillage             réactive liens et formulaires des articles en ligne
  python3 tools/autopilote.py audit                liens entrants et sortants de chaque page en ligne
  python3 tools/autopilote.py une <slug>           pose l'image à la une d'un article déjà envoyé
  python3 tools/autopilote.py plugin               génère setup/mu-plugins/leads.php (réception des devis)
  python3 tools/autopilote.py brief <slug> [<lien google.be>…]  brief SEO en cascade (variantes, SERP, IA lecteur + concurrents, critique)
  python3 tools/autopilote.py serp <slug> <url>…     analyse les 10 premiers résultats Google → briefs/<slug>.md
  python3 tools/autopilote.py photos chercher|prendre …  photos libres (Pixabay, Openverse, Commons) : voir moteur/photos.py
  python3 tools/autopilote.py modele <slug>         crée articles/<slug>.md depuis le modèle de page locale (articles/_modeles/)
  python3 tools/autopilote.py theme [pousser|retirer]  habillage du thème (session avec le propriétaire, jamais le pilote)
"""
import sys, os, re, json, csv, random, urllib.request
import datetime as dt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config
import wp
import images
import prix

ROOT = wp.ROOT
ART = os.path.join(ROOT, "articles")
AP = os.path.join(ROOT, "autopilote")
ETAT = os.path.join(AP, "etat.json")
JOURNAL = os.path.join(AP, "journal.md")
FILE = os.path.join(AP, "file-attente.txt")
SITEMAP = os.path.join(ROOT, "strategie", "sitemap-urls.csv")
UTC = dt.timezone.utc
MERES = config.CATEGORIE_MERE
PUB = config.PUBLICATION
STATUTS = {"publish": "publié", "future": "planifié", "draft": "brouillon", "pending": "en attente"}

try:
    from zoneinfo import ZoneInfo
    BXL = ZoneInfo(config.FUSEAU)
except Exception:
    BXL = None


def to_bxl(d):
    if BXL:
        return d.astimezone(BXL)
    return d.astimezone(dt.timezone(dt.timedelta(hours=2 if 3 < d.month < 11 else 1)))


def now():
    return dt.datetime.now(UTC)


def parse_gmt(s):
    return dt.datetime.fromisoformat(s).replace(tzinfo=UTC)


def fmt_bxl(d):
    return to_bxl(d).strftime("%d/%m à %H:%M")


# ---------------------------------------------------------------- état local
def load_etat():
    if os.path.exists(ETAT):
        with open(ETAT, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_etat(e):
    with open(ETAT, "w", encoding="utf-8") as f:
        json.dump(e, f, ensure_ascii=False, indent=2)


def journal(msg):
    stamp = to_bxl(now()).strftime("%Y-%m-%d %H:%M")
    with open(JOURNAL, "a", encoding="utf-8") as f:
        f.write(f"- {stamp} — {msg}\n")


def maj_sitemap(slug, statut):
    with open(SITEMAP, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    fields = list(rows[0].keys())
    for r in rows:
        if r["url"].strip("/") == slug:
            r["statut"] = statut
    with open(SITEMAP, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def file_attente():
    out = []
    with open(FILE, encoding="utf-8") as f:
        for line in f:
            line = line.split("#")[0].strip()
            if line:
                out.append(line.split()[0])
    return out


# ---------------------------------------------------------------- WordPress
def fetch(kind):
    s, items = wp.api(f"/wp-json/wp/v2/{kind}?per_page=100&status=any&context=edit")
    if s != 200:
        code = items.get("code") if isinstance(items, dict) else ""
        raise SystemExit(f"ERREUR API ({kind}) : HTTP {s} {code} — connexion WordPress refusée ou site injoignable")
    return items


def live_paths(posts, pages):
    live = {"/"}
    for it in posts + pages:
        if it["status"] == "publish":
            live.add(f"/{it['slug']}/")
    return live


POLITIQUE = config.FORM["politique"]


def formulaires_actifs(live):
    """(actifs, plugin présent, politique en ligne). Pas de formulaire sans les deux."""
    s, _ = wp.api(config.FORM["endpoint"])
    return (s == 200 and POLITIQUE in live), s == 200, POLITIQUE in live


def categories():
    s, cats = wp.api("/wp-json/wp/v2/categories?per_page=100")
    return {c["name"]: c["id"] for c in cats}


def liens_homepage():
    try:
        req = urllib.request.Request(wp.URL + "/", headers={"User-Agent": "Mozilla/5.0"})
        h = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
    except Exception:
        return None
    # Liens absolus vers le site (avec ou sans www) et liens relatifs (« /slug/ »), que les thèmes en blocs emploient
    hote = re.escape(re.sub(r"^https?://(www\.)?", "", wp.URL.rstrip("/")))
    chemins = re.findall(r'href="(?:https?://(?:www\.)?' + hote + r')?(/[^/"#?][^"#?]*)"', h)
    return len({c for c in chemins if not re.search(r"/(wp-|feed|comments|xmlrpc)", c)})


def rattrapage(posts):
    """Publie les articles programmés dont l'heure est passée (le cron WordPress dépend des visites)."""
    faits = []
    for p in posts:
        if p["status"] == "future" and parse_gmt(p["date_gmt"]) < now() - dt.timedelta(minutes=10):
            s, _ = wp.api(f"/wp-json/wp/v2/{p['type']}s/{p['id']}", "POST", {"status": "publish"})
            if s == 200:
                faits.append(p["slug"])
                p["status"] = "publish"
    try:
        urllib.request.urlopen(urllib.request.Request(wp.URL + "/wp-cron.php", headers={"User-Agent": "Mozilla/5.0"}), timeout=20).read()
    except Exception:
        pass
    return faits


def synchroniser(etat, posts, pages):
    par_slug = {p["slug"]: p for p in posts + pages}
    for slug, e in etat.items():
        p = par_slug.get(slug)
        if p and e.get("statut") != "bloqué":
            e["statut"] = STATUTS.get(p["status"], p["status"])
            e["date_gmt"] = p["date_gmt"]


def suivant(etat, posts, pages):
    wp_statut = {p["slug"]: p["status"] for p in posts + pages}
    for slug in file_attente():
        e = etat.get(slug, {})
        if e.get("statut") in ("publié", "planifié", "bloqué") or e.get("manuel"):
            continue
        if slug not in etat and wp_statut.get(slug) in ("publish", "future"):
            continue
        return slug
    return None


# ---------------------------------------------------------------- contrôle qualité
REMPLISSAGE = ["tout se joue", "le geste est court", "un mot sur", "c'est le moment de", "profitez-en pour",
               "concrètement,", "la bonne nouvelle", "il faut savoir que", "à noter que", "il convient de",
               "force est de constater", "plongeons", "discrètement", "n'hésitez pas", "dans cet article",
               "en conclusion", "en résumé", "il est important de noter"] + config.SITE.get("formules_bannies_en_plus", [])


MOTS_VIDES = {"de", "du", "des", "le", "la", "les", "un", "une", "et", "ou", "a", "au", "aux", "en", "pour", "par",
              "sur", "dans", "avec", "son", "sa", "ses", "mon", "ma", "mes", "quel", "quelle", "quels", "quelles",
              "comment", "combien", "est", "ce", "que", "qui", "d", "l"}


def _termes(texte):
    t = texte.lower()
    for a, b in (("àâä", "a"), ("éèêë", "e"), ("îï", "i"), ("ôö", "o"), ("ùûü", "u"), ("ç", "c")):
        t = re.sub(f"[{a}]", b, t)
    return {m[:5] for m in re.findall(r"[a-z0-9]+", t) if m not in MOTS_VIDES and len(m) > 1}


def h2_cibles(fm, visible):
    """(H2 qui reprennent la requête cible, H2 hors FAQ). Une H2 compte si elle contient au moins
    la moitié des termes de la requête (radicaux de 5 lettres, mots vides exclus)."""
    cible = _termes(fm.get("requete_cible", ""))
    h2 = [h for h in re.findall(r"^##\s+(.+)$", visible, re.M) if not re.match(r"(Questions fréquentes|FAQ)", h)]
    if not cible:
        return [], h2
    return [h for h in h2 if len(cible & _termes(h)) * 2 >= len(cible)], h2


def verifier(slug):
    path = os.path.join(ART, f"{slug}.md")
    bloq, avert = [], []
    if not os.path.exists(path):
        return [f"fichier absent : articles/{slug}.md"], []
    try:
        fm, body = wp.parse_article(path)
        fm = prix.front_matter(fm)
    except Exception as e:
        return [f"front-matter illisible : {e}"], []
    visible = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    faux = prix.inconnus(visible)
    if faux:
        bloq.append(f"prix dynamiques inconnus de prix/releves.json : {', '.join(faux)}")
    body = prix.remplacer(body)
    visible = prix.remplacer(visible)

    for k in ("slug", "title_seo", "meta_description", "h1", "requete_cible"):
        if not fm.get(k):
            bloq.append(f"front-matter : `{k}` manquant")
    if fm.get("slug") and fm["slug"] != os.path.basename(slug):
        bloq.append(f"le slug du front-matter ({fm['slug']}) ne correspond pas au nom du fichier")
    if fm.get("type") != "page" and not fm.get("categorie"):
        bloq.append("front-matter : `categorie` manquante")
    t = fm.get("title_seo", "")
    if len(t) > 65:
        bloq.append(f"title_seo trop long ({len(t)} car., cible ≤ 60)")
    elif len(t) > 60:
        avert.append(f"title_seo à {len(t)} car. (cible ≤ 60)")
    d = fm.get("meta_description", "")
    if d and not 70 <= len(d) <= 170:
        bloq.append(f"meta_description à {len(d)} car. (cible 120-160)")
    elif d and not 120 <= len(d) <= 160:
        avert.append(f"meta_description à {len(d)} car. (cible 120-160)")

    n = visible.count(wp.MARQUEUR)
    if n:
        bloq.append(f"{n} marqueur(s) {wp.MARQUEUR} restant(s) : sourcer le fait ou le retirer")
    if re.search(r"^##[^#].*\n(?:\s*\n)*###", visible, re.M):
        bloq.append("un H2 est directement suivi d'un H3 : paragraphe de transition requis")

    listes, dedans, bloc = 0, False, False
    for l in visible.split("\n"):
        if l.strip().startswith("::"):
            bloc = True  # les lignes d'un composant (::avantages, ::checklist…) ne sont pas des listes
            continue
        if bloc:
            bloc = bool(l.strip())
            continue
        if l.lstrip().startswith(">"):
            dedans = False
            continue
        est = bool(re.match(r"^\s*(- |\d+\. )\S", l))
        if est and not dedans:
            listes += 1
        dedans = est
    if listes > 2:
        bloq.append(f"{listes} listes hors encadré (à puces ou numérotées : 2 maximum, idéalement 1)")
    elif listes == 2:
        avert.append("2 listes : vérifier que la seconde est indispensable")

    low = visible.lower()
    for f_ in REMPLISSAGE:
        if f_ in low:
            bloq.append(f"formule de remplissage : « {f_} »")
    for m in re.finditer(r"n['’]est pas [^.\n]{1,90}?[,:;] c['’]est", visible):
        avert.append(f"construction « n'est pas X, c'est Y » : « …{m.group(0)[:60]}… »")
    if fm.get("type") != "page" and "En bref" not in visible:
        avert.append("pas d'encadré « En bref »")
    mots = len(re.sub(r"[#>*|`]", " ", visible).split())
    if mots < 600 and fm.get("type") != "page":
        avert.append(f"article court ({mots} mots)")
    for svg in re.findall(r"!\[\[([^\]|]+)", visible):
        if not os.path.exists(os.path.join(ROOT, svg.strip())):
            bloq.append(f"schéma introuvable : {svg.strip()}")
    ok_h2, tous_h2 = h2_cibles(fm, visible)
    if tous_h2 and not ok_h2:
        bloq.append(f"aucune H2 ne reprend la requête cible « {fm.get('requete_cible')} » : reformuler les H2 sur les recherches réelles")
    elif len(tous_h2) >= 3 and len(ok_h2) < 2:
        avert.append(f"une seule H2 reprend la requête cible « {fm.get('requete_cible')} » (2 au moins conseillées)")
    if config.SITE.get("design") == 2 and not (config.SITE.get("auteur") or {}).get("nom"):
        avert.append("design v2 sans auteur dans site.json : le cadre auteur n'affichera que les dates")
    if fm.get("schema") == "FAQPage" and len(wp.faq_pairs(visible)) < 2:
        avert.append("schema FAQPage déclaré mais moins de 2 questions détectées")
    if "::cta-fort" not in visible:
        avert.append("pas de CTA fort (::cta-fort)")
    mere = MERES.get(fm.get("categorie"))
    if mere and fm.get("type") != "page":
        pos = visible.find(f"]({mere})")
        if pos < 0:
            bloq.append(f"aucun lien vers la page mère {mere} dans le texte (règle du silo)")
        elif pos > len(visible) / 3:
            avert.append(f"le lien vers la page mère {mere} arrive après le premier tiers de l'article")
    if "::a-lire-aussi" in visible:
        bloq.append("bloc ::a-lire-aussi interdit : les liens internes vont dans les phrases, ancrés sur le sujet de la page cible")
    if re.search(r"^\s*→", visible, re.M):
        bloq.append("ligne de renvoi « → » interdite : intégrer le lien dans une phrase, ancré sur le sujet de la page cible")
    outils = re.findall(r"(?:\]\(|^::(?:boton|ficha)\s+)@([\w.-]+)", visible, re.M)
    inconnus = sorted({o for o in outils if o.lower() not in config.OUTILS})
    if inconnus:
        bloq.append(f"outil inconnu de affiliation.json : {', '.join(inconnus)}")
    ext = re.findall(r"\]\((https?://[^)\s]+)\)", visible)
    if ext:
        bloq.append(f"lien externe dans le texte ({ext[0][:60]}) : une source se cite par son nom, l'URL va dans les notes")
    ancres_vagues = re.findall(r"\[(ici|cliquez ici|en savoir plus|lire la suite|voir|lien)\]\(/", visible, re.I)
    if ancres_vagues:
        bloq.append(f"ancre vague pour un lien interne : {', '.join(sorted(set(ancres_vagues)))}")
    if fm.get("type") == "page" and f"/{slug}/" in MERES.values() and "::guides" not in visible:
        avert.append("page mère sans ::guides : la liste de ses guides ne sera pas générée")
    import seo
    b_seo, a_seo = seo.controler(fm, body, visible, ART, wp.parse_article)
    return bloq + b_seo, avert + a_seo


# ---------------------------------------------------------------- pages locales : modèle
def creer_depuis_modele(slug):
    """Brouillon d'une page locale : le modèle de sa verticale (articles/_modeles/locale-<motif>.md), la ville
    tirée du titre de la sitemap, les données de la ville (setup/03-donnees-locales-a-collecter.csv) en notes."""
    dest = os.path.join(ART, f"{slug}.md")
    if os.path.exists(dest):
        sys.exit(f"articles/{slug}.md existe déjà")
    with open(SITEMAP, encoding="utf-8") as f:
        ligne = next((r for r in csv.DictReader(f) if r["url"].strip("/") == slug), None)
    if not ligne:
        sys.exit(f"/{slug}/ absent de la sitemap")
    if ligne["cluster"] != config.LOCAL.get("cluster", "Ville"):
        sys.exit(f"/{slug}/ n'est pas une page de ville (cluster « {ligne['cluster']} ») : pas de modèle local")
    modeles = os.path.join(ART, "_modeles")
    # locale-<préfixe>.md sert les slugs <préfixe>-<ville> ; « bois » reste l'abréviation de « bois-de-chauffage »
    prefixes = {m: {"bois": "bois-de-chauffage"}.get(m[len("locale-"):-3], m[len("locale-"):-3])
                for m in os.listdir(modeles) if m.startswith("locale-") and m.endswith(".md")}
    modele = next((os.path.join(modeles, m) for m, p in sorted(prefixes.items(), key=lambda x: -len(x[1]))
                   if slug.startswith(p + "-")), None)
    if not modele:
        sys.exit(f"aucun modèle de page locale pour {slug} dans articles/_modeles/")
    ville = re.split(r"\s(?:à|en|au|aux)\s", ligne["titre"])[-1].strip()
    donnees = "(aucune ligne pour cette ville : à collecter avant d'écrire)"
    chemin = os.path.join(ROOT, "setup", "03-donnees-locales-a-collecter.csv")
    if os.path.exists(chemin):
        with open(chemin, encoding="utf-8") as f:
            r = next((r for r in csv.DictReader(f) if r["zone"].strip().lower() == ville.lower()), None)
        if r:
            donnees = "\n".join(f"- {k} : {v}" for k, v in r.items() if v and v.strip() and k != "zone")
    t = open(modele, encoding="utf-8").read()
    for k, v in {"{SLUG}": slug, "{VILLE}": ville, "{ville}": ville.lower(), "{ANNEE}": str(now().year), "{DONNEES}": donnees}.items():
        t = t.replace(k, v)
    open(dest, "w", encoding="utf-8").write(t)
    print(f"✔ articles/{slug}.md créé depuis {os.path.basename(modele)} (ville : {ville})")


# ---------------------------------------------------------------- dates affichées (design v2)
def empreinte_source(body):
    """Empreinte du texte publié de l'article (notes de production exclues) : sert à dater les mises à jour."""
    return wp.empreinte(re.sub(r"<!--.*?-->", "", body, flags=re.S).strip())


def suivre_modification(e, body):
    """Note la date du jour quand le texte de l'article a changé depuis le dernier envoi."""
    emp = empreinte_source(body)
    if e.get("empreinte_source") and e["empreinte_source"] != emp:
        e["modifie_le"] = now().isoformat(timespec="seconds")
    e["empreinte_source"] = emp


def meta_dates(fm, e, date_gmt):
    """Dates du cadre auteur, à l'heure locale du site."""
    mod = None
    if fm.get("mis_a_jour"):
        mod = dt.datetime.fromisoformat(fm["mis_a_jour"]).replace(tzinfo=UTC)
    elif e.get("modifie_le"):
        mod = dt.datetime.fromisoformat(e["modifie_le"])
    return {"publication": to_bxl(parse_gmt(date_gmt)) if date_gmt else None,
            "modification": to_bxl(mod) if mod else None}


# ---------------------------------------------------------------- images
def envoyer_photos(body):
    """Prépare et envoie les photos appelées par l'article, avant le rendu qui les cite."""
    for src, legende, alt, fmt in images.photos_article(body):
        images.televerser(images.preparer_photo(src, fmt=fmt), alt or wp._plain(legende))


def image_une(slug, fm):
    """Id médiathèque de l'image à la une : la photo `image_une` du front-matter, sinon l'image générée."""
    if fm.get("image_une"):
        path = images.preparer_photo(fm["image_une"], images.UNE)
        alt = fm.get("image_une_alt") or fm["h1"]
    else:
        dessin = images.theme(fm)
        path, alt = images.generer_une(slug, dessin), images.ALT_UNE[dessin]
    m = images.televerser(path, alt)
    # le fichier porte le nom du slug : sans ce renommage, l'image prend le lien d'une page (slug-2)
    wp.api(f"/wp-json/wp/v2/media/{m['id']}", "POST", {"slug": f"{slug}-image-une"})
    return m["id"]


# ---------------------------------------------------------------- publication
def choisir_date(etat, posts):
    """Date de sortie au rythme du site (site.json → "publication") : `par_jour` articles chaque jour de sortie,
    un jour de sortie tous les `tous_les` jours, au hasard entre `heure_debut` et `heure_fin`, jamais avant
    maintenant + `delai_min_heures`. Par défaut, un article par jour, le jour même s'il n'en sort pas déjà un.
    Plusieurs articles le même jour : la fenêtre est découpée en parts égales, une par article."""
    geres = sorted(to_bxl(parse_gmt(p["date_gmt"])) for p in posts
                   if p["slug"] in etat and p["status"] in ("publish", "future"))
    debut, fin = PUB["heure_debut"], PUB["heure_fin"]
    par_jour, tous_les = max(1, int(PUB["par_jour"])), max(1, int(PUB["tous_les"]))
    tot = to_bxl(now() + dt.timedelta(hours=PUB["delai_min_heures"]))
    jour = tot.date()
    if geres:
        dernier = geres[-1].date()
        complet = sum(g.date() == dernier for g in geres) >= par_jour
        jour = max(jour, dernier + dt.timedelta(days=tous_les) if complet else dernier)
    part = dt.timedelta(hours=fin - debut) / par_jour
    while True:
        deja = [g for g in geres if g.date() == jour]
        ouverture = tot.replace(year=jour.year, month=jour.month, day=jour.day, hour=debut, minute=0, second=0,
                                microsecond=0)
        for k in range(len(deja), par_jour):
            a = max(ouverture + k * part, tot, *(g + dt.timedelta(minutes=1) for g in deja))
            b = ouverture + (k + 1) * part
            if a < b:
                minutes = max(0, int((b - a).total_seconds() // 60) - 1)
                d = (a + dt.timedelta(minutes=random.randint(0, minutes))).astimezone(UTC)
                return d.replace(second=random.randint(0, 59), microsecond=0)
        jour += dt.timedelta(days=tous_les if deja else 1)


def publier(slug, brouillon=False):
    bloq, avert = verifier(slug)
    if bloq and not brouillon:
        print("⛔ Publication refusée :")
        for b in bloq:
            print("   -", b)
        sys.exit(2)
    fm, body = wp.parse_article(os.path.join(ART, f"{slug}.md"))
    fm = prix.front_matter(fm)
    posts, pages = fetch("posts"), fetch("pages")
    etat = load_etat()
    live = live_paths(posts, pages)
    kind = "pages" if fm.get("type") == "page" else "posts"
    envoyer_photos(body)
    existant = next((p for p in (pages if kind == "pages" else posts) if p["slug"] == slug), None)
    e = etat.get(slug, {})
    if existant and existant["status"] in ("publish", "future"):
        date_sortie = existant["date_gmt"]
    elif brouillon:
        date_sortie = None
    else:
        date_sortie = choisir_date(etat, posts + pages).strftime("%Y-%m-%dT%H:%M:%S")
    suivre_modification(e, body)
    contenu = wp.render(body, live, fm, formulaires_actifs(live)[0], meta_dates(fm, e, date_sortie))

    if existant and e.get("empreinte_contenu") and wp.empreinte(existant["content"]["raw"]) != e["empreinte_contenu"]:
        e["manuel"] = True
        etat[slug] = e
        save_etat(etat)
        journal(f"`{slug}` a été modifié à la main dans WordPress — laissé tel quel")
        print("⛔ Article modifié à la main dans WordPress depuis mon dernier envoi : je n'y touche pas.")
        sys.exit(3)

    payload = {"title": fm["h1"], "slug": slug, "content": contenu, "excerpt": fm["meta_description"],
               "meta": {"_yoast_wpseo_title": fm["title_seo"],
                        "_yoast_wpseo_metadesc": fm["meta_description"],
                        "_yoast_wpseo_focuskw": fm["requete_cible"]}}
    if not existant or not existant.get("featured_media"):
        payload["featured_media"] = image_une(slug, fm)
    if kind == "posts":
        cats = categories()
        if fm["categorie"] not in cats:
            sys.exit(f"Catégorie inconnue dans WordPress : {fm['categorie']}")
        payload["categories"] = [cats[fm["categorie"]]]
    if existant and existant["status"] in ("publish", "future"):
        pass  # mise à jour sans toucher au statut ni à la date
    elif brouillon:
        payload["status"] = "draft"
    else:
        payload["status"] = "future"
        payload["date_gmt"] = date_sortie

    path = f"/wp-json/wp/v2/{kind}" + (f"/{existant['id']}" if existant else "")
    s, r = wp.api(path, "POST", payload)
    if s not in (200, 201):
        sys.exit(f"ERREUR publication : HTTP {s} {json.dumps(r, ensure_ascii=False)[:300] if r else ''}")
    if payload.get("featured_media"):
        rafraichir_yoast(kind, r["id"], payload["featured_media"])
    if r.get("meta", {}).get("_yoast_wpseo_title") != fm["title_seo"]:
        print("⚠️ Le title Yoast n'a pas été enregistré (mu-plugin absent ?)")

    statut = STATUTS.get(r["status"], r["status"])
    etat[slug] = {"id": r["id"], "type": kind[:-1], "statut": statut, "date_gmt": r["date_gmt"],
                  "empreinte_contenu": wp.empreinte(r["content"]["raw"]), "empreinte_rendu": wp.empreinte(contenu),
                  **{k: e[k] for k in ("empreinte_source", "modifie_le") if k in e}}
    save_etat(etat)
    maj_sitemap(slug, statut)
    quand = fmt_bxl(parse_gmt(r["date_gmt"]))
    journal(f"`{slug}` {statut}" + (f", sortie le {quand}" if statut == "planifié" else "")
            + (f" · {len(avert)} avertissement(s)" if avert else ""))
    print(f"✔ {slug} → {statut}" + (f", sortie le {quand} (heure locale)" if statut == "planifié" else ""))
    print(f"  {wp.URL}/wp-admin/post.php?post={r['id']}&action=edit")
    for a in avert:
        print("  ⚠", a)


def replanifier(prioritaires=()):
    """Réordonne les articles programmés par le moteur : `prioritaires` d'abord, dans l'ordre donné, puis les autres
    dans leur ordre actuel. Les créneaux (un par jour) ne changent pas : chaque article déplacé prend la date de son
    nouveau créneau, et son cadre auteur est rendu à cette date. Un article repris à la main garde la sienne."""
    prioritaires = list(dict.fromkeys(prioritaires))
    posts, pages = fetch("posts"), fetch("pages")
    etat = load_etat()
    live = live_paths(posts, pages)
    form = formulaires_actifs(live)[0]
    prog = []
    for p in sorted(posts + pages, key=lambda p: p["date_gmt"]):
        e = etat.get(p["slug"])
        if p["status"] != "future" or not e or e.get("manuel") or not os.path.exists(os.path.join(ART, f"{p['slug']}.md")):
            continue
        if e.get("empreinte_contenu") and wp.empreinte(p["content"]["raw"]) != e["empreinte_contenu"]:
            e["manuel"] = True
            journal(f"`{p['slug']}` modifié à la main dans WordPress — laissé à sa date")
            continue
        prog.append(p)
    par_slug = {p["slug"]: p for p in prog}
    absents = [s for s in prioritaires if s not in par_slug]
    if absents:
        save_etat(etat)
        sys.exit(f"Pas programmés par le moteur : {', '.join(absents)} (un article pas encore envoyé : publier <slug> --urgent)")
    creneaux = [p["date_gmt"] for p in prog]
    ordre = [par_slug[s] for s in prioritaires] + [p for p in prog if p["slug"] not in prioritaires]
    deplaces, echecs = [], []
    for p, date in zip(ordre, creneaux):
        if p["date_gmt"] == date:
            continue
        e = etat[p["slug"]]
        fm, body = wp.parse_article(os.path.join(ART, f"{p['slug']}.md"))
        fm = prix.front_matter(fm)
        contenu = wp.render(body, live, fm, form, meta_dates(fm, e, date))
        kind = "pages" if e.get("type") == "page" else "posts"
        s, r = wp.api(f"/wp-json/wp/v2/{kind}/{p['id']}", "POST", {"status": "future", "date_gmt": date, "content": contenu})
        if s != 200:
            echecs.append(p["slug"])
            continue
        e.update(date_gmt=r["date_gmt"], empreinte_contenu=wp.empreinte(r["content"]["raw"]),
                 empreinte_rendu=wp.empreinte(contenu))
        deplaces.append(p["slug"])
    save_etat(etat)
    if deplaces:
        journal(f"replanification : {len(deplaces)} article(s) déplacé(s)"
                + (f", en tête : {', '.join(prioritaires)}" if prioritaires else ""))
    print(f"Replanification : {len(deplaces)} article(s) déplacé(s) sur {len(prog)} programmé(s)")
    for p, date in zip(ordre, creneaux):
        if p["slug"] in echecs:
            print(f"  ⛔ {p['slug']} → refusé par WordPress, reste au {fmt_bxl(parse_gmt(p['date_gmt']))}")
        else:
            print(f"  · {p['slug']} → {fmt_bxl(parse_gmt(date))}")
    if echecs:
        print("Un article refusé garde son ancienne date, qui peut tomber le jour d'un autre : vérifier avec etat.")
        sys.exit(1)


def maillage():
    import serp
    for msg in prix.actualiser(serp.lire):
        journal(msg)
        print(msg)
    posts, pages = fetch("posts"), fetch("pages")
    etat = load_etat()
    live = live_paths(posts, pages)
    par_slug = {p["slug"]: p for p in posts + pages}
    form = formulaires_actifs(live)[0]
    n = 0
    for slug, e in etat.items():
        if e.get("statut") not in ("publié", "planifié") or e.get("manuel"):
            continue
        p = par_slug.get(slug)
        src = os.path.join(ART, f"{slug}.md")
        if not p or not os.path.exists(src):
            continue
        if e.get("empreinte_contenu") and wp.empreinte(p["content"]["raw"]) != e["empreinte_contenu"]:
            e["manuel"] = True
            journal(f"`{slug}` modifié à la main dans WordPress — je ne le mets plus à jour")
            continue
        fm, body = wp.parse_article(src)
        dynamique = any("{{" in str(fm.get(k, "")) for k in ("title_seo", "meta_description", "h1"))
        fm = prix.front_matter(fm)
        if dynamique:
            meta = {"_yoast_wpseo_title": fm["title_seo"], "_yoast_wpseo_metadesc": fm["meta_description"]}
            if wp.empreinte(json.dumps(meta, ensure_ascii=False)) != e.get("empreinte_meta"):
                kind_m = "pages" if e.get("type") == "page" else "posts"
                s_m, _ = wp.api(f"/wp-json/wp/v2/{kind_m}/{p['id']}", "POST", {"meta": meta})
                if s_m == 200:
                    e["empreinte_meta"] = wp.empreinte(json.dumps(meta, ensure_ascii=False))
        envoyer_photos(body)
        suivre_modification(e, body)
        contenu = wp.render(body, live, fm, form, meta_dates(fm, e, p["date_gmt"]))
        if wp.empreinte(contenu) == e.get("empreinte_rendu"):
            continue
        kind = "pages" if e.get("type") == "page" else "posts"
        s, r = wp.api(f"/wp-json/wp/v2/{kind}/{p['id']}", "POST", {"content": contenu})
        if s == 200:
            e["empreinte_contenu"] = wp.empreinte(r["content"]["raw"])
            e["empreinte_rendu"] = wp.empreinte(contenu)
            n += 1
    save_etat(etat)
    print(f"Maillage : {n} article(s) mis à jour")
    if n:
        journal(f"maillage : {n} article(s) relié(s) aux pages publiées depuis")


def audit():
    posts, pages = fetch("posts"), fetch("pages")
    exclus = set(config.SITE.get("audit_exclus", []))
    en_ligne = [p for p in posts + pages if p["status"] == "publish" and p["slug"] not in exclus]
    entrants = {f"/{p['slug']}/": 0 for p in en_ligne}
    sortants = {}
    for p in en_ligne:
        cibles = set(re.findall(r'href="(?:' + re.escape(wp.URL) + r')?(/[^"#?]+/)"', p["content"]["raw"]))
        cibles.discard(f"/{p['slug']}/")
        sortants[f"/{p['slug']}/"] = len(cibles & set(entrants))
        for c in cibles:
            if c in entrants:
                entrants[c] += 1
    print(f"{'Page':<44}{'entrants':>9}{'sortants':>9}")
    for page, n in sorted(entrants.items(), key=lambda x: (x[1], x[0])):
        print(f"{page:<44}{n:>9}{sortants.get(page, 0):>9}")
    orphelins = [k for k, n in entrants.items() if n == 0]
    print(f"\n{len(en_ligne)} page(s) en ligne · {len(orphelins)} sans lien entrant")
    return orphelins


def rafraichir_yoast(kind, pid, mid):
    """Yoast construit ses balises (og:image…) avec un enregistrement de retard : on enregistre une seconde fois."""
    wp.api(f"/wp-json/wp/v2/{kind}/{pid}", "POST", {"featured_media": mid})


def poser_une(slug):
    """Image à la une d'un article déjà envoyé par le pilote. Un article repris à la main n'est pas touché."""
    e = load_etat().get(slug)
    if not e or not e.get("id"):
        sys.exit(f"{slug} : pas envoyé par le pilote")
    if e.get("manuel"):
        sys.exit(f"{slug} : repris à la main, je n'y touche pas")
    fm, _ = wp.parse_article(os.path.join(ART, f"{slug}.md"))
    kind = "pages" if e.get("type") == "page" else "posts"
    mid = image_une(slug, fm)
    s, r = wp.api(f"/wp-json/wp/v2/{kind}/{e['id']}", "POST", {"featured_media": mid})
    if s != 200:
        sys.exit(f"ERREUR : HTTP {s}")
    rafraichir_yoast(kind, e["id"], mid)
    journal(f"`{slug}` : image à la une posée (média {mid})")
    print(f"✔ {slug} : image à la une {mid}")


def _php(s):
    return "'" + str(s).replace("\\", "\\\\").replace("'", "\\'") + "'"


def generer_plugin():
    """Plugin de réception des demandes, tiré de site.json : besoins, champs, code postal, adresse d'envoi."""
    f = config.FORM
    m = re.match(r"^/wp-json/(.+)(/[^/]+)$", f["endpoint"])
    if not m:
        sys.exit("formulaire.endpoint doit être de la forme /wp-json/<espace>/v1/<route>")
    libelles = "array(" + ", ".join(f"{_php(b['cle'])} => {_php(b.get('libelle_court', b['libelle']))}" for b in f["besoins"]) + ")"
    details = "array(\n" + "".join(
        f"        {_php(b['cle'])} => array(" + ", ".join(f"{_php(c[0])} => {_php(c[1])}" for c in b.get("champs", [])) + "),\n"
        for b in f["besoins"]) + "    )"
    cp = f["code_postal"]
    if f.get("mode") == "simple":
        # formulaire simple : pas de code postal, prénom et téléphone obligatoires, prénom ajouté au nom
        controles = ("    $prenom  = $texte('prenom', 80);\n"
                     "    if ($prenom === '') {\n        return bcp_leads_erreur('Indiquez votre prénom.');\n    }\n"
                     "    if ($nom === '') {\n        return bcp_leads_erreur('Indiquez votre nom.');\n    }\n"
                     "    if (!preg_match('/^[+0-9 ().\\/-]{8,}$/', $tel)) {\n"
                     "        return bcp_leads_erreur('Indiquez un numéro de téléphone pour être rappelé.');\n    }\n"
                     "    $nom = trim($prenom . ' ' . $nom);\n"
                     "    $cp = $cp !== '' ? $cp : '—';")
    else:
        controles = ("\n    if (!preg_match('/__CP_REGEX__/', $cp)) {\n"
                     "        return bcp_leads_erreur('__CP_ERREUR__');\n    }")
    modele = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "plugin-leads.php.modele"), encoding="utf-8").read()
    modele = modele.replace("__CONTROLES__", controles)
    php = (modele.replace("__NOM__", config.SITE.get("nom", "")).replace("__NAMESPACE__", m.group(1))
           .replace("__ROUTE__", m.group(2)).replace("__CP_LONGUEUR__", str(cp["longueur"]))
           .replace("__CP_REGEX__", cp["regex"].replace("/", "\\/")).replace("__CP_ERREUR__", cp["erreur"].replace("'", "\\'"))
           .replace("__LIBELLES__", libelles).replace("__DETAILS__", details))
    # messages renvoyés au visiteur : traduits si site.json → formulaire.textes les remplace
    for cle in ("err_expire", "err_trop", "err_nom", "err_prenom", "err_email", "err_tel", "err_accord_serveur", "err_besoin"):
        if wp.TF[cle] != wp.TF_FR[cle]:
            php = php.replace(_php(wp.TF_FR[cle]), _php(wp.TF[cle]))
    dest = os.path.join(ROOT, "setup", "mu-plugins", "leads.php")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, "w", encoding="utf-8").write(php)
    print(f"✔ {os.path.relpath(dest, ROOT)} — à déposer par le propriétaire dans wp-content/mu-plugins/")


def cmd_etat():
    posts, pages = fetch("posts"), fetch("pages")
    faits = rattrapage(posts + pages)
    etat = load_etat()
    synchroniser(etat, posts, pages)
    save_etat(etat)
    live = live_paths(posts, pages)
    liens = liens_homepage()
    prog = sorted((p for p in posts + pages if p["status"] == "future"), key=lambda p: p["date_gmt"])
    print(f"Connexion WordPress OK · {len(live) - 1} contenu(s) en ligne")
    for f_ in faits:
        print(f"  ↻ {f_} était en retard → publié")
        journal(f"`{f_}` publié en rattrapage (cron WordPress en retard)")
    print(f"Programmés : {len(prog)}")
    for p in prog:
        print(f"  · {p['slug']} → {fmt_bxl(parse_gmt(p['date_gmt']))}")
    actif, plugin, politique = formulaires_actifs(live)
    manque = [x for x, ok in (("plugin de réception des demandes", plugin), (f"page {POLITIQUE}", politique)) if not ok]
    print("Formulaires de devis :", "actifs" if actif else "masqués, il manque : " + " + ".join(manque))
    print("Menu homepage :", "inconnu" if liens is None else
          (f"{liens} liens internes" if liens >= 3 else "ABSENT (articles publiés peu découvrables)"))
    bl = [s for s, e in etat.items() if e.get("statut") == "bloqué"]
    if bl:
        print("Bloqués :", " · ".join(f"{s} ({etat[s].get('raison', '')})" for s in bl))
    man = [s for s, e in etat.items() if e.get("manuel")]
    if man:
        print("Repris à la main (plus gérés) :", ", ".join(man))
    print("Suivant :", suivant(etat, posts, pages) or "file d'attente vide")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        sys.exit(0)
    c = a[0]
    if c == "etat":
        cmd_etat()
    elif c == "suivant":
        print(suivant(load_etat(), fetch("posts"), fetch("pages")) or "")
    elif c == "verifier" and len(a) > 1:
        b, w = verifier(a[1])
        for x in b:
            print("⛔", x)
        for x in w:
            print("⚠", x)
        print("OK — publiable" if not b else f"{len(b)} point(s) bloquant(s)")
        sys.exit(1 if b else 0)
    elif c == "publier" and len(a) > 1:
        publier(a[1], "--brouillon" in a)
        if "--urgent" in a and "--brouillon" not in a:
            replanifier([a[1]])
    elif c == "replanifier":
        replanifier(a[1:])
    elif c == "bloquer" and len(a) > 1:
        etat = load_etat()
        e = etat.get(a[1], {})
        e.update(statut="bloqué", raison=" ".join(a[2:]) or "sans raison")
        etat[a[1]] = e
        save_etat(etat)
        maj_sitemap(a[1], "bloqué")
        journal(f"`{a[1]}` bloqué — {e['raison']}")
        print(f"{a[1]} bloqué : {e['raison']}")
    elif c == "debloquer" and len(a) > 1:
        etat = load_etat()
        if a[1] in etat:
            etat[a[1]].update(statut="à faire")
            etat[a[1]].pop("raison", None)
            save_etat(etat)
            maj_sitemap(a[1], "à faire")
        print(f"{a[1]} remis dans la file")
    elif c == "maillage":
        maillage()
    elif c == "audit":
        audit()
    elif c == "une" and len(a) > 1:
        poser_une(a[1])
    elif c == "plugin":
        generer_plugin()
    elif c == "brief" and len(a) > 1:
        import brief
        brief.main(a[1:], wp.parse_article, ART, SITEMAP)
    elif c == "serp" and len(a) > 2:
        import serp
        fm_s = wp.parse_article(os.path.join(ART, f"{a[1]}.md"))[0] if os.path.exists(os.path.join(ART, f"{a[1]}.md")) else {}
        ligne = next((r for r in csv.DictReader(open(SITEMAP, encoding="utf-8")) if r["url"].strip("/") == a[1]), {})
        serp.analyser(a[1], a[2:], fm_s.get("requete_cible") or ligne.get("titre", a[1]))
    elif c == "photos":
        import photos
        photos.main(a[1:])
    elif c == "modele" and len(a) > 1:
        creer_depuis_modele(a[1])
    elif c == "theme":
        import theme
        theme.main(a[1:])
    else:
        print(__doc__)
        sys.exit(1)
