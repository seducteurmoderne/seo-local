"""Moteur de brief SEO en cascade.

    python3 tools/autopilote.py brief <slug> [<url de résultat Google>…]   (lance ou reprend)
    python3 tools/autopilote.py brief <slug> --refaire <étape>             (efface une étape et la suite)

Deux regards, puis une synthèse critiquée :
  1. suggestions  variantes de recherche (suggestions Google Belgique, puis DuckDuckGo)
  2. candidats    pages classées : liens google.be donnés en argument (le plus fiable), puis DuckDuckGo
                  région Belgique ; jusqu'à 30 candidats
  3. pages        lecture adaptative : une page illisible ou bloquée est sautée, on passe à la suivante,
                  jusqu'à 10 pages lisibles
  4. lecteur      l'IA, SANS regarder les concurrents : qui cherche, dans quelle situation, ce qu'il veut
                  lire en premier, ses questions, ce qu'il lui faut pour décider, ce qui le ferait demander un devis
  5. concurrents  l'IA lit la structure des pages : intention que Google récompense, sections incontournables,
                  différenciantes, lacunes, faiblesses
  6. brief        l'IA croise 4 et 5 avec la charte : intention, plan H2/H3 avec le contenu de chaque section
  7. critique     l'IA relit le brief comme un SEO senior exigeant et le corrige
Le bloc BRIEF SEO final s'inscrit dans les notes de production de articles/<slug>.md (s'il existe) ;
le brief détaillé (contenu de chaque section, objections, déclencheur du devis) est dans briefs/<slug>/brief.md.
Chaque étape écrit son résultat dans briefs/<slug>/ : une étape faite n'est jamais refaite.
"""
import os, re, json, csv, html, shutil, urllib.request, urllib.parse
from collections import OrderedDict

import config
import serp
import ia

ETAPES = ["suggestions", "candidats", "pages", "lecteur", "concurrents", "brief", "critique"]
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/126.0 Safari/537.36", "Accept-Language": "fr-BE,fr;q=0.9"}
EXCLUS = re.compile(r"(duckduckgo\.com/y\.js|bing\.com/aclick|google\.[a-z.]+/(aclk|search)|facebook\.com|instagram\.com|"
                    r"tiktok\.com|pinterest\.)")


# Pays et langue des recherches, présentation du site dans les questions à l'IA : site.json → "brief".
# Par défaut, les réglages des sites belges (Google Belgique, français, site de demandes de devis).
B = {"hl": "fr", "gl": "be", "kl": "be-fr", "pays": "Belgique",
     "modifs": ["", "comment ", "pourquoi ", "prix ", "quel ", "quand "],
     "expert": "Tu es un rédacteur SEO senior qui connaît le chauffage au bois en Wallonie.",
     "presentation": None,
     "declencheur": "ce qui la ferait demander un devis sur ce site, et à quel moment de la page"}
B.update(config.SITE.get("brief", {}))


def _get(url, timeout=20):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read().decode("utf-8", "ignore")


# ---------------------------------------------------------------- 1. variantes
def suggestions(q):
    vues = OrderedDict()
    modifs = B["modifs"]
    for m in modifs:
        for source in ("google", "ddg"):
            try:
                if source == "google":
                    d = json.loads(_get("https://suggestqueries.google.com/complete/search?" + urllib.parse.urlencode(
                        {"client": "firefox", "hl": B["hl"], "gl": B["gl"], "q": m + q})))
                    liste = d[1]
                else:
                    d = json.loads(_get("https://duckduckgo.com/ac/?" + urllib.parse.urlencode({"q": m + q, "kl": B["kl"]})))
                    liste = [x["phrase"] for x in d]
            except Exception:
                continue
            for s in liste:
                vues.setdefault(s.strip(), source)
    return [{"requete": k, "source": v} for k, v in vues.items() if k]


