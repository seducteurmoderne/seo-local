"""Design v2 des articles : en-tête (fil d'Ariane, titre, auteur et dates), encadré « En bref »,
sommaire, encadrés d'alerte et d'astuce, chiffres clés, tableaux, FAQ en accordéon, encadré auteur.

Activé par site.json → "design": 2. Tout est porté par le contenu (HTML + CSS scopé sous
.bcp-article) : aucun gabarit WordPress n'est modifié. Le titre du gabarit Elementor est masqué
par le CSS pour laisser place au fil d'Ariane, qui doit venir au-dessus du H1.
"""
import html, re, datetime as dt

import config

K = config.COULEURS
AUTEUR = config.SITE.get("auteur") or {}
POLICES = {"titres": "Fahkwang, Georgia, serif", "texte": "Roboto, -apple-system, 'Segoe UI', sans-serif",
           **config.SITE.get("polices", {})}
# Libellés affichés, en français par défaut. Un site dans une autre langue les remplace dans
# site.json → "textes" (mêmes clés). "date" : {j} jour, {er} suffixe du 1er du mois, {mois}, {a} année.
T = {
    "mois": ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre",
             "novembre", "décembre"],
    "date": "{j}{er} {mois} {a}", "premier": "er",
    "accueil": "Accueil", "fil_ariane": "Fil d'Ariane", "publie": "Publié le", "mis_a_jour": "Mis à jour le",
    "lecture": "min de lecture", "par": "Par", "a_propos_auteur": "À propos de l'auteur",
    "methode": "En savoir plus sur notre méthode",
    "en_bref": "En bref", "attention": "Attention", "bon_a_savoir": "Bon à savoir", "a_savoir": "À savoir",
    "sommaire": "Au sommaire", "sommaire_aria": "Sommaire",
    "a_verifier": "À vérifier", "a_eviter": "À éviter", "avantages": "Avantages", "inconvenients": "Inconvénients",
    "notre_avis": "Notre avis",
    "points_forts": "Points forts", "limites": "Limites", "voir_offre": "Voir l'offre",
    # titres reconnus dans les sources Markdown : section FAQ, ligne de sources (« *Sources : … »)
    "faq": ["Questions fréquentes", "FAQ"], "sources": ["Sources"],
}
T.update(config.SITE.get("textes", {}))
MOIS = T["mois"]
e = html.escape


def date_fr(d):
    return T["date"].format(j=d.day, er=T["premier"] if d.day == 1 else "", mois=MOIS[d.month - 1], a=d.year)


def ancre(texte):
    t = texte.lower()
    for a, b in (("àâä", "a"), ("éèêë", "e"), ("îï", "i"), ("ôö", "o"), ("ùûü", "u"), ("ç", "c")):
        t = re.sub(f"[{a}]", b, t)
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:60]


def html_bloc(h):
    return "<!-- wp:html -->\n" + h + "\n<!-- /wp:html -->"


# ---------------------------------------------------------------- en-tête
def fil_ariane(fm):
    """Accueil › page mère de la verticale › titre court. Une page mère : Accueil › titre."""
    etapes = [(T["accueil"], "/")]
    besoin = fm.get("besoin")
    mere = config.CATEGORIE_MERE.get(fm.get("categorie", ""))
    if not mere and besoin:
        mere = next((f"/{v['mere']}/" for v in config.VERTICALES if v["besoin"] == besoin), None)
    principale = fm.get("categorie_principale")
    if principale and fm.get("type") != "page" and principale != fm.get("categorie"):
        # catégorie principale propre (ex. « Guides ») : son étape remplace celle de la verticale ;
        # lien vers sa page si site.json → pages_categories la donne
        page = (config.SITE.get("pages_categories") or {}).get(principale)
        etapes.append((principale, f"/{page}/" if page else None))
    elif mere and fm.get("type") != "page" and mere != f"/{fm.get('slug')}/":
        nom = next(v["categorie"] for v in config.VERTICALES if f"/{v['mere']}/" == mere)
        etapes.append((nom, mere))
    court = fm.get("fil_ariane") or re.split(r"\s[:?]\s?|\s—\s", fm.get("h1", ""))[0].strip()
    items = "".join(f'<li><a href="{h}">{e(n)}</a></li>' if h else f"<li>{e(n)}</li>" for n, h in etapes)
    return f'<nav class="bcp-ariane" aria-label="{T["fil_ariane"]}"><ol>{items}<li aria-current="page">{e(court)}</li></ol></nav>'


