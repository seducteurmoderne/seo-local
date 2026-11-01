"""Prix relevés chaque jour chez les fournisseurs, et leur date de relevé dans les articles.

Les relevés vivent dans <dossier du site>/prix/releves.json, un objet par prix :

  "atoutbois_vert_hcc": {
    "source": "Atoutbois",                       nom affiché dans les notes
    "url": "https://atoutbois.be/?page_id=18",   page relue chaque jour
    "motif": "charme en 33 ou 50cm.*?(\\d+)€/st", expression cherchée dans le texte de la page
                                                   (balises retirées) ; le groupe 1 est le prix
    "valeur": 86,                                dernier prix lu
    "verifie_le": "2026-10-09",                  dernier jour où le prix a été relu tel quel
    "echecs": 0                                  jours de suite sans pouvoir le relire
  }

Un relevé à « attendu » ne lit pas de prix : il vérifie que la page montre toujours la même chose
(le tableau mensuel de Valbiom, qui est une image). Tant que le groupe 1 vaut « attendu », la date
avance ; quand il change, le pilote le signale et la valeur reste celle de la main.

Dans un article (rendu seulement : la source Markdown ne change pas) :
  {{prix:id}}      le prix, sans unité (« 86 », « 2 150 », « 7,91 »)
  {{calc:expr}}    un calcul sur les id, arrondi à l'unité : {{calc:(atoutbois_vert_hcc*5+75)/5}}, {{calc:min(id_a, id_b)}}
  {{releve}}       la date du plus ancien relevé parmi les prix cités dans l'article (« 9 octobre 2026 »)
  {{releve:id}}    la date du relevé d'un prix

La date n'avance que si le prix a été relu le jour même sur le site du fournisseur : une page qui
affiche « relevé du <aujourd'hui> » dit vrai. Un prix illisible garde sa dernière date.
"""
import ast, datetime, decimal, html, json, operator, os, re

from config import ROOT

FICHIER = os.path.join(ROOT, "prix", "releves.json")
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
        "septembre", "octobre", "novembre", "décembre"]
BALISE = re.compile(r"\{\{(prix|calc[12]?|releve)(?::([^}]+))?\}\}")


def charger():
    if not os.path.exists(FICHIER):
        return {}
    with open(FICHIER, encoding="utf-8") as f:
        return json.load(f)


def enregistrer(rel):
    os.makedirs(os.path.dirname(FICHIER), exist_ok=True)
    with open(FICHIER, "w", encoding="utf-8") as f:
        json.dump(rel, f, ensure_ascii=False, indent=2)
        f.write("\n")


# ---------------------------------------------------------------- lecture des pages
def texte_page(brut):
    """Texte visible d'une page HTML, espaces normalisés."""
    t = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", " ", brut, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def nombre(s):
    """« 2 150 », « 345,00 », « 7.91 » → 2150, 345, 7.91."""
    s = re.sub(r"[\s  ]", "", s).replace(",", ".")
    v = float(s)
    return int(v) if v == int(v) else v


def _signaler(r):
    """Un échec se signale le premier jour, puis une fois par semaine."""
    return r["echecs"] == 1 or r["echecs"] % 7 == 0


def actualiser(lire, aujourdhui=None):
    """Relit chaque prix. `lire(url)` rend le HTML. Retourne la liste des messages pour le journal."""
    rel = charger()
    if not rel:
        return []
    jour = (aujourdhui or datetime.date.today()).isoformat()
    pages, erreurs, msgs = {}, {}, []
    for ident, r in rel.items():
        if r.get("verifie_le") == jour and not r.get("echecs"):
            continue
        url = r["url"]
        if url not in pages:
            try:
                pages[url] = texte_page(lire(url))
            except Exception as e:
                pages[url] = None
                erreurs[url] = str(e)
        texte = pages[url]
        m = re.search(r["motif"], texte, re.S) if texte else None
        if not m:
            r["echecs"] = r.get("echecs", 0) + 1
            if _signaler(r):
                cause = f"page illisible ({erreurs.get(url)})" if texte is None else "motif introuvable, à revoir"
                msgs.append(f"prix : `{ident}` non relu chez {r.get('source', url)} depuis {r['echecs']} jour(s), "
                            f"{cause} — la page garde la date du {r.get('verifie_le')}")
            continue
        lu = m.group(1).strip()
        if "attendu" in r:
            if lu != r["attendu"]:
                r["echecs"] = r.get("echecs", 0) + 1
                if _signaler(r):
                    msgs.append(f"prix : `{ident}` a changé chez {r.get('source')} (« {lu} » au lieu de "
                                f"« {r['attendu']} ») — chiffre et texte à mettre à jour à la main")
                continue
        else:
            v = nombre(lu)
            if v != r.get("valeur"):
                msgs.append(f"prix : `{ident}` passe de {r.get('valeur')} à {v} ({r.get('source')}) — "
                            "relire les phrases qui comparent ce prix")
                r["valeur"] = v
        r["verifie_le"], r["echecs"] = jour, 0
    enregistrer(rel)
    return msgs


# ---------------------------------------------------------------- rendu dans les articles
def format_nombre(v):
    """86 → « 86 », 2150 → « 2 150 », 7.91 → « 7,91 »."""
    if isinstance(v, float) and v != int(v):
        ent, dec = f"{v:.2f}".split(".")
        return f"{int(ent):,}".replace(",", " ") + "," + dec
    return f"{int(round(v)):,}".replace(",", " ")