# ---------------------------------------------------------------- 2. candidats
def candidats_ddg(q, pages=2):
    out = []
    for p in range(pages):
        try:
            params = {"q": q, "kl": B["kl"]}
            if p:
                params["s"] = str(30 * p)
            h = _get("https://html.duckduckgo.com/html/?" + urllib.parse.urlencode(params))
        except Exception:
            break
        for l in re.findall(r'class="result__a" href="([^"]+)"', h):
            l = html.unescape(l)
            if "uddg=" in l:
                l = urllib.parse.unquote(re.sub(r"^.*?uddg=([^&]+).*$", r"\1", l))
            if l.startswith("//"):
                l = "https:" + l
            out.append(l)
    return out


def candidats(q, liens_google):
    """Liste ordonnée, sans doublon, au plus 2 pages par domaine : Google Belgique d'abord, puis DuckDuckGo."""
    vus, par_domaine, out = set(), {}, []
    sources = ([(f"google.{B['gl']}", serp.resoudre(u)) for u in liens_google]
               + [(f"duckduckgo {B['kl']}", u) for u in candidats_ddg(q)])
    for source, u in sources:
        if not u.startswith("http") or EXCLUS.search(u):
            continue
        cle = re.sub(r"[?#].*$", "", u).rstrip("/")
        dom = urllib.parse.urlparse(u).netloc.replace("www.", "")
        if cle in vus or par_domaine.get(dom, 0) >= 2:
            continue
        vus.add(cle)
        par_domaine[dom] = par_domaine.get(dom, 0) + 1
        out.append({"url": u, "source": source})
    return out[:30]


# ---------------------------------------------------------------- 3. lecture adaptative
def lisible(p):
    return "erreur" not in p and p.get("mots", 0) >= 150 and len(p.get("titres", [])) >= 1


def lire_pages(cands, cible=10):
    lues, sautees = [], []
    for c in cands:
        if len([p for p in lues if lisible(p)]) >= cible:
            break
        p = serp.analyser_page(c["url"])
        p["source"] = c["source"]
        p["rang"] = len(lues) + len(sautees) + 1
        if lisible(p):
            lues.append(p)
            print(f"  ✔ {p['url'][:80]} — {p['mots']} mots, {len(p['titres'])} titres")
        else:
            p["raison"] = p.get("erreur") or f"trop peu de contenu ({p.get('mots', 0)} mots)"
            sautees.append(p)
            print(f"  ↷ {c['url'][:80]} — sautée : {p['raison'][:60]}")
    return lues, sautees


# ---------------------------------------------------------------- contexte commun des questions à l'IA
def contexte(fm, ligne):
    s = config.SITE
    besoins = ", ".join(b["libelle"] for b in s["formulaire"]["besoins"])
    locale = config.est_locale(fm) or (ligne.get("cluster") == config.LOCAL.get("cluster"))
    presentation = B["presentation"] or (
        f"Un intermédiaire, pas un vendeur : il transmet gratuitement des demandes de devis à des "
        f"professionnels de la région du visiteur ({besoins}). Zone : Wallonie (Belgique), visiteurs belges francophones.")
    return (f"Site : {s['nom']}. {presentation}\n"
            f"Page à écrire : « {ligne.get('titre') or fm.get('h1', '')} » (slug {fm.get('slug') or ligne.get('url', '').strip('/')}), "
            f"verticale {ligne.get('verticale') or fm.get('categorie', '')}, cluster {ligne.get('cluster') or fm.get('cluster', '')}"
            + (", page locale (modèle de page de ville du site)" if locale else "") + ".\n")


def q_lecteur(ctx, q, sugg):
    return f"""{B["expert"]}
{ctx}
Requête cible : « {q} »
Recherches associées en {B["pays"]} : {", ".join(s["requete"] for s in sugg[:30]) or "aucune"}

SANS regarder ce que publient les concurrents, réfléchis à la personne qui tape cette requête :
1. qui elle est, dans quelle situation (moment, urgence, ce qu'elle a déjà essayé) ;
2. son intention principale et ses intentions secondaires (informationnelle, commerciale, locale, navigationnelle), avec la part de chacune ;
3. ce qu'elle veut lire en premier, avant de faire défiler la page ;
4. les questions qu'elle se pose, dans l'ordre où elle se les pose ;
5. les informations dont elle a besoin pour décider ou agir (chiffres, critères, étapes) ;
6. ses doutes et objections ;
7. {B["declencheur"]}.

Réponds uniquement par un objet JSON :
{{"persona": "", "situation": "", "intentions": [{{"type": "", "part": 0.0, "description": ""}}], "reponse_attendue": "", "questions": [""], "informations": [""], "objections": [""], "declencheur_devis": ""}}"""


