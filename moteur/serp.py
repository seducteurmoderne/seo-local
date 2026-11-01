"""Analyse des pages classées sur une requête : la base du brief SEO.

    python3 tools/autopilote.py serp <slug> <url1> <url2> … (les 10 premiers résultats, dans l'ordre)

Pour chaque URL : titre, H1, plan H2/H3, nombre de mots, tableaux, listes, FAQ, vidéo, données structurées.
Puis une synthèse : longueur médiane, formats dominants, sujets que plusieurs pages traitent, questions posées.
Le rapport s'écrit dans briefs/<slug>.md ; le brief et le plan de l'article s'écrivent à partir de lui.
"""
import os, re, json, html, statistics, urllib.request, urllib.error
from html.parser import HTMLParser
from collections import Counter

import config

DOSSIER = os.path.join(config.ROOT, "briefs")
HORS_CONTENU = {"nav", "footer", "aside", "header", "form", "script", "style", "noscript", "svg", "button"}
TITRES_PARASITES = re.compile(r"(articles? (récents|similaires|liés)|catégories|commentaires?|laisser un commentaire|newsletter|"
                              r"partager|suivez-nous|à propos de l'auteur|vous aimerez aussi|sommaire|table des matières|"
                              r"contact|menu|rechercher|navigation|publicité|derniers articles|nos guides)", re.I)
MOTS_VIDES = {"de", "du", "des", "le", "la", "les", "un", "une", "et", "ou", "a", "au", "aux", "en", "pour", "par", "sur",
              "dans", "avec", "son", "sa", "ses", "votre", "vos", "quel", "quelle", "quels", "quelles", "comment", "combien",
              "pourquoi", "quand", "est", "ce", "que", "qui", "quoi", "d", "l", "s", "faut", "il", "on", "ne", "pas", "plus",
              "vous", "nous", "nos", "notre", "mon", "ma", "mes", "faire", "bien", "tout", "tous", "y", "se", "si", "sont", "peut"}


class _Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.pile, self.titres, self.texte = [], [], []
        self.titre_page, self.h_en_cours, self.dans_title = "", None, False
        self.tables = self.ol = self.ul = self.images = self.videos = 0
        self.jsonld, self.dans_jsonld = [], False
        self.titres_main, self.texte_main = [], []  # ce qui est dans <main> ou <article> : le contenu, sans les blocs annexes

    def _dans_main(self):
        return "main" in self.pile or "article" in self.pile

    def _hors(self):
        return any(t in HORS_CONTENU for t in self.pile)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "script" and "ld+json" in (a.get("type") or ""):
            self.dans_jsonld = True
        if tag in ("br", "img", "hr", "meta", "link", "input", "source"):
            if tag == "img" and not self._hors():
                self.images += 1
            return
        self.pile.append(tag)
        if tag == "title":
            self.dans_title = True
        if self._hors():
            return
        if tag in ("h1", "h2", "h3"):
            self.h_en_cours = [tag, ""]
        elif tag == "table":
            self.tables += 1
        elif tag == "ol":
            self.ol += 1
        elif tag == "ul":
            self.ul += 1
        elif tag == "iframe" and re.search(r"youtube|vimeo|dailymotion", a.get("src") or ""):
            self.videos += 1
        elif tag == "video":
            self.videos += 1

    def handle_endtag(self, tag):
        if tag == "script":
            self.dans_jsonld = False
        if tag == "title":
            self.dans_title = False
        if self.h_en_cours and tag == self.h_en_cours[0]:
            t = " ".join(self.h_en_cours[1].split())
            if t and not TITRES_PARASITES.search(t):
                self.titres.append((tag, t))
                if self._dans_main():
                    self.titres_main.append((tag, t))
            self.h_en_cours = None
        if tag in self.pile:
            while self.pile and self.pile.pop() != tag:
                pass

    def handle_data(self, data):
        if self.dans_jsonld:
            self.jsonld.append(data)
            return
        if self.dans_title:
            self.titre_page += data
        if self._hors():
            return
        if self.h_en_cours:
            self.h_en_cours[1] += data
        self.texte.append(data)
        if self._dans_main():
            self.texte_main.append(data)


def lire(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                                                             "(KHTML, like Gecko) Chrome/126.0 Safari/537.36",
                                               "Accept-Language": "fr-BE,fr;q=0.9"})
    with urllib.request.urlopen(req, timeout=30) as r:
        brut = r.read()
        enc = r.headers.get_content_charset() or "utf-8"
    return brut.decode(enc, "ignore")