def initiales(nom):
    return "".join(p[0] for p in nom.split()[:2]).upper()


def avatar(taille):
    if AUTEUR.get("photo"):
        return (f'<img class="bcp-avatar" src="{e(AUTEUR["photo"])}" alt="{e(AUTEUR.get("nom", ""))}" '
                f'width="{taille}" height="{taille}" loading="lazy">')
    return f'<span class="bcp-avatar bcp-avatar--initiales" aria-hidden="true">{e(initiales(AUTEUR.get("nom", "?")))}</span>'


def entete(fm, meta, mots):
    """Fil d'Ariane, H1, puis le cadre auteur : nom, rôle, date de publication, de mise à jour, temps de lecture."""
    h = fil_ariane(fm) + f'<h1 class="bcp-titre">{e(fm.get("h1_jour") or fm.get("h1", ""))}</h1>'
    if fm.get("chapo"):  # accroche sous le H1 (pages d'accueil)
        h += f'<p class="bcp-chapo">{e(fm["chapo"])}</p>'
    dates = []
    pub, mod = meta.get("publication"), meta.get("modification")
    if pub:
        dates.append(f'{T["publie"]} <time datetime="{pub.date().isoformat()}">{date_fr(pub)}</time>')
    if mod and (not pub or mod.date() > pub.date()):
        dates.append(f'{T["mis_a_jour"]} <time datetime="{mod.date().isoformat()}">{date_fr(mod)}</time>')
    dates.append(f"{max(1, round(mots / 200))} {T['lecture']}")
    if AUTEUR.get("nom"):
        nom = e(AUTEUR["nom"])
        if AUTEUR.get("page"):
            nom = f'<a href="{e(AUTEUR["page"])}">{nom}</a>'
        role = f'<span class="bcp-byline__role">{e(AUTEUR["role"])}</span>' if AUTEUR.get("role") else ""
        h += (f'<div class="bcp-byline">{avatar(48)}<div><p class="bcp-byline__nom">{T["par"]} {nom}{role}</p>'
              f'<p class="bcp-byline__dates">{" · ".join(dates)}</p></div></div>')
    else:
        h += f'<p class="bcp-byline__dates bcp-byline--seul">{" · ".join(dates)}</p>'
    # `entete: carte` (pages prix) ou toute autre valeur propre au thème du site (ex. `accueil`) : classe bcp-entete--<valeur>
    variante = re.sub(r"[^a-z0-9-]", "", str(fm.get("entete") or "").lower())
    carte = f" bcp-entete--{variante}" if variante else ""
    return html_bloc(f'<header class="bcp-entete{carte}">{h}</header>')


def encadre_auteur():
    if not AUTEUR.get("nom") or not AUTEUR.get("bio"):
        return None
    lien = (f' <a href="{e(AUTEUR["page"])}">{T["methode"]}</a>' if AUTEUR.get("page") else "")
    role = f'<p class="bcp-auteur__role">{e(AUTEUR["role"])}</p>' if AUTEUR.get("role") else ""
    return html_bloc(f'<aside class="bcp-auteur">{avatar(88)}<div><p class="bcp-auteur__label">{T["a_propos_auteur"]}</p>'
                     f'<p class="bcp-auteur__nom">{e(AUTEUR["nom"])}</p>{role}'
                     f'<p class="bcp-auteur__bio">{e(AUTEUR["bio"])}{lien}</p></div></aside>')


# ---------------------------------------------------------------- blocs du corps
def en_bref(contenu_html):
    return html_bloc(f'<div class="bcp-bref"><p class="bcp-bref__label">{T["en_bref"]}</p>{contenu_html}</div>')


ENCADRES = {"⚠️": ("alerte", T["attention"]), "💡": ("astuce", T["bon_a_savoir"]), "ℹ️": ("info", T["a_savoir"])}


def encadre(sorte, contenu_html):
    classe, label = ENCADRES[sorte]
    return html_bloc(f'<div class="bcp-encadre bcp-encadre--{classe}"><p class="bcp-encadre__label">{label}</p>{contenu_html}</div>')


