"""Contrôle SEO d'un article : brief, titres, lisibilité, couverture de l'intention, doublons entre pages locales.

Appelé par `autopilote.py verifier`. Renvoie (bloquants, avertissements), comme le reste du contrôle.
Les seuils sont réglables par site : site.json → "seo": {...} (voir SEUILS).

Le brief SEO vit dans les notes de production de l'article (commentaire HTML, jamais publié) :

    BRIEF SEO
    Intention : <ce que veut la personne qui tape la requête, et ce qu'elle fera après>
    Format SERP : <ce qui occupe les résultats : guide, liste, tableau, vidéo, page locale, forum…>
    Structure SERP : <ce que les 10 pages ont en commun (briefs/<slug>.md) : sections récurrentes, longueur, formats>
    Variantes : <variante 1> ; <variante 2> ; …
    Termes : <terme 1> ; <terme 2> ; …            (vocabulaire des pages qui se classent)
    Questions :
    - <question réelle 1>
    - <question réelle 2>
    Plan :
    - H2 : <titre>
      - H3 : <titre>

L'analyse des 10 premiers résultats (`autopilote.py serp <slug> <url>…`, au moins 8 pages lues) est exigée,
sauf pour les pages locales d'un site qui pose `seo.brief_locales_facultatif` dans site.json.
"""
import os, re, glob

import config

# Titres FAQ et lignes de sources reconnus, dans la langue du site (site.json → "textes")
_TX = config.SITE.get("textes", {})
FAQ_RE = "|".join(re.escape(t) for t in _TX.get("faq", ["Questions fréquentes", "FAQ"]))
SOURCES_RE = "|".join(r"\*" + re.escape(t) for t in _TX.get("sources", ["Sources"]))

SEUILS = {
    "h2_entite_min": 0.8,        # part des H2 qui nomment l'objet de l'article (bloquant en dessous)
    "paragraphe_avert": 80,      # mots
    "paragraphe_max": 110,       # mots (bloquant au-delà)
    "phrase_longue": 30,         # mots
    "phrases_longues_avert": 0.10,
    "phrases_longues_max": 0.20,  # part des phrases longues (bloquant au-delà)
    "phrase_moyenne_max": 22,    # mots (avertissement au-delà)
    "doublon_avert": 0.35,       # part du texte d'une page locale déjà présente dans une autre
    "doublon_max": 0.50,         # (bloquant au-delà)
    "brief_locales_facultatif": False,  # True : pages locales sans analyse SERP ni brief exigés (avertissement)
    **config.SITE.get("seo", {}),
}

# Titres d'accroche : ils décrivent l'humeur de la section, pas son sujet. Google ne sait pas quoi en faire.
H2_ACCROCHES = [r"\bvraiment\b", r"fausse bonne id[ée]e", r"ne parlent pas", r"\bhistoires?\b", r"^et (apr[eè]s|maintenant)\b",
                r"ce qu['’]il faut (savoir|retenir)\s*$", r"\ble bon r[ée]flexe\b", r"^quel .+ pour quel", r"\bla vraie question\b",
                r"\ben pratique\s*$", r"\ble pi[eè]ge\b", r"\bpas si simple\b", r"\bce que (chacun|chaque fournisseur) d[ée]crit\b",
                r"\bmode d['’]emploi\s*$", r"\bl['’]essentiel\s*$"] + config.SITE.get("h2_accroches_en_plus", [])

MOTS_VIDES = {"de", "du", "des", "le", "la", "les", "un", "une", "et", "ou", "a", "au", "aux", "en", "pour", "par", "sur",
              "dans", "avec", "son", "sa", "ses", "mon", "ma", "mes", "votre", "vos", "quel", "quelle", "quels", "quelles",
              "comment", "combien", "pourquoi", "quand", "est", "ce", "que", "qui", "quoi", "d", "l", "s", "faut", "il",
              "elle", "on", "ne", "pas", "plus", "peut", "doit", "faire", "mon", "y"}


# Mots que les gens emploient l'un pour l'autre : ramenés au même radical
SYNONYMES = {"granu": "pelle"} | config.SITE.get("seo_synonymes", {})


def radicaux(texte):
    """Radicaux de 5 lettres, sans accents ni mots vides : « poêles à pellets » → {poele, pelle}."""
    t = texte.lower()
    for a, b in (("àâä", "a"), ("éèêë", "e"), ("îï", "i"), ("ôö", "o"), ("ùûü", "u"), ("ç", "c"), ("œ", "oe")):
        t = re.sub(f"[{a}]", b, t)
    return {SYNONYMES.get(m[:5], m[:5]) for m in re.findall(r"[a-z0-9]+", t) if m not in MOTS_VIDES and len(m) > 1}