def q_concurrents(ctx, q, synthese, pages):
    plans = []
    for p in pages:
        t = "\n".join(("    " if n == "h3" else "  ") + f"{n.upper()} {x}" for n, x in p["titres"][:40])
        plans.append(f"- #{p['rang']} {p['url']} ({p['source']}) — {p['mots']} mots, {p['tables']} tableau(x), "
                     f"{p['ol']} liste(s) numérotée(s), FAQ : {'oui' if p['faq'] else 'non'}\n{t}")
    return f"""Tu es un consultant SEO senior. Analyse les pages qui se classent sur « {q} ».
{ctx}
Synthèse mesurée :
{synthese}

Plans des pages lues (dans l'ordre de classement) :
{chr(10).join(plans)}

Détermine :
1. le type de chaque page (guide, page de service, annuaire, comparateur, forum, boutique, vidéo) ;
2. l'intention que Google récompense sur cette requête ;
3. les sections que la majorité des pages traite (incontournables) ;
4. les sections que seules une ou deux pages traitent et qui apportent de la valeur (différenciantes) ;
5. ce qu'aucune page ne fait bien et que le lecteur attend (lacunes) ;
6. les faiblesses à exploiter (pages courtes, sans chiffres, sans réponse directe, mal structurées) ;
7. la longueur à viser pour faire mieux.

Réponds uniquement par un objet JSON :
{{"types": {{"guide": 0, "service": 0, "annuaire": 0, "autre": 0}}, "intention_recompensee": "", "incontournables": [""], "differenciants": [""], "lacunes": [""], "faiblesses": [""], "longueur_cible": 0}}"""


REGLES = """Règles de la charte du site (elles priment) :
- La réponse avant le premier scroll. Pour un guide ou une page locale : un encadré « En bref » de 3 à 5 puces si la requête appelle une réponse factuelle (il n'est jamais obligatoire). Pour une page prix : pas d'« En bref », le titre daté puis la carte du prix du jour (::prix-jour) ouvrent la page. Ensuite une introduction de 2 à 3 phrases dont la première nomme la requête.
- Chaque H2 se lit seul, comme une recherche Google, et nomme l'objet de la page (ou la ville d'une page locale). Nombres en chiffres. Jamais de titre d'accroche (« ce qu'il faut savoir », « vraiment », « le bon réflexe », « en pratique »…).
- Une H2 en question est suivie d'une réponse directe de 40 à 60 mots. Une procédure se donne en liste numérotée. Une comparaison de 3 éléments ou plus, en tableau.
- Toujours un paragraphe entre une H2 et sa première H3. Une liste à puces par article, deux au plus. Paragraphes de 80 mots au plus.
- Aucun fait chiffré, réglementaire ou normatif sans source primaire : le plan dit quelle donnée chercher, il n'invente rien.
- Le site est un intermédiaire : formulaire de devis (CTA) après l'introduction quand l'intention est commerciale ou locale ; une phrase de CTA doux sinon.
- Pas de classement ni de note des fournisseurs (neutralité). Pas de FAQ par défaut : seulement si 3 questions réelles restent sans section.
- Varier les formes : un article de plus de 800 mots porte au moins 2 éléments visuels (tableau, avantages et inconvénients, checklist, cartes de choix, citation, chiffres clés, schéma, image), jamais deux du même type à la suite. Une image ne se prévoit que si elle montre quelque chose d'utile (reconnaître, comparer, situer) : jamais d'ambiance.
- Page locale : suivre le modèle de page de ville du site (Qui livre… à <ville> ? · Prix… à <ville> · format · Livraison… à <ville> · autour de <ville>), chaque section avec une donnée propre à la ville."""