def arrondi(v):
    """Arrondi commercial à l'unité (192,5 → 193), pas l'arrondi au pair de Python."""
    return int(decimal.Decimal(str(v)).quantize(decimal.Decimal("1"), rounding=decimal.ROUND_HALF_UP))


def format_decimal(v, n):
    """10.8, 1 → « 10,8 » ; 7.2, 2 → « 7,20 »."""
    ent, dec = f"{v:.{n}f}".split(".")
    return f"{int(ent):,}".replace(",", " ") + "," + dec


def format_date(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{'1er' if d.day == 1 else d.day} {MOIS[d.month - 1]} {d.year}"


_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}


def calculer(expr, rel, utilises):
    def ev(n):
        if isinstance(n, ast.Expression):
            return ev(n.body)
        if isinstance(n, ast.BinOp) and type(n.op) in _OPS:
            return _OPS[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub):
            return -ev(n.operand)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in ("min", "max") and n.args:
            return (min if n.func.id == "min" else max)(ev(x) for x in n.args)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.Name):
            if n.id not in rel:
                raise KeyError(n.id)
            utilises.add(n.id)
            return rel[n.id]["valeur"]
        raise ValueError(f"calcul non permis : {expr}")
    return ev(ast.parse(expr.strip(), mode="eval"))


def inconnus(body):
    """Balises qui renvoient à un relevé absent (contrôle bloquant)."""
    rel, faux = charger(), []
    for sorte, arg in BALISE.findall(body):
        if sorte == "prix" or (sorte == "releve" and arg):
            if arg.strip() not in rel:
                faux.append(arg.strip())
        elif sorte.startswith("calc"):
            try:
                calculer(arg, rel, set())
            except Exception as e:
                faux.append(f"calc:{arg} ({e})")
    return faux


def remplacer(body):
    """Remplace les balises par les valeurs du jour. Sans balise, le texte est rendu tel quel."""
    if "{{" not in body:
        return body
    rel, utilises = charger(), set()

    def val(m):
        sorte, arg = m.group(1), (m.group(2) or "").strip()
        try:
            if sorte == "prix":
                utilises.add(arg)
                return format_nombre(rel[arg]["valeur"])
            if sorte == "calc":
                return format_nombre(arrondi(calculer(arg, rel, utilises)))
            if sorte in ("calc1", "calc2"):
                n = int(sorte[-1])
                v = float(decimal.Decimal(str(calculer(arg, rel, utilises))).quantize(
                    decimal.Decimal(1).scaleb(-n), rounding=decimal.ROUND_HALF_UP))
                return format_decimal(v, n)
            if sorte == "releve" and arg:
                utilises.add(arg)
                return format_date(rel[arg]["verifie_le"])
        except (KeyError, ValueError, SyntaxError, ZeroDivisionError):
            return m.group(0)
        return m.group(0)

    body = BALISE.sub(lambda m: m.group(0) if m.group(1) == "releve" and not m.group(2) else val(m), body)
    if "{{releve}}" in body:
        dates = [rel[i]["verifie_le"] for i in utilises if i in rel and rel[i].get("verifie_le")]
        body = body.replace("{{releve}}", format_date(min(dates)) if dates else "{{releve}}")
    return body


# ---------------------------------------------------------------- date du jour de la visite
# {{aujourdhui}} : dans le texte, la date s'écrit au rendu puis le navigateur du visiteur la remplace
# par la date du jour (heure de Bruxelles) ; dans un title ou une méta, c'est la date de l'envoi,
# renouvelé chaque matin par le maillage.
JOUR = "{{aujourdhui}}"
_JS_JOUR = ('<script>(function(){var d=new Date(),o={day:"numeric",month:"long",year:"numeric",timeZone:"Europe/Brussels"};'
            'var t=d.toLocaleDateString("fr-BE",o).replace(/^1 /,"1er ");'
            '[].forEach.call(document.querySelectorAll(".bcp-jour"),function(s){s.textContent=t;});})();</script>')


def date_du_jour():
    import config
    try:
        from zoneinfo import ZoneInfo
        return datetime.datetime.now(ZoneInfo(config.FUSEAU)).date()
    except Exception:
        return datetime.date.today()


def texte(s):
    """Titre, méta, H1 : balises de prix remplacées, {{aujourdhui}} → date du jour en clair."""
    if not s or "{{" not in s:
        return s
    return remplacer(s).replace(JOUR, format_date(date_du_jour().isoformat()))


def jour_html(h):
    """Rendu HTML : {{aujourdhui}} devient une date que le navigateur du visiteur met à son jour."""
    if JOUR not in h:
        return h
    d = date_du_jour().isoformat()
    h = h.replace(JOUR, f'<span class="bcp-jour" data-rendu="{d}">{format_date(d)}</span>')
    return h + "\n\n<!-- wp:html -->\n" + _JS_JOUR + "\n<!-- /wp:html -->"


def front_matter(fm):
    """Front-matter avec title, méta et H1 du jour (les autres champs inchangés)."""
    out = {k: (texte(v) if k in ("title_seo", "meta_description", "h1", "fil_ariane") and isinstance(v, str) else v)
           for k, v in fm.items()}
    if isinstance(fm.get("h1"), str) and JOUR in fm["h1"]:
        out["h1_jour"] = remplacer(fm["h1"])  # H1 affiché : la date reste {{aujourdhui}}, mise à jour par le navigateur
    return out