# ---------------------------------------------------------------- brief
def brief(body):
    """Le brief SEO des notes de production : {intention, format, variantes[], termes[], questions[]} ou None."""
    notes = "\n".join(re.findall(r"<!--(.*?)-->", body, re.S))
    m = re.search(r"BRIEF SEO[ \t]*\n((?:[^\n]+\n?)+)", notes)  # le bloc s'arrête à la première ligne vide
    if not m:
        return None
    b = m.group(1)

    def champ(nom):
        mm = re.search(rf"^\s*{nom}\s*:\s*(.+)$", b, re.M | re.I)
        return mm.group(1).strip() if mm else ""

    qs = re.search(r"^\s*Questions\s*:\s*\n((?:\s*-\s.+\n?)+)", b, re.M | re.I)
    plan = re.search(r"^\s*Plan\s*:\s*\n((?:\s*-\s.+\n?)+)", b, re.M | re.I)
    return {"intention": champ("Intention"), "format": champ("Format SERP"),
            "variantes": [x.strip() for x in champ("Variantes").split(";") if x.strip()],
            "termes": [x.strip() for x in champ("Termes").split(";") if x.strip()],
            "questions": [re.sub(r"^\s*-\s*", "", q).strip() for q in qs.group(1).strip().split("\n")] if qs else [],
            "structure": champ("Structure SERP"),
            "plan": [l.rstrip() for l in plan.group(1).rstrip().split("\n")] if plan else []}


# ---------------------------------------------------------------- texte courant
def paragraphes(visible):
    """Paragraphes de texte courant (titres, listes, tableaux, encadrés, blocs :: et images exclus)."""
    out = []
    for p in re.split(r"\n\s*\n", visible):
        p = p.strip()
        if not p or re.match(r"^(#|\||-|>|::|!\[\[|\d+\.\s|" + SOURCES_RE + ")", p):
            continue
        if re.match(r"^\*\*.+\*\*\s*\n", p):  # question de FAQ : la réponse seule compte
            p = p.split("\n", 1)[1]
        out.append(" ".join(p.split()))
    return out


def phrases(texte):
    return [s for s in re.split(r"(?<=[.!?…])\s+(?=[A-ZÀ-Ý«\d])", texte) if s.strip()]