def q_brief(ctx, q, sugg, lecteur, conc, fm):
    return f"""Tu es un rédacteur SEO senior. Écris le brief de la page « {q} ».
{ctx}
Analyse du lecteur (notre propre réflexion) :
{json.dumps(lecteur, ensure_ascii=False, indent=1)}

Analyse des concurrents :
{json.dumps(conc, ensure_ascii=False, indent=1)}

Recherches associées : {", ".join(s["requete"] for s in sugg[:30])}
Objet de la page tel que les gens le nomment (entité) : {", ".join(fm.get("entites") or []) or "à déterminer"}

{REGLES}

Décide l'intention, puis le plan. Le plan reprend les incontournables, dans l'ordre où le lecteur se pose les questions, ajoute ce qui comble les lacunes, et dit pour chaque section ce qu'elle doit contenir et sous quelle forme. Les variantes et termes viennent des recherches associées et du vocabulaire des pages classées.

Réponds uniquement par un objet JSON :
{{"intention": "", "format_serp": "", "structure_serp": "", "entites": [""], "variantes": [""], "termes": [""], "questions": [""], "en_bref": [""], "plan": [{{"h2": "", "contenu": "", "forme": "paragraphe | réponse directe | liste numérotée | tableau | tableau avec colonne mise en avant | avantages et inconvénients | checklist à vérifier / à éviter | cartes de choix | citation mise en avant | notre avis | chiffres clés | schéma | image 600x400 | bannière | carte", "image": "ce que l'image doit montrer, si la section en a besoin, sinon vide", "donnees_a_chercher": [""], "h3": [{{"titre": "", "contenu": ""}}]}}], "cta": "", "faq": [""], "longueur_cible": 0, "decision": ""}}"""


def q_critique(ctx, q, brief_, lecteur, conc):
    return f"""Tu es un directeur SEO exigeant. Relis ce brief pour « {q} » avant rédaction.
{ctx}
Brief :
{json.dumps(brief_, ensure_ascii=False, indent=1)}

Ce que veut le lecteur :
{json.dumps(lecteur, ensure_ascii=False, indent=1)}

Ce que font les concurrents :
{json.dumps(conc, ensure_ascii=False, indent=1)}

{REGLES}

Contrôle point par point : le plan répond-il à l'intention dominante dès le début ? Chaque question du lecteur a-t-elle sa section ? Les incontournables sont-ils couverts ? Le brief apporte-t-il quelque chose qu'aucun concurrent n'a ? Chaque H2 nomme-t-elle l'objet et se lit-elle seule ? Y a-t-il une section inutile, redondante ou hors sujet ? Une donnée inventée ou impossible à sourcer ? Le devis arrive-t-il au bon moment ?
Puis renvoie le brief corrigé, complet, au même format.

Réponds uniquement par un objet JSON :
{{"problemes": [""], "brief": {{...le brief corrigé, mêmes clés...}}}}"""


# ---------------------------------------------------------------- sortie
def bloc_brief(b, n_pages, sources):
    lignes = ["BRIEF SEO",
              f"Intention : {b.get('intention', '')}",
              f"Format SERP : {b.get('format_serp', '')} (sources : {sources})",
              f"Structure SERP : {b.get('structure_serp', '')} — {n_pages} pages lues, détail dans briefs/<slug>/serp.md",
              f"Variantes : {' ; '.join(b.get('variantes', []))}",
              f"Termes : {' ; '.join(b.get('termes', []))}",
              "Questions :"] + [f"- {q}" for q in b.get("questions", [])] + ["Plan :"]
    for s in b.get("plan", []):
        lignes.append(f"- H2 : {s.get('h2', '')}")
        lignes += [f"  - H3 : {h.get('titre', '')}" for h in s.get("h3", []) or []]
    lignes.append(f"Décision : {b.get('decision', '')}")
    return "\n".join(lignes)