def sommaire(titres):
    li = "".join(f'<li><a href="#{a}">{t}</a></li>' for a, t in titres)
    label = e(config.SITE.get("sommaire", {}).get("label", T["sommaire"]))
    return html_bloc(f'<nav class="bcp-sommaire" aria-label="{T["sommaire_aria"]}"><p class="bcp-sommaire__label">{label}</p><ol>{li}</ol></nav>')


def chiffres(lignes, inline):
    cartes = "".join(f'<div class="bcp-chiffre"><p class="bcp-chiffre__valeur">{inline(v)}</p><p class="bcp-chiffre__texte">{inline(t)}</p></div>'
                     for v, t in lignes)
    return html_bloc(f'<div class="bcp-chiffres">{cartes}</div>')


def prix_jour(lignes, inline):
    """Carte du prix du jour : la première ligne en grand, les suivantes en repères dessous."""
    (v0, t0), autres = lignes[0], lignes[1:]
    reperes = "".join(f'<li><span class="bcp-prixjour__val">{inline(v)}</span> <span>{inline(t)}</span></li>' for v, t in autres)
    return html_bloc(f'<div class="bcp-prixjour"><p class="bcp-prixjour__valeur">{inline(v0)}</p>'
                     f'<p class="bcp-prixjour__texte">{inline(t0)}</p>'
                     + (f'<ul class="bcp-prixjour__reperes">{reperes}</ul>' if reperes else "") + '</div>')


def faq(titre_html, ancre_id, paires_html):
    items = "".join(f'<details class="bcp-faq__item"><summary>{q}</summary><div class="bcp-faq__reponse"><p>{r}</p></div></details>'
                    for q, r in paires_html)
    return html_bloc(f'<section class="bcp-faq"><h2 id="{ancre_id}" class="wp-block-heading">{titre_html}</h2>{items}</section>')


def sources(contenu_html):
    return html_bloc(f'<p class="bcp-sources">{contenu_html}</p>')


def table(h, avant=None):
    """Tableau ; `avant` = index (1 = 2e colonne) de la colonne mise en avant."""
    cls = f" bcp-table--avant-{avant}" if avant else ""
    return html_bloc(f'<div class="bcp-table{cls}">{h}</div>')


# ---------------------------------------------------------------- composants visuels (design C)
ICO_PLUS = '<svg class="bcp-ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
ICO_MOINS = '<svg class="bcp-ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 12h12"/></svg>'
ICO_NON = '<svg class="bcp-ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>'


def duo(sorte, titres, plus, moins, inline):
    """Deux cartes côte à côte. sorte = « avantages » (plus / moins) ou « checklist » (à faire / à éviter)."""
    t1, t2 = (titres + ["", ""])[:2]
    if sorte == "checklist":
        t1, t2, i1, i2 = t1 or T["a_verifier"], t2 or T["a_eviter"], ICO_PLUS, ICO_NON
    else:
        t1, t2, i1, i2 = t1 or T["avantages"], t2 or T["inconvenients"], ICO_PLUS, ICO_MOINS
    li = lambda items, ico: "".join(f"<li>{ico}<span>{inline(x)}</span></li>" for x in items)
    return html_bloc(f'<div class="bcp-duo bcp-duo--{sorte}"><div class="bcp-duo__plus"><p class="bcp-duo__titre">{e(t1)}</p>'
                     f'<ul>{li(plus, i1)}</ul></div><div class="bcp-duo__moins"><p class="bcp-duo__titre">{e(t2)}</p>'
                     f'<ul>{li(moins, i2)}</ul></div></div>')


def choix(cartes, inline):
    """Cartes de choix : [(mise_en_avant, titre, sous_titre, texte, badge)]."""
    h = ""
    for avant, titre, sous, texte, badge in cartes:
        b = f'<span class="bcp-choix__badge">{e(badge)}</span>' if badge else ""
        h += (f'<div class="bcp-choix__carte{" bcp-choix__carte--avant" if avant else ""}">{b}'
              f'<p class="bcp-choix__titre">{inline(titre)}</p>'
              + (f'<p class="bcp-choix__sous">{inline(sous)}</p>' if sous else "")
              + (f'<p class="bcp-choix__texte">{inline(texte)}</p>' if texte else "") + "</div>")
    return html_bloc(f'<div class="bcp-choix">{h}</div>')


def citation(texte, source, inline):
    cap = f"<figcaption>{inline(source)}</figcaption>" if source else ""
    return html_bloc(f'<figure class="bcp-citation"><blockquote>{inline(texte)}</blockquote>{cap}</figure>')