def mots(texte):
    return re.findall(r"[\wÀ-ÿ’'-]+", re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", texte))


# ---------------------------------------------------------------- doublons entre pages locales
def _shingles(texte, n=5):
    m = [w.lower() for w in mots(texte)]
    return {" ".join(m[i:i + n]) for i in range(len(m) - n + 1)}


def doublon_local(fm, visible, art_dir, parse):
    """(part la plus forte du texte déjà présente dans une autre page locale de la même catégorie, slug de cette page)."""
    moi = _shingles(" ".join(paragraphes(visible)))
    if not moi:
        return 0, None
    pire = (0, None)
    for f in glob.glob(os.path.join(art_dir, "*.md")):
        slug = os.path.basename(f)[:-3]
        if slug == fm.get("slug"):
            continue
        try:
            fm2, b2 = parse(f)
        except Exception:
            continue
        if not config.est_locale(fm2) or fm2.get("categorie") != fm.get("categorie"):
            continue
        autre = _shingles(" ".join(paragraphes(re.sub(r"<!--.*?-->", "", b2, flags=re.S))))
        part = len(moi & autre) / len(moi)
        if part > pire[0]:
            pire = (part, slug)
    return pire


# ---------------------------------------------------------------- contrôle
def entites(fm):
    """Ce qu'une H2 doit nommer : le front-matter `entites`, sinon la requête cible ; plus la ville d'une page locale."""
    e = fm.get("entites") or []
    if isinstance(e, str):
        e = [x.strip() for x in e.split(";")]
    e = [x for x in e if x] or [fm.get("requete_cible", "")]
    if fm.get("ville"):
        e.append(fm["ville"])
    return [radicaux(x) for x in e if radicaux(x)]


def nomme_entite(titre, ents):
    r = radicaux(titre)
    return any(e <= r for e in ents)


def controler(fm, body, visible, art_dir, parse):
    bloq, avert = [], []
    S = SEUILS

    # 1. Analyse des résultats Google, puis brief et plan qui en découlent
    # Un site peut dispenser ses pages locales de l'analyse et du brief (site.json → seo.brief_locales_facultatif) :
    # sur les petites communes, il n'y a pas 8 résultats à lire, et le plan vient du modèle local.
    manque_brief = avert if S["brief_locales_facultatif"] and config.est_locale(fm) else bloq
    import serp
    n = serp.pages_analysees(fm.get("slug", ""))
    if n < 8:
        manque_brief.append(f"analyse SERP insuffisante ({n} page(s) lue(s), 8 au moins) : `autopilote.py serp {fm.get('slug')} <url1> … <url10>`")
    b = brief(body)
    if not b:
        manque_brief.append("brief SEO absent des notes de production (bloc « BRIEF SEO » : intention, format SERP, structure SERP, variantes, termes, questions, plan)")
    else:
        manque = [k for k in ("intention", "format", "structure", "variantes", "termes", "questions", "plan") if not b[k]]
        if manque:
            bloq.append(f"brief SEO incomplet : {', '.join(manque)}")
        if b["plan"]:
            # l'objet de l'article est dans tous les titres : il ne compte pas pour reconnaître une section
            commun = set().union(*entites(fm)) if entites(fm) else set()
            sans = lambda r: (r - commun) or r
            prevus = [sans(radicaux(re.sub(r"^\s*-\s*(H[23]\s*:?)?\s*", "", l))) for l in b["plan"]]
            hors = [h for h in re.findall(r"^##\s+(.+)$", visible, re.M) if not re.match(r"(" + FAQ_RE + ")", h)
                    and not any(p and len(p & sans(radicaux(h))) / len(p) >= 0.6 for p in prevus)]
            if hors:
                avert.append("H2 absentes du plan du brief : " + " · ".join(f"« {h} »" for h in hors))
            h2_article = [sans(radicaux(h)) for h in re.findall(r"^##\s+(.+)$", visible, re.M)]
            oubliees = [re.sub(r"^\s*-\s*H2\s*:?\s*", "", l) for l, p in zip(b["plan"], prevus)
                        if re.match(r"^\s*-\s*H2", l) and p and not any(len(p & h) / len(p) >= 0.6 for h in h2_article)]
            if oubliees:
                avert.append("sections du plan absentes de l'article : " + " · ".join(f"« {h} »" for h in oubliees))

    # 2. Titres
    ents = entites(fm)
    if not fm.get("entites"):
        avert.append("front-matter : `entites` absent (l'objet de l'article, ex. « poêle à pellets ») — la requête cible sert d'entité")
    h2 = re.findall(r"^##\s+(.+)$", visible, re.M)
    if h2:
        sans = [h for h in h2 if not nomme_entite(h, ents)]
        part = 1 - len(sans) / len(h2)
        if part < S["h2_entite_min"]:
            bloq.append(f"{len(sans)}/{len(h2)} H2 ne nomment pas l'objet de l'article ({', '.join(fm.get('entites') or [fm.get('requete_cible', '')])}"
                        + (f", {fm['ville']}" if fm.get("ville") else "") + ") : " + " · ".join(f"« {h} »" for h in sans[:4]))
        elif sans:
            avert.append("H2 sans l'objet de l'article : " + " · ".join(f"« {h} »" for h in sans))
    for h in re.findall(r"^#{2,3}\s+(.+)$", visible, re.M):
        for motif in H2_ACCROCHES:
            if re.search(motif, h, re.I):
                bloq.append(f"titre d'accroche, il ne dit pas de quoi parle la section : « {h} »")
                break
        if len(h) > 90:
            avert.append(f"titre long ({len(h)} car.) : « {h[:60]}… »")
    for h in h2:
        if re.search(r"^(Les?|La) (deux|trois|quatre|cinq|six|sept|huit|neuf|dix)\b", h, re.I):
            avert.append(f"nombre en lettres dans une H2 (en chiffres, il attire l'œil dans Google) : « {h} »")

    # 3. Lisibilité
    paras = paragraphes(visible)
    longs = [p for p in paras if len(mots(p)) > S["paragraphe_max"]]
    moyens = [p for p in paras if S["paragraphe_avert"] < len(mots(p)) <= S["paragraphe_max"]]
    if longs:
        bloq.append(f"{len(longs)} paragraphe(s) de plus de {S['paragraphe_max']} mots : « {longs[0][:70]}… »")
    if moyens:
        avert.append(f"{len(moyens)} paragraphe(s) de {S['paragraphe_avert']} à {S['paragraphe_max']} mots : couper en deux idées")
    ph = [s for p in paras for s in phrases(p)]
    if ph:
        lg = [s for s in ph if len(mots(s)) > S["phrase_longue"]]
        part = len(lg) / len(ph)
        moy = sum(len(mots(s)) for s in ph) / len(ph)
        ex = " · ".join(f"« {s[:60]}… » ({len(mots(s))} mots)" for s in lg[:2])
        if part > S["phrases_longues_max"]:
            bloq.append(f"{len(lg)}/{len(ph)} phrases de plus de {S['phrase_longue']} mots ({part:.0%}) : {ex}")
        elif part > S["phrases_longues_avert"]:
            avert.append(f"{len(lg)} phrases de plus de {S['phrase_longue']} mots ({part:.0%}) : {ex}")
        if moy > S["phrase_moyenne_max"]:
            avert.append(f"phrases de {moy:.1f} mots en moyenne (cible ≤ {S['phrase_moyenne_max']})")

    # 4. La requête dans l'introduction
    intro = paras[0] if paras else ""
    if intro and not (nomme_entite(intro, ents) or len(radicaux(fm.get("requete_cible", "")) & radicaux(intro)) * 2
                      >= len(radicaux(fm.get("requete_cible", "")))):
        bloq.append("l'introduction ne nomme ni la requête cible ni l'objet de l'article")

    # 5. Couverture de l'intention
    if b:
        titres = re.findall(r"^#{2,3}\s+(.+)$", visible, re.M) + re.findall(r"^\*\*(.+\?)\*\*\s*$", visible, re.M)
        bref = "\n".join(l for l in visible.split("\n") if l.startswith(">"))
        cibles = [radicaux(t) for t in titres] + [radicaux(bref)]
        oublis = []
        for q in b["questions"]:
            rq = radicaux(re.sub(r"\(.*?\)", "", q))
            if rq and not any(len(rq & c) / len(rq) >= 0.6 for c in cibles):
                oublis.append(q)
        if oublis:
            avert.append("questions du brief sans titre, question de FAQ ni réponse dans « En bref » : " + " · ".join(f"« {q} »" for q in oublis))
        rv = radicaux(visible)
        absents = [t for t in b["termes"] if not radicaux(t) <= rv]
        if b["termes"] and len(absents) > len(b["termes"]) / 2:
            bloq.append(f"{len(absents)}/{len(b['termes'])} termes du brief absents de l'article : {', '.join(absents[:6])}")
        elif absents:
            avert.append(f"termes du brief absents : {', '.join(absents)}")

    # 6. Images : un nom de fichier et un texte alternatif qui disent ce qu'on voit
    noms_vagues = re.compile(r"^(img|dsc|dcim|pxl|image|photo|picture|capture|screenshot|canva|essai|test|untitled|sans-titre|design)"
                             r"[-_ ]?\d*$|^[0-9a-f_-]{12,}$|^\d+$", re.I)
    for m in re.finditer(r"^!\[\[(.+?)\]\]\s*$", visible, re.M):
        p = [x.strip() for x in m.group(1).split("|")] + ["", "", ""]
        chemin, alt = p[0], p[2]
        if chemin.lower().endswith(".svg"):
            continue
        nom = os.path.splitext(os.path.basename(chemin))[0]
        mots_nom = [x for x in re.split(r"[-_ ]+", nom) if x]
        if noms_vagues.match(nom) or len(mots_nom) < 3:
            bloq.append(f"nom de fichier qui ne décrit pas l'image : « {os.path.basename(chemin)} » (ex. creuset-poele-a-pellets-encrasse.jpg)")
        if not alt:
            bloq.append(f"image sans texte alternatif : {os.path.basename(chemin)}")
        elif not 25 <= len(alt) <= 140:
            avert.append(f"texte alternatif de {len(alt)} caractères (25 à 140) : « {alt[:50]} »")
        if alt and not (nomme_entite(alt, ents) or nomme_entite(" ".join(mots_nom), ents)):
            avert.append(f"ni le nom ni le texte alternatif de {os.path.basename(chemin)} ne nomment l'objet de l'article : glisser le mot-clé s'il décrit l'image")
        if len(re.findall(re.escape(fm.get("requete_cible", "~")), alt.lower())) > 1:
            avert.append(f"mot-clé répété dans le texte alternatif de {os.path.basename(chemin)}")

    # 7. Pages locales : texte propre à la ville
    if config.est_locale(fm):
        if not fm.get("ville"):
            bloq.append("page locale sans `ville` dans le front-matter")
        part, autre = doublon_local(fm, visible, art_dir, parse)
        if part > S["doublon_max"]:
            bloq.append(f"{part:.0%} du texte se retrouve déjà dans {autre} : la page doit reposer sur les données de sa ville")
        elif part > S["doublon_avert"]:
            avert.append(f"{part:.0%} du texte en commun avec {autre}")
    return bloq, avert