def brief_detaille(slug, q, b, lecteur, conc, problemes):
    out = [f"# Brief — {q}", "", f"Article : `articles/{slug}.md`", "", "## Le lecteur", "",
           f"**Qui** : {lecteur.get('persona', '')}", "", f"**Situation** : {lecteur.get('situation', '')}", "",
           f"**Ce qu'il veut lire en premier** : {lecteur.get('reponse_attendue', '')}", "",
           "**Objections** :"] + [f"- {o}" for o in lecteur.get("objections", [])] + [
           "", f"**Déclencheur du devis** : {lecteur.get('declencheur_devis', '')}", "",
           "## Les concurrents", "", f"**Intention récompensée** : {conc.get('intention_recompensee', '')}", "",
           "**Lacunes à combler** :"] + [f"- {x}" for x in conc.get("lacunes", [])] + [
           "", "**Faiblesses à exploiter** :"] + [f"- {x}" for x in conc.get("faiblesses", [])] + [
           "", "## En bref (proposition)", ""] + [f"- {x}" for x in b.get("en_bref", [])] + ["", "## Plan détaillé", ""]
    for s in b.get("plan", []):
        out += [f"### H2 — {s.get('h2', '')}", "", f"*Forme : {s.get('forme', '')}*", "", s.get("contenu", "")]
        if s.get("donnees_a_chercher"):
            out += ["", "Données à sourcer : " + " · ".join(s["donnees_a_chercher"])]
        for h in s.get("h3", []) or []:
            out += ["", f"- **H3 — {h.get('titre', '')}** : {h.get('contenu', '')}"]
        out.append("")
    out += [f"**CTA** : {b.get('cta', '')}", "", f"**Longueur visée** : {b.get('longueur_cible', '')} mots", ""]
    if b.get("faq"):
        out += ["**FAQ** (seulement si ces questions restent sans section) :"] + [f"- {x}" for x in b["faq"]] + [""]
    if problemes:
        out += ["## Ce que la relecture critique a corrigé", ""] + [f"- {x}" for x in problemes]
    return "\n".join(out)


def inscrire(chemin, bloc, entites):
    """Place le bloc BRIEF SEO dans les notes de production de l'article (remplace l'ancien), et `entites` en front-matter."""
    t = open(chemin, encoding="utf-8").read()
    if re.search(r"BRIEF SEO\n", t):
        # le bloc s'arrête à la première ligne vide : rien d'autre dans les notes n'est touché
        t = re.sub(r"BRIEF SEO\n(?:[^\n]+\n)*", lambda m: bloc + "\n", t, count=1)
    elif "<!--" in t:
        t = t.replace("<!--", "<!--\n" + bloc + "\n", 1)
    else:
        t = t.rstrip() + "\n\n<!--\nNOTES DE PRODUCTION\n\n" + bloc + "\n-->\n"
    if entites and not re.search(r"^entites:", t, re.M):
        t = re.sub(r"^(requete_cible:.*)$", lambda m: m.group(1) + "\nentites:\n" + "\n".join(f"  - {e}" for e in entites), t, count=1, flags=re.M)
    open(chemin, "w", encoding="utf-8").write(t)