def avis(texte, inline):
    return html_bloc(f'<aside class="bcp-avis"><p class="bcp-avis__label">{T["notre_avis"]}</p><p>{inline(texte)}</p></aside>')


# ---------------------------------------------------------------- affiliation (sites qui ont "affiliation" dans site.json)
def bouton(url, rel, texte):
    """Bouton vers un outil (::boton @cle | texte). Le style vient du thème du site."""
    return html_bloc(f'<p class="bcp-bouton"><a href="{e(url)}" rel="{rel}" target="_blank">{texte} →</a></p>')


def ficha(nom, infos, plus, moins, url, rel, inline):
    """Fiche d'un outil (::ficha @cle) : lignes « clé | valeur », points forts (+) et limites (-), bouton."""
    lignes = "".join(f"<tr><th>{inline(k)}</th><td>{inline(v)}</td></tr>" for k, v in infos)
    li = lambda xs: "".join(f"<li>{inline(x)}</li>" for x in xs)
    pf = f'<div class="bcp-ficha__plus"><p class="bcp-ficha__label">{T["points_forts"]}</p><ul>{li(plus)}</ul></div>' if plus else ""
    lm = f'<div class="bcp-ficha__moins"><p class="bcp-ficha__label">{T["limites"]}</p><ul>{li(moins)}</ul></div>' if moins else ""
    btn = (f'<p class="bcp-bouton"><a href="{e(url)}" rel="{rel}" target="_blank">{T["voir_offre"]} {e(nom)} →</a></p>'
           if url else "")
    return html_bloc(f'<aside class="bcp-ficha"><p class="bcp-ficha__nom">{e(nom)}</p>'
                     f'<table class="bcp-ficha__infos">{lignes}</table><div class="bcp-ficha__duo">{pf}{lm}</div>{btn}</aside>')


def mention(texte, inline):
    """Mention d'affiliation, sous l'en-tête des articles qui contiennent un lien affilié."""
    return html_bloc(f'<p class="bcp-mention">{inline(texte)}</p>')