class _SansSuite(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def resoudre(url):
    """Un lien de résultat Google (google.be/goto?url=…, /url?q=…) → l'adresse réelle de la page."""
    if not re.search(r"//(www\.)?google\.[a-z.]+/(goto|url)\?", url):
        return url
    try:
        urllib.request.build_opener(_SansSuite).open(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=20)
    except urllib.error.HTTPError as e:
        if e.headers.get("Location"):
            return e.headers["Location"]
    except Exception:
        pass
    return url


def analyser_page(url):
    url = resoudre(url)
    try:
        h = lire(url)
    except Exception as e:
        return {"url": url, "erreur": str(e)[:120]}
    p = _Page()
    try:
        p.feed(h)
    except Exception:
        pass
    types = set()
    for bloc in p.jsonld:
        for t in re.findall(r'"@type"\s*:\s*"([^"]+)"', bloc):
            types.add(t)
    if len(p.titres_main) >= 2:  # la page balise son contenu : on s'y limite
        p.titres, p.texte = p.titres_main, p.texte_main
    texte = " ".join(" ".join(p.texte).split())
    mots = len(re.findall(r"[\wÀ-ÿ’'-]+", texte))
    faq = "FAQPage" in types or any(re.search(r"questions? fréquentes|faq", t, re.I) for _, t in p.titres)
    return {"url": url, "titre": " ".join(html.unescape(p.titre_page).split()), "titres": p.titres, "mots": mots,
            "tables": p.tables, "ol": p.ol, "ul": p.ul, "images": p.images, "videos": p.videos, "faq": faq,
            "schemas": sorted(types & {"Article", "BlogPosting", "NewsArticle", "FAQPage", "HowTo", "Product", "Review",
                                       "LocalBusiness", "VideoObject", "Recipe", "QAPage", "ItemList"})}


def _radicaux(t):
    t = t.lower()
    for a, b in (("àâä", "a"), ("éèêë", "e"), ("îï", "i"), ("ôö", "o"), ("ùûü", "u"), ("ç", "c")):
        t = re.sub(f"[{a}]", b, t)
    return [m[:6] for m in re.findall(r"[a-z0-9]+", t) if m not in MOTS_VIDES and len(m) > 2]


def synthese(pages, requete):
    ok = [p for p in pages if "erreur" not in p and p["titres"]]
    if not ok:
        return "Aucune page lisible : relancer avec d'autres URL."
    req = set(_radicaux(requete))
    lignes = [f"- Pages analysées : {len(ok)}/{len(pages)}"]
    m = [p["mots"] for p in ok]
    lignes.append(f"- Longueur : médiane {int(statistics.median(m))} mots (de {min(m)} à {max(m)})")
    for nom, test in (("tableau", lambda p: p["tables"]), ("liste numérotée", lambda p: p["ol"]), ("FAQ", lambda p: p["faq"]),
                      ("vidéo", lambda p: p["videos"])):
        n = sum(1 for p in ok if test(p))
        lignes.append(f"- {nom.capitalize()} : {n}/{len(ok)} pages")
    h2 = [[t for n, t in p["titres"] if n == "h2"] for p in ok]
    lignes.append(f"- H2 par page : médiane {int(statistics.median([len(x) for x in h2] or [0]))}")
    # Sujets récurrents : radicaux présents dans les H2/H3 d'au moins 3 pages (hors mots de la requête)
    par_page = Counter()
    exemples = {}
    for p in ok:
        vus = set()
        for n, t in p["titres"]:
            if n == "h1":
                continue
            for r in set(_radicaux(t)) - req:
                if r not in vus:
                    vus.add(r)
                    par_page[r] += 1
                    exemples.setdefault(r, []).append(t)
    seuil = max(3, len(ok) // 3)
    communs = [(r, n) for r, n in par_page.most_common(40) if n >= seuil]
    lignes.append("\n**Sujets traités par plusieurs pages** (radical : nombre de pages, exemple de titre) :")
    for r, n in communs[:20]:
        lignes.append(f"- {r} : {n} pages — « {exemples[r][0][:90]} »")
    questions = []
    for p in ok:
        for n, t in p["titres"]:
            if t.endswith("?") and t not in questions:
                questions.append(t)
    if questions:
        lignes.append("\n**Questions posées en titre** :")
        lignes += [f"- {q}" for q in questions[:25]]
    return "\n".join(lignes)


def analyser(slug, urls, requete):
    os.makedirs(DOSSIER, exist_ok=True)
    pages = []
    for i, u in enumerate(urls, 1):
        p = analyser_page(u)
        pages.append(p)
        print(("⛔" if "erreur" in p else "✔"), i, u[:90], p["erreur"] if "erreur" in p else f"{p['mots']} mots, {len(p['titres'])} titres")
    out = [f"# Analyse SERP — {requete}", "", f"Requête : `{requete}` · article : `{slug}`", "",
           "## Synthèse", "", synthese(pages, requete), "", "## Les pages, dans l'ordre", ""]
    for i, p in enumerate(pages, 1):
        if "erreur" in p:
            out += [f"### {i}. {p['url']}", "", f"Illisible : {p['erreur']}", ""]
            continue
        formats = ", ".join(x for x in (f"{p['tables']} tableau(x)" if p["tables"] else "", f"{p['ol']} liste(s) numérotée(s)" if p["ol"] else "",
                                        "FAQ" if p["faq"] else "", f"{p['videos']} vidéo(s)" if p["videos"] else "") if x) or "texte seul"
        out += [f"### {i}. {p['titre'][:100]}", "", f"{p['url']}", "",
                f"{p['mots']} mots · {formats} · schémas : {', '.join(p['schemas']) or 'aucun'}", ""]
        out += [("- " if n == "h2" else "  - " if n == "h3" else "**H1** ") + t for n, t in p["titres"]]
        out.append("")
    chemin = os.path.join(DOSSIER, f"{slug}.md")
    open(chemin, "w", encoding="utf-8").write("\n".join(out))
    lisibles = sum(1 for p in pages if "erreur" not in p and p["titres"])
    print(f"✔ {os.path.relpath(chemin, config.ROOT)} : {lisibles} page(s) analysée(s)")
    if lisibles < 8:
        print("⚠ moins de 8 pages lisibles : ajoutez les résultats suivants (11e, 12e…) pour atteindre 8 au moins")


def pages_analysees(slug):
    """Nombre de pages lisibles dans briefs/<slug>.md (0 si l'analyse n'existe pas)."""
    meilleur = 0
    for chemin in (os.path.join(DOSSIER, f"{slug}.md"), os.path.join(DOSSIER, slug, "serp.md"),
                   os.path.join(DOSSIER, "_essais", slug, "serp.md")):
        if os.path.exists(chemin):
            m = re.search(r"Pages analysées : (\d+)/", open(chemin, encoding="utf-8").read())
            meilleur = max(meilleur, int(m.group(1)) if m else 0)
    return meilleur