# ---------------------------------------------------------------- orchestration
def main(args, parse_article, art_dir, sitemap):
    slug = args[0]
    d = os.path.join(config.ROOT, "briefs", slug)
    os.makedirs(d, exist_ok=True)
    if "--refaire" in args:
        e = args[args.index("--refaire") + 1]
        for x in ETAPES[ETAPES.index(e):]:
            for f in (f"{x}.json", f"{x}.prompt.md"):
                if os.path.exists(os.path.join(d, f)):
                    os.remove(os.path.join(d, f))
        args = args[:args.index("--refaire")]
    liens_google = [a for a in args[1:] if a.startswith("http")]
    chemin = os.path.join(art_dir, f"{slug}.md")
    fm = parse_article(chemin)[0] if os.path.exists(chemin) else {}
    ligne = next((r for r in csv.DictReader(open(sitemap, encoding="utf-8")) if r["url"].strip("/") == slug), {})
    q = fm.get("requete_cible") or re.sub(r"^(acheter|choisir)\s+", "", (ligne.get("titre") or slug).lower())
    ctx = contexte(fm, ligne)
    garder = lambda nom, data: json.dump(data, open(os.path.join(d, f"{nom}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    lire = lambda nom: json.load(open(os.path.join(d, f"{nom}.json"), encoding="utf-8")) if os.path.exists(os.path.join(d, f"{nom}.json")) else None
    print(f"Brief SEO — « {q} »")

    sugg = lire("suggestions")
    if sugg is None:
        sugg = suggestions(q)
        garder("suggestions", sugg)
    print(f"1. suggestions : {len(sugg)} variantes")

    cands = lire("candidats")
    if cands is None or (liens_google and not any(c["source"] == f"google.{B['gl']}" for c in cands)):
        cands = candidats(q, liens_google)
        garder("candidats", cands)
    google = f"google.{B['gl']}"
    print(f"2. candidats : {len(cands)} ({sum(c['source'] == google for c in cands)} de {google})")

    pages = lire("pages")
    if pages is None:
        print("3. lecture des pages :")
        lues, sautees = lire_pages(cands)
        pages = {"lues": lues, "sautees": [{"url": p["url"], "raison": p["raison"]} for p in sautees]}
        garder("pages", pages)
        synth = serp.synthese(lues, q)
        rapport = [f"# Analyse SERP — {q}", "", "## Synthèse", "", synth, "", "## Les pages lues, dans l'ordre", ""]
        for p in lues:
            rapport += [f"### {p['rang']}. {p.get('titre', '')[:100]}", "", p["url"], "", f"{p['mots']} mots · source : {p['source']}", ""]
            rapport += [("- " if n == "h2" else "  - " if n == "h3" else "**H1** ") + t for n, t in p["titres"]] + [""]
        if pages["sautees"]:
            rapport += ["## Pages sautées", ""] + [f"- {p['url']} — {p['raison']}" for p in pages["sautees"]]
        open(os.path.join(d, "serp.md"), "w", encoding="utf-8").write("\n".join(rapport))
        shutil.copy(os.path.join(d, "serp.md"), os.path.join(config.ROOT, "briefs", f"{os.path.basename(slug)}.md"))
    lues = pages["lues"]
    print(f"3. pages : {len(lues)} lues, {len(pages['sautees'])} sautées")
    synth = serp.synthese(lues, q)

    try:
        lecteur = ia.demander(q_lecteur(ctx, q, sugg), "lecteur", d)
        print("4. lecteur : analysé")
        conc = ia.demander(q_concurrents(ctx, q, synth, lues), "concurrents", d)
        print("5. concurrents : analysés")
        b = ia.demander(q_brief(ctx, q, sugg, lecteur, conc, fm), "brief", d)
        print(f"6. brief : {len(b.get('plan', []))} sections")
        crit = ia.demander(q_critique(ctx, q, b, lecteur, conc), "critique", d)
        b, problemes = crit.get("brief") or b, crit.get("problemes", [])
        print(f"7. critique : {len(problemes)} correction(s)")
    except ia.IAIndisponible as e:
        raise SystemExit(f"⏸ {e}")

    sources = " + ".join(sorted({p["source"] for p in lues})) or "aucune"
    bloc = bloc_brief(b, len(lues), sources).replace("<slug>", slug)
    open(os.path.join(d, "brief.md"), "w", encoding="utf-8").write(
        brief_detaille(slug, q, b, lecteur, conc, problemes) + "\n\n## Bloc pour les notes de production\n\n```\n" + bloc + "\n```\n")
    if os.path.exists(chemin):
        inscrire(chemin, bloc, b.get("entites"))
        print(f"✔ brief inscrit dans articles/{slug}.md · détail : briefs/{slug}/brief.md")
    else:
        print(f"✔ brief prêt : briefs/{slug}/brief.md (crée l'article, puis relance la commande pour l'y inscrire)")