# ---------------------------------------------------------------- style
CSS = """
.elementor-location-single:has(.bcp-article) .elementor-widget-theme-post-title,
main.site-main:has(.bcp-article) .page-header{display:none}
.bcp-article{--acc:__accent__;--acc2:__accent_fonce__;--fond:__fond__;--bord:__bord__;--encre:#1f2a24;--doux:#5b645f;--vert:#13221b;
 font-family:__texte__;font-size:17px;line-height:1.72;letter-spacing:normal;color:var(--encre);max-width:760px;margin:0 auto}
.bcp-article p,.bcp-article li,.bcp-article td,.bcp-article th{letter-spacing:normal;font-size:inherit}
.bcp-article a{color:var(--acc);text-decoration:underline;text-underline-offset:3px;text-decoration-thickness:1px}
.bcp-article a:hover{color:var(--acc2);text-decoration-thickness:2px}
.bcp-article h2{font-family:__titres__;font-size:clamp(1.45rem,1.1rem + 1.2vw,1.9rem);line-height:1.25;letter-spacing:.01em;
 color:var(--vert);margin:2.4em 0 .7em;padding-top:.9em;border-top:1px solid var(--bord);scroll-margin-top:90px}
.bcp-article h2::before{content:"";display:block;width:44px;height:4px;border-radius:2px;background:var(--acc);margin:0 0 .7em}
.bcp-article h3{font-family:__texte__;font-size:1.2rem;font-weight:700;letter-spacing:normal;color:var(--vert);margin:1.8em 0 .5em}
.bcp-article strong{color:var(--vert)}
.bcp-entete{margin:0 0 2em}
.bcp-ariane ol{list-style:none;margin:0 0 1.4em;padding:0;display:flex;flex-wrap:wrap;gap:.2em .5em;font-size:.82rem;color:var(--doux)}
.bcp-ariane li{margin:0}.bcp-ariane li+li::before{content:"›";margin-right:.5em;opacity:.6}
.bcp-article .bcp-ariane a{color:var(--doux);text-decoration:none}.bcp-article .bcp-ariane a:hover{color:var(--acc);text-decoration:underline}
.bcp-ariane [aria-current]{color:var(--encre);font-weight:500}
.bcp-article .bcp-titre{font-family:__titres__;font-size:clamp(1.9rem,1.3rem + 2.4vw,2.8rem);line-height:1.15;font-weight:500;
 letter-spacing:.01em;text-transform:none;color:var(--vert);margin:0 0 .7em}
.bcp-byline{display:flex;align-items:center;gap:.9em;padding:.9em 1.1em;background:#fff;border:1px solid var(--bord);border-radius:12px}
.bcp-byline p{margin:0;line-height:1.4}.bcp-byline__nom{font-weight:700;color:var(--vert)}
.bcp-article .bcp-byline__nom a{color:inherit;text-decoration:none}.bcp-article .bcp-byline__nom a:hover{color:var(--acc)}
.bcp-byline__role{display:block;font-weight:400;font-size:.85rem;color:var(--doux)}
.bcp-byline__dates{font-size:.85rem;color:var(--doux)}.bcp-byline--seul{margin:0}
.bcp-avatar{flex:none;width:48px;height:48px;border-radius:50%;object-fit:cover;background:var(--acc);color:#fff;
 display:inline-flex;align-items:center;justify-content:center;font-weight:700;font-size:1rem}
.bcp-bref{position:relative;margin:2em 0;padding:1.6em 1.6em 1.2em;background:linear-gradient(135deg,var(--fond),#fff);
 border:1px solid var(--bord);border-left:6px solid var(--acc);border-radius:14px;box-shadow:0 10px 30px -18px rgba(19,34,27,.45)}
.bcp-bref__label{position:absolute;top:-.85em;left:1.2em;margin:0;padding:.15em .8em;background:var(--acc);color:#fff;
 font-size:.78rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;border-radius:999px}
.bcp-bref ul{list-style:none;margin:0;padding:0}.bcp-bref li{position:relative;padding:0 0 0 1.9em;margin:.55em 0}
.bcp-bref li::before{content:"✓";position:absolute;left:0;top:.05em;width:1.3em;height:1.3em;border-radius:50%;background:var(--acc);
 color:#fff;font-size:.75em;line-height:1.3em;text-align:center;font-weight:700}
.bcp-sommaire{margin:2em 0;padding:1.1em 1.4em;background:#fff;border:1px dashed var(--bord);border-radius:12px}
.bcp-sommaire__label{margin:0 0 .4em;font-weight:700;color:var(--vert);font-size:.9rem;letter-spacing:.08em;text-transform:uppercase}
.bcp-sommaire ol{margin:0;padding-left:1.3em;columns:2 16em;column-gap:2em;font-size:.95rem}
.bcp-sommaire li{margin:.25em 0;break-inside:avoid}.bcp-article .bcp-sommaire a{text-decoration:none;color:var(--encre)}
.bcp-article .bcp-sommaire a:hover{color:var(--acc);text-decoration:underline}
.bcp-encadre{margin:1.8em 0;padding:1.1em 1.3em;border-radius:12px;border:1px solid}
.bcp-encadre p{margin:.3em 0}.bcp-encadre__label{font-weight:700;font-size:.8rem;letter-spacing:.1em;text-transform:uppercase}
.bcp-encadre--alerte{background:#fff4ec;border-color:#f1cdb4}.bcp-encadre--alerte .bcp-encadre__label{color:#a8431a}
.bcp-encadre--astuce{background:#eef6f1;border-color:#c6dfcf}.bcp-encadre--astuce .bcp-encadre__label{color:#1f6b4a}
.bcp-encadre--info{background:#f2f4f7;border-color:#d7dce3}.bcp-encadre--info .bcp-encadre__label{color:#34506b}
.bcp-chiffres{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:1em;margin:2em 0}
.bcp-chiffre{padding:1.1em 1.2em;background:var(--vert);color:#fff;border-radius:14px}
.bcp-chiffre p{margin:0}.bcp-chiffre__valeur{font-family:__titres__;font-size:1.9rem;line-height:1.1;color:#fff}
.bcp-chiffre__valeur strong{color:#fff}.bcp-chiffre__texte{font-size:.88rem;line-height:1.45;opacity:.85;margin-top:.4em!important}
.bcp-article .bcp-chiffre a{color:#fff}
.bcp-table{margin:1.8em 0;overflow-x:auto;border:1px solid var(--bord);border-radius:12px}
.bcp-table figure{margin:0}.bcp-table table{width:100%;border-collapse:collapse;font-size:.93rem;margin:0}
.bcp-table th{background:var(--vert);color:#fff;text-align:left;font-weight:600;padding:.75em .9em;border:0}
.bcp-table td{padding:.7em .9em;border:0;border-top:1px solid var(--bord);vertical-align:top}
.bcp-table tbody tr:nth-child(even) td{background:var(--fond)}
.bcp-article blockquote.wp-block-quote{margin:1.8em 0;padding:.4em 0 .4em 1.2em;border-left:3px solid var(--acc);font-style:italic;color:var(--doux)}
.bcp-faq{margin:2.4em 0}.bcp-faq__item{border:1px solid var(--bord);border-radius:12px;margin:.7em 0;background:#fff;overflow:hidden}
.bcp-faq__item summary{cursor:pointer;list-style:none;padding:1em 3em 1em 1.2em;font-weight:600;color:var(--vert);position:relative}
.bcp-faq__item summary::-webkit-details-marker{display:none}
.bcp-faq__item summary::after{content:"+";position:absolute;right:1em;top:50%;transform:translateY(-50%);width:1.6em;height:1.6em;
 border-radius:50%;background:var(--fond);color:var(--acc);text-align:center;line-height:1.55em;font-size:1.1rem;transition:transform .2s}
.bcp-faq__item[open] summary::after{content:"–"}.bcp-faq__item[open] summary{border-bottom:1px solid var(--bord)}
.bcp-faq__reponse{padding:.2em 1.2em .9em}
.bcp-sources{margin:2.4em 0 0;padding:1em 1.2em;background:var(--fond);border-radius:10px;font-size:.85rem;color:var(--doux)}
.bcp-sources em{font-style:normal}
.bcp-auteur{display:flex;gap:1.3em;align-items:flex-start;margin:2.4em 0 1em;padding:1.5em;background:#fff;border:1px solid var(--bord);
 border-top:4px solid var(--vert);border-radius:14px}
.bcp-auteur .bcp-avatar{width:88px;height:88px;font-size:1.6rem}.bcp-auteur p{margin:0}
.bcp-auteur__label{font-size:.75rem;letter-spacing:.12em;text-transform:uppercase;color:var(--doux)}
.bcp-auteur__nom{font-family:__titres__;font-size:1.35rem;color:var(--vert);margin-top:.15em!important}
.bcp-auteur__role{font-size:.9rem;color:var(--acc);font-weight:600}.bcp-auteur__bio{margin-top:.6em!important;font-size:.95rem}
.bcp-entete--carte{padding:1.4em 1.6em 1.2em;background:#fff;border:1px solid var(--bord);border-radius:16px;margin:0 0 1em}
.bcp-entete--carte .bcp-titre{margin:0 0 .4em}.bcp-entete--carte .bcp-byline{padding:0;border:0;background:none}
.bcp-prixjour{margin:0 0 2em;padding:1.5em 1.6em;background:var(--vert);color:#fff;border-radius:16px;box-shadow:0 14px 34px -20px rgba(19,34,27,.6)}
.bcp-prixjour p{margin:0}.bcp-prixjour__valeur{font-family:__titres__;font-size:clamp(2.4rem,1.6rem + 3vw,3.4rem);line-height:1.05;color:#fff}
.bcp-prixjour__valeur strong{color:#fff}.bcp-prixjour__texte{margin-top:.35em!important;font-size:1rem;opacity:.9}
.bcp-prixjour__reperes{list-style:none;margin:1.1em 0 0;padding:1em 0 0;border-top:1px solid rgba(255,255,255,.2);
 display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:.7em 1.4em;font-size:.88rem;line-height:1.4}
.bcp-prixjour__reperes li{margin:0;opacity:.92}.bcp-prixjour__val{display:block;font-family:__titres__;font-size:1.35rem;color:#fff}
.bcp-article .bcp-prixjour a{color:#fff}
@media (max-width:600px){.bcp-prixjour{padding:1.2em 1.1em}.bcp-entete--carte{padding:1.1em}}
@media (max-width:600px){.bcp-article{font-size:16px}.bcp-auteur{flex-direction:column}.bcp-bref{padding:1.5em 1.1em 1em}}
"""


def css():
    c = CSS
    for k, v in K.items():
        c = c.replace(f"__{k}__", v)
    return c.replace("__titres__", POLICES["titres"]).replace("__texte__", POLICES["texte"]).strip()
