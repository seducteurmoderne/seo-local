"""Client WordPress et rendu Markdown → blocs Gutenberg (moteur commun à tous les sites).

Les articles sources vivent dans articles/*.md ; WordPress n'en reçoit que le rendu.
Au rendu : les liens internes vers des pages non publiées deviennent du texte,
les formulaires de devis n'apparaissent que si le plugin de réception est actif,
les commentaires HTML ne sortent jamais.
"""
import re, json, base64, os, html, hashlib, csv, random, datetime
import urllib.request, urllib.error

import config
import design
from config import ROOT, COULEURS as K, FORM
import prix

V2 = config.SITE.get("design") == 2
MARQUEUR = "[À VÉRIFIER]"


def load_env():
    env = {}
    with open(os.path.join(ROOT, "setup", ".env"), encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


_E = load_env()
URL = _E["WP_URL"].rstrip("/")
USER = _E["WP_USER"]
PW = _E["WP_APP_PASSWORD"].replace(" ", "")


def api(path, method="GET", body=None):
    req = urllib.request.Request(f"{URL}{path}", method=method)
    req.add_header("Authorization", "Basic " + base64.b64encode(f"{USER}:{PW}".encode()).decode())
    req.add_header("User-Agent", config.USER_AGENT)
    if body is not None:
        req.add_header("Content-Type", "application/json")
        req.data = json.dumps(body).encode()
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode())
        except Exception:
            return e.code, None
    except Exception as e:
        return None, {"code": "network", "message": str(e)}


def envoyer_fichier(path, mime):
    """Envoie un fichier dans la médiathèque (corps brut, pas de JSON)."""
    req = urllib.request.Request(f"{URL}/wp-json/wp/v2/media", method="POST", data=open(path, "rb").read())
    req.add_header("Authorization", "Basic " + base64.b64encode(f"{USER}:{PW}".encode()).decode())
    req.add_header("User-Agent", config.USER_AGENT)
    req.add_header("Content-Type", mime)
    req.add_header("Content-Disposition", f'attachment; filename="{os.path.basename(path)}"')
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode())
        except Exception:
            return e.code, None
    except Exception as e:
        return None, {"code": "network", "message": str(e)}


def empreinte(*parts):
    return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()[:16]


# ---------------------------------------------------------------- source
def parse_article(path):
    raw = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    if not m:
        raise ValueError("front-matter absent")
    fm_raw, body = m.group(1), m.group(2)
    fm, key = {}, None
    for line in fm_raw.split("\n"):
        if re.match(r"^\s+-\s", line) and key:
            fm.setdefault(key, []).append(line.strip()[2:].split("#")[0].strip())
        elif ":" in line:
            k, v = line.split(":", 1)
            key = k.strip()
            v = v.strip().strip('"')
            if v:
                fm[key] = v
    body = re.sub(r"^#\s+.*\n", "", body.lstrip("\n"), count=1).strip()
    return fm, body


# ---------------------------------------------------------------- inline
_live = None


def _norm(href):
    h = href.split("#")[0].split("?")[0]
    return h if h.endswith("/") else h + "/"


def _est_en_ligne(href):
    return _live is None or href == "/" or _norm(href) in _live


def lien_outil(cle):
    """Lien vers un outil d'affiliation (affiliation.json) : (href, rel) ou (None, None).
    Lien affilié s'il existe, sinon le site officiel en nofollow. Marque l'article comme affilié."""
    global _affilie
    o = config.OUTILS.get(cle.lstrip("@").lower())
    if not o:
        return None, None
    if o.get("url"):
        _affilie = True
        return o["url"], "sponsored nofollow noopener"
    if o.get("site"):
        return o["site"], "nofollow noopener"
    return None, None


def _lien(m):
    texte, href = m.group(1), m.group(2)
    if href.startswith("@"):
        url, rel = lien_outil(href)
        return f'<a href="{html.escape(url)}" rel="{rel}" target="_blank">{texte}</a>' if url else texte
    if href.startswith("/") and not _est_en_ligne(href):
        return texte
    return f'<a href="{href}">{texte}</a>'


def inline(t):
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", _lien, t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![*\w])\*([^*\n]+?)\*(?![*\w])", r"<em>\1</em>", t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    return t


def _plain(t):
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    t = re.sub(r"[*`_]", "", t)
    return re.sub(r"\s+", " ", t).strip()


# ---------------------------------------------------------------- blocs
def b_para(h):
    return f"<!-- wp:paragraph -->\n<p>{h}</p>\n<!-- /wp:paragraph -->"


def b_head(level, h, ancre=None):
    if ancre:
        return (f'<!-- wp:heading {{"level":{level},"anchor":"{ancre}"}} -->\n'
                f'<h{level} class="wp-block-heading" id="{ancre}">{h}</h{level}>\n<!-- /wp:heading -->')
    return (f'<!-- wp:heading {{"level":{level}}} -->\n'
            f'<h{level} class="wp-block-heading">{h}</h{level}>\n<!-- /wp:heading -->')


def b_sep():
    return '<!-- wp:separator -->\n<hr class="wp-block-separator has-alpha-channel-opacity"/>\n<!-- /wp:separator -->'


def b_list(items):
    inner = "\n".join(f"<!-- wp:list-item -->\n<li>{inline(i)}</li>\n<!-- /wp:list-item -->" for i in items)
    return f'<!-- wp:list -->\n<ul class="wp-block-list">\n{inner}\n</ul>\n<!-- /wp:list -->'


def b_olist(items):
    """Liste numérotée : étapes d'une procédure (format repris par les extraits « liste » de Google)."""
    inner = "\n".join(f"<!-- wp:list-item -->\n<li>{inline(i)}</li>\n<!-- /wp:list-item -->" for i in items)
    return f'<!-- wp:list {{"ordered":true}} -->\n<ol class="wp-block-list">\n{inner}\n</ol>\n<!-- /wp:list -->'


def b_quote(inner_blocks):
    return ('<!-- wp:quote -->\n<blockquote class="wp-block-quote">\n'
            + "\n".join(inner_blocks) + "\n</blockquote>\n<!-- /wp:quote -->")


def b_table(head, rows, avant=None):
    th = "".join(f"<th>{inline(c)}</th>" for c in head)
    body = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows)
    if V2:
        # data-label : l'en-tête de chaque cellule, pour l'affichage en cartes sur téléphone
        lab = lambda j: html.escape(_plain(head[j]), quote=True) if j < len(head) else ""
        body = "".join("<tr>" + "".join(f'<td data-label="{lab(j)}">{inline(c)}</td>' for j, c in enumerate(r)) + "</tr>" for r in rows)
        return design.table(f'<figure class="wp-block-table"><table><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></figure>', avant)
    return ('<!-- wp:table -->\n<figure class="wp-block-table"><table>'
            f"<thead><tr>{th}</tr></thead><tbody>{body}</tbody>"
            "</table></figure>\n<!-- /wp:table -->")


def b_svg(svg_path, caption):
    svg = open(os.path.join(ROOT, svg_path), encoding="utf-8").read().strip()
    svg = re.sub(r"<\?xml[^>]*\?>\s*", "", svg)
    svg = svg.replace("<svg ", '<svg style="width:100%;height:auto;display:block" ', 1)
    cap = f'<figcaption class="wp-element-caption">{inline(caption)}</figcaption>' if caption else ""
    return ('<!-- wp:html -->\n<figure class="wp-block-image" style="margin:2em 0">\n'
            + svg + "\n" + cap + "\n</figure>\n<!-- /wp:html -->")


def b_photo(chemin, caption, alt, fmt=None):
    """Photo déjà envoyée dans la médiathèque (voir images.televerser). Absente du registre : rien.
    fmt : 600 (image descriptive centrée), banniere (3:1) ou large (pleine largeur du texte)."""
    import images
    fmt = fmt or images.FORMAT_DEFAUT
    m = images.registre().get(images.chemin_photo(chemin, fmt))
    if not m:
        return None
    e = html.escape
    cap = f'<figcaption class="wp-element-caption">{inline(caption)}</figcaption>' if caption else ""
    return (f'<!-- wp:html -->\n<figure class="wp-block-image size-full bcp-img bcp-img--{fmt}" style="margin:2em 0">'
            f'<img src="{e(m["url"])}" alt="{e(alt or _plain(caption))}" width="{m["w"]}" height="{m["h"]}" '
            f'class="wp-image-{m["id"]}" loading="lazy" decoding="async" style="width:100%;height:auto"/>'
            + cap + "</figure>\n<!-- /wp:html -->")


VERTICALES = config.CATEGORIE_BESOIN
MERE_VERTICALE = config.MERE_BESOIN
BESOINS = [(b["cle"], b["libelle"]) for b in FORM["besoins"]]
CHAMPS = {b["cle"]: [tuple(c) for c in b.get("champs", [])] for b in FORM["besoins"]}
DELAIS = FORM["delais"]
CP = FORM["code_postal"]
# Textes affichés par le formulaire de devis, en français par défaut. Un site dans une autre langue les
# remplace dans site.json → formulaire.textes (mêmes clés) ; les erreurs du plugin de réception aussi.
TF = {
    "choisir": "Choisir…", "besoin": "Vous avez besoin de", "code_postal": "Code postal", "delai": "Délai",
    "prenom_nom": "Prénom et nom", "prenom": "Prénom", "nom": "Nom", "email": "E-mail", "telephone": "Téléphone",
    "facultatif": "(facultatif)", "precisions": "Précisions", "informations": "Informations",
    "message_simple": "Décrivez votre demande", "confidentialite": "Confidentialité", "site_web": "Site web",
    "cp_aria": "Votre code postal", "continuer": "Continuer",
    "err_besoin": "Cochez au moins un besoin.", "err_nom": "Indiquez votre nom.", "err_prenom": "Indiquez votre prénom.",
    "err_email": "Vérifiez votre adresse e-mail.", "err_tel": "Indiquez un numéro de téléphone pour être rappelé.",
    "err_accord": "Cochez la case d'accord : sans elle, nous ne pouvons pas transmettre votre demande.",
    "envoi": "Envoi…", "err_envoi": "Envoi impossible pour le moment. Réessayez dans un instant.",
    # renvoyées par le plugin de réception (setup/mu-plugins/leads.php)
    "err_expire": "Le formulaire a expiré. Rechargez la page, puis recommencez.",
    "err_trop": "Trop de demandes envoyées depuis votre connexion. Réessayez dans une heure.",
    "err_accord_serveur": "Sans votre accord, nous ne pouvons pas transmettre votre demande.",
}
TF_FR = dict(TF)
TF.update(FORM.get("textes", {}))

CSS_FORM = (
    ".bcp-form{margin:2em 0;padding:1.2em 1.3em;border:1px solid __bord__;border-left:4px solid __accent__;background:__fond__;border-radius:4px}"
    ".bcp-form__titre{margin:0 0 .2em;font-size:1.15em;font-weight:700;line-height:1.3}"
    ".bcp-form__sous{margin:0 0 .9em;opacity:.8;font-size:.92em}.bcp-form__accroche{font-weight:600}"
    ".bcp-form form{display:grid;gap:.75em}"
    ".bcp-form fieldset{border:0;padding:0;margin:0;display:flex;flex-wrap:wrap;gap:.45em 1.1em}"
    ".bcp-form legend{font-weight:600;margin:0 0 .5em;padding:0;width:100%}"
    ".bcp-form .bcp-g{display:grid;grid-template-columns:repeat(auto-fit,minmax(11em,1fr));gap:.6em}"
    ".bcp-form label{display:flex;flex-direction:column;gap:.3em;font-weight:600;font-size:.92em}"
    ".bcp-form label small{font-weight:400;opacity:.7}"
    ".bcp-form fieldset label{flex-direction:row;align-items:center;gap:.45em;font-weight:400;font-size:1em}"
    ".bcp-form input[type=text],.bcp-form input[type=email],.bcp-form input[type=tel],.bcp-form select,.bcp-form textarea"
    "{font:inherit;font-size:.95em;font-weight:400;padding:.5em .65em;border:1px solid __bord_champ__;border-radius:3px;background:#fff;color:__texte_champ__;width:100%;box-sizing:border-box}"
    ".bcp-form .bcp-ok{flex-direction:row;align-items:flex-start;gap:.5em;font-weight:400;font-size:.85em}"
    ".bcp-form .bcp-ok input{margin-top:.2em;flex:none}"
    ".bcp-form button{justify-self:start;background:__accent__;color:#fff;border:0;border-radius:3px;padding:.7em 1.3em;font:inherit;font-weight:600;cursor:pointer}"
    ".bcp-form button:hover{background:__accent_fonce__}.bcp-form button:disabled{opacity:.6;cursor:wait}"
    ".bcp-form [hidden]{display:none!important}"
    ".bcp-form__msg{margin:.8em 0 0;font-weight:600}.bcp-form__msg:empty{display:none}"
    ".bcp-pot{position:absolute!important;left:-9999px!important;width:1px;height:1px;overflow:hidden}"
    ".bcp-demarreur{margin:1.6em 0;padding:.9em 1.1em;border-left:3px solid __accent__;background:__fond__}"
    ".bcp-demarreur p{margin:0 0 .6em}.bcp-demarreur form{display:flex;flex-wrap:wrap;gap:.5em}"
    ".bcp-demarreur input{font:inherit;padding:.55em .7em;border:1px solid __bord_champ__;border-radius:3px;width:9em;background:#fff;color:__texte_champ__}"
    ".bcp-demarreur button{font:inherit;font-weight:600;background:__accent__;color:#fff;border:0;border-radius:3px;padding:.55em 1em;cursor:pointer}"
)
for _cle, _val in K.items():
    CSS_FORM = CSS_FORM.replace(f"__{_cle}__", _val)

JS_FORM = r"""(function(){[].forEach.call(document.querySelectorAll(".bcp-form"),function(r){if(r.getAttribute("data-pret"))return;r.setAttribute("data-pret","1");
var f=r.querySelector("form"),m=r.querySelector(".bcp-form__msg"),b=f.querySelector("button"),lib=b.textContent,t0=Date.now();
function maj(){[].forEach.call(r.querySelectorAll("[data-besoin]"),function(d){var c=f.querySelector('input[name="besoins"][value="'+d.getAttribute("data-besoin")+'"]');d.hidden=!(c&&c.checked);});}
function dit(t,err){m.textContent=t;m.style.color=err?"__ERREUR__":"__SUCCES__";}
f.addEventListener("change",function(e){if(e.target.name==="besoins")maj();});maj();
f.addEventListener("submit",function(e){e.preventDefault();var d={besoins:[],t0:t0,source:location.href,page:document.title};
[].forEach.call(f.elements,function(el){if(!el.name||el.type==="submit")return;if(el.name==="besoins"){if(el.checked)d.besoins.push(el.value);}else if(el.type==="checkbox"){d[el.name]=el.checked;}else{d[el.name]=el.value.trim();}});
[].forEach.call(r.querySelectorAll("[data-besoin]"),function(x){if(x.hidden)[].forEach.call(x.querySelectorAll("select"),function(s){delete d[s.name];});});
if(!d.besoins.length)return dit("Cochez au moins un besoin.",1);
if(!/__CP_REGEX__/.test(d.cp))return dit("__CP_ERREUR__",1);
if(!d.nom)return dit("Indiquez votre nom.",1);
if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(d.email))return dit("Vérifiez votre adresse e-mail.",1);
if(!d.consentement)return dit("Cochez la case d'accord : sans elle, nous ne pouvons pas transmettre votre demande.",1);
b.disabled=true;b.textContent="Envoi…";
fetch(r.getAttribute("data-endpoint"),{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(d)})
.then(function(x){return x.json().then(function(j){return x.ok&&j.ok?j:Promise.reject(j);});})
.then(function(){f.hidden=true;dit("__SUCCES_MSG__",0);})
.catch(function(j){dit((j&&j.message)||"Envoi impossible pour le moment. Réessayez dans un instant.",1);b.disabled=false;b.textContent=lib;});});});
var r=document.querySelector(".bcp-form");if(!r||r.getAttribute("data-demarreur"))return;r.setAttribute("data-demarreur","1");var f=r.querySelector("form");
[].forEach.call(document.querySelectorAll(".bcp-demarreur form"),function(s){s.addEventListener("submit",function(e){e.preventDefault();var v=s.querySelector("input").value.trim(),cp=f.querySelector('[name="cp"]');if(v)cp.value=v;r.scrollIntoView({behavior:"smooth",block:"start"});setTimeout(function(){(v?f.querySelector('[name="nom"]'):cp).focus({preventScroll:true});},600);});});
})();"""
SIMPLE = FORM.get("mode") == "simple"
if SIMPLE:
    # Formulaire simple (site.json → formulaire.mode) : besoin déduit de la page, ni code postal ni délai,
    # prénom, nom, e-mail et téléphone obligatoires.
    for _avant, _apres in (
            ('if(el.checked)d.besoins.push(el.value);', 'if(el.checked||el.type==="hidden")d.besoins.push(el.value);'),
            ('if(!/__CP_REGEX__/.test(d.cp))return dit("__CP_ERREUR__",1);\n', 'if(!d.prenom)return dit("Indiquez votre prénom.",1);\n'),
            ('return dit("Vérifiez votre adresse e-mail.",1);\n',
             'return dit("Vérifiez votre adresse e-mail.",1);\n'
             'if(!/^[+0-9 ().\\/-]{8,}$/.test(d.tel||""))return dit("Indiquez un numéro de téléphone pour être rappelé.",1);\n')):
        assert _avant in JS_FORM, _avant
        JS_FORM = JS_FORM.replace(_avant, _apres)
JS_FORM = (JS_FORM.replace("__ERREUR__", K["accent"]).replace("__SUCCES__", K["succes"])
           .replace("__CP_REGEX__", CP["regex"]).replace("__CP_ERREUR__", CP["erreur"])
           .replace("__SUCCES_MSG__", FORM["succes"]))
for _cle in ("err_besoin", "err_nom", "err_prenom", "err_email", "err_tel", "err_accord", "envoi", "err_envoi"):
    if TF[_cle] != TF_FR[_cle]:
        JS_FORM = JS_FORM.replace(json.dumps(TF_FR[_cle], ensure_ascii=False), json.dumps(TF[_cle], ensure_ascii=False))


def _select(name, label, options):
    opts = f'<option value="">{html.escape(TF["choisir"])}</option>' + "".join(f"<option>{html.escape(o)}</option>" for o in options)
    return f'<label>{html.escape(label)}<select name="{name}">{opts}</select></label>'


_nform = 0


def b_formulaire(verticale, titre, sous="", bouton=FORM["bouton"]):
    """Formulaire de devis. Si site.json → formulaire.titre existe, il devient le titre de tous les
    formulaires, et le titre écrit dans l'article passe en accroche juste en dessous."""
    global _nform
    e = html.escape
    _nform += 1
    ident = ' id="bcp-demande"' if _nform == 1 else ""
    if SIMPLE:
        return b_formulaire_simple(verticale or BESOINS[0][0], titre, ident, bouton)
    if FORM.get("titre"):
        entete = (f'<p class="bcp-form__titre">{e(FORM["titre"])}</p>'
                  f'<p class="bcp-form__sous"><span class="bcp-form__accroche">{e(titre)}</span>'
                  + (f" {e(sous)}" if sous else "") + "</p>")
    else:
        entete = f'<p class="bcp-form__titre">{e(titre)}</p>' + (f'<p class="bcp-form__sous">{e(sous)}</p>' if sous else "")
    cases = "".join(f'<label><input type="checkbox" name="besoins" value="{k}"{" checked" if k == verticale else ""}> {e(l)}</label>'
                    for k, l in BESOINS)
    details = "".join(f'<div class="bcp-g" data-besoin="{k}">' + "".join(_select(n, l, o) for n, l, o in CHAMPS[k]) + "</div>"
                      for k, _ in BESOINS)
    h = (f'<div class="bcp-form"{ident} data-endpoint="{FORM["endpoint"]}">'
         + entete
         + '<form novalidate>'
         f'<fieldset><legend>{e(TF["besoin"])}</legend>{cases}</fieldset>{details}'
         f'<div class="bcp-g"><label>{e(TF["code_postal"])}<input type="text" name="cp" inputmode="numeric" maxlength="{CP["longueur"]}" autocomplete="postal-code" placeholder="{CP["exemple"]}"></label>'
         + _select("delai", TF["delai"], DELAIS) + '</div>'
         f'<div class="bcp-g"><label>{e(TF["prenom_nom"])}<input type="text" name="nom" autocomplete="name"></label>'
         f'<label>{e(TF["email"])}<input type="email" name="email" autocomplete="email"></label>'
         f'<label><span>{e(TF["telephone"])} <small>{e(TF["facultatif"])}</small></span><input type="tel" name="tel" autocomplete="tel"></label></div>'
         f'<label><span>{e(TF["precisions"])} <small>{e(TF["facultatif"])}</small></span><textarea name="message" rows="2"></textarea></label>'
         f'<label class="bcp-pot" aria-hidden="true">{e(TF["site_web"])}<input type="text" name="site_web" tabindex="-1" autocomplete="off"></label>'
         f'<label class="bcp-ok"><input type="checkbox" name="consentement"><span>{FORM["consentement"]} '
         f'<a href="{FORM["politique"]}">{e(TF["confidentialite"])}</a></span></label>'
         f'<button type="submit">{e(bouton)} →</button></form>'
         '<p class="bcp-form__msg" role="status" aria-live="polite"></p></div>')
    return "<!-- wp:html -->\n" + h + "\n<style>" + CSS_FORM + "</style>\n<script>" + JS_FORM + "</script>\n<!-- /wp:html -->"


def b_formulaire_simple(verticale, titre, ident, bouton):
    """Formulaire simple : le titre écrit dans l'article (« Un élagage à faire ? … »), le sous-titre de
    site.json → formulaire.sous_titre, puis prénom, nom, e-mail, téléphone et un message facultatif."""
    e = html.escape
    sous = FORM.get("sous_titre", "")
    h = (f'<div class="bcp-form"{ident} data-endpoint="{FORM["endpoint"]}">'
         f'<p class="bcp-form__titre">{e(titre)}</p>' + (f'<p class="bcp-form__sous">{e(sous)}</p>' if sous else "")
         + '<form novalidate>'
         f'<input type="hidden" name="besoins" value="{e(verticale)}">'
         f'<div class="bcp-g"><label>{e(TF["prenom"])}<input type="text" name="prenom" autocomplete="given-name"></label>'
         f'<label>{e(TF["nom"])}<input type="text" name="nom" autocomplete="family-name"></label></div>'
         f'<div class="bcp-g"><label>{e(TF["email"])}<input type="email" name="email" autocomplete="email"></label>'
         f'<label>{e(TF["telephone"])}<input type="tel" name="tel" autocomplete="tel"></label></div>'
         f'<label><span>{e(TF["informations"])} <small>{e(TF["facultatif"])}</small></span>'
         f'<textarea name="message" rows="3" placeholder="{e(FORM.get("placeholder_message", TF["message_simple"]))}"></textarea></label>'
         f'<label class="bcp-pot" aria-hidden="true">{e(TF["site_web"])}<input type="text" name="site_web" tabindex="-1" autocomplete="off"></label>'
         f'<label class="bcp-ok"><input type="checkbox" name="consentement"><span>{FORM["consentement"]} '
         f'<a href="{FORM["politique"]}">{e(TF["confidentialite"])}</a></span></label>'
         f'<button type="submit">{e(bouton)} →</button></form>'
         '<p class="bcp-form__msg" role="status" aria-live="polite"></p></div>')
    return "<!-- wp:html -->\n" + h + "\n<style>" + CSS_FORM + "</style>\n<script>" + JS_FORM + "</script>\n<!-- /wp:html -->"


def b_demarreur(question, lien):
    e = html.escape
    return ("<!-- wp:html -->\n"
            f'<div class="bcp-demarreur"><p><strong>{e(question)}</strong> {e(lien)} :</p>'
            f'<form><input type="text" inputmode="numeric" maxlength="{CP["longueur"]}" placeholder="{e(TF["code_postal"])}" aria-label="{e(TF["cp_aria"])}">'
            f'<button type="submit">{e(TF["continuer"])} →</button></form></div>'
            "\n<!-- /wp:html -->")


# Titres de section FAQ et débuts de ligne de sources reconnus (site.json → "textes" pour une autre langue)
FAQ_RE = "|".join(re.escape(t) for t in design.T["faq"])
SOURCES_DEBUTS = tuple("*" + t for t in design.T["sources"])


def faq_pairs(body):
    m = re.search(r"^##\s+(?:" + FAQ_RE + r")[^\n]*\n(.*?)(?=^##\s|\Z)", body, re.M | re.S)
    if not m:
        return []
    pairs = []
    for para in re.split(r"\n\s*\n", m.group(1)):
        mm = re.match(r"^\s*\*\*(.+?)\*\*\s*\n(.+)$", para.strip(), re.S)
        if mm:
            pairs.append((_plain(mm.group(1)), _plain(mm.group(2))))
    return pairs


def b_faq_jsonld(pairs):
    data = {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]}
    js = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    return f'<!-- wp:html -->\n<script type="application/ld+json">{js}</script>\n<!-- /wp:html -->'


def b_service_jsonld(fm, svc):
    """Service : la prestation de la page (besoin), sa zone (la ville, sinon celle du site) et l'organisation."""
    libelles = {b["cle"]: b["libelle"] for b in config.FORM.get("besoins", [])}
    zone = {"@type": "City", "name": fm["ville"]} if fm.get("ville") else svc.get("zone")
    data = {"@context": "https://schema.org", "@type": "Service", "name": fm.get("h1", ""),
            "serviceType": libelles.get(fm["besoin"], fm["besoin"]),
            "url": f"{URL}/{fm.get('slug', '')}/", "description": fm.get("meta_description", "")}
    if zone:
        data["areaServed"] = zone
    if svc.get("organisation"):
        data["provider"] = {"@id": svc["organisation"]}
    js = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    return f'<!-- wp:html -->\n<script type="application/ld+json">{js}</script>\n<!-- /wp:html -->'


# ---------------------------------------------------------------- maillage généré
VERT_CSV = config.CATEGORIE_SITEMAP
MERE_CSV = config.MERE_SITEMAP


def _filles(verticale):
    """Guides d'une verticale dans l'ordre de la sitemap : [(slug, titre, cluster)]."""
    out = []
    with open(os.path.join(ROOT, "strategie", "sitemap-urls.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            # mères, mères locales et villes sont liées dans le texte : pas dans la liste des guides
            if r["verticale"] == verticale and r["role"] not in ("mère", "mère locale", "ville"):
                out.append((r["url"].strip("/"), r["titre"], r["cluster"]))
    return out


def b_guides(verticale):
    """Page mère : ses guides en ligne, groupés par intention."""
    groupes = {}
    for slug, titre, cluster in _filles(verticale):
        if _est_en_ligne(f"/{slug}/"):
            groupes.setdefault(re.sub(r"^[A-Z]\s*·\s*", "", cluster).strip(), []).append(f"[{titre}](/{slug}/)")
    blocs = []
    for nom, liens in groupes.items():
        blocs.append(b_para(f"<strong>{html.escape(nom, quote=False)}</strong>"))
        blocs.append(b_list(liens))
    return blocs


# Habillage porté par le contenu lui-même (couleur des liens, fond de page…), propre au thème
# de chaque site : site.json → "habillage_css". Vide : aucun style ajouté.
CSS_HABILLAGE = config.SITE.get("habillage_css", "")


def b_habillage(blocs):
    if V2 and config.SITE.get("theme"):
        css = ""  # le thème du site porte le style des articles (theme/site.css, envoyé par `autopilote.py theme`)
    else:
        css = (design.css() + CSS_HABILLAGE) if V2 else CSS_HABILLAGE
    style = ("<!-- wp:html -->\n<style>" + css + "</style>\n<!-- /wp:html -->\n\n") if css else ""
    return (style +
            '<!-- wp:group {"className":"bcp-article"} -->\n<div class="wp-block-group bcp-article">\n\n'
            + blocs + "\n\n</div>\n<!-- /wp:group -->")


def _citation_html(block):
    """Contenu d'une citation Markdown en HTML simple (paragraphes, listes), sans balises Gutenberg."""
    out, j = [], 0
    while j < len(block):
        b = block[j].strip()
        if not b or re.match(r"^#{1,6}\s", b):
            j += 1
            continue
        if b.startswith("- "):
            items = []
            while j < len(block) and block[j].strip().startswith("- "):
                items.append(f"<li>{inline(block[j].strip()[2:])}</li>")
                j += 1
            out.append("<ul>" + "".join(items) + "</ul>")
            continue
        para = [b]
        j += 1
        while j < len(block) and block[j].strip() and not block[j].strip().startswith(("-", "#")):
            para.append(block[j].strip())
            j += 1
        out.append(f"<p>{inline(' '.join(para))}</p>")
    return "".join(out)


def _citation_v2(block):
    """En bref, encadré d'alerte ou d'astuce ; None pour une citation ordinaire."""
    titres = [re.sub(r"^#+\s*", "", b.strip()) for b in block if re.match(r"^\s*#{1,6}\s", b)]
    if titres and titres[0].lower() == "en bref":
        return design.en_bref(_citation_html(block))
    premier = next((b.strip() for b in block if b.strip()), "")
    for sorte in design.ENCADRES:
        if premier.startswith(sorte):
            reste = [premier[len(sorte):].strip()] + block[block.index(next(b for b in block if b.strip())) + 1:]
            return design.encadre(sorte, _citation_html(reste))
    return None


_QR = re.compile(r"^\s*\*\*(.+?)\*\*\s*\n(.+)$", re.S)
_FIN_PARA = re.compile(r"^\s*(#{2,4}\s|[-|>]|<!--|::|!\[\[|→|\d+\.\s)")


_affilie = False


def render(body, live=None, fm=None, formulaires=False, meta=None):
    """Rendu Gutenberg. `live` = chemins publiés ("/slug/") ; None = tout considérer en ligne.
    `formulaires` = le plugin de réception des demandes est actif (sinon aucun formulaire n'est rendu).
    `meta` (design v2) = {"publication": datetime, "modification": datetime|None} pour le cadre auteur."""
    global _live, _nform, _affilie
    _live = set(live) if live is not None else None
    _nform = 0
    _affilie = False
    body = prix.remplacer(body)
    fm = fm or {}
    titres_h2, premier_h2 = [], None
    verticale = fm.get("besoin") or VERTICALES.get(fm.get("categorie", ""), MERE_VERTICALE.get(fm.get("slug", ""), ""))
    avec_form = formulaires and "::cta-fort" in body
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    lines = body.split("\n")
    out, i = [], 0
    while i < len(lines):
        s = lines[i].strip()
        if not s:
            i += 1
            continue
        if s.startswith(">"):
            block = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                block.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            if V2:
                special = _citation_v2(block)
                if special:
                    out.append(special)
                    continue
            inner, j = [], 0
            while j < len(block):
                b = block[j].strip()
                if not b:
                    j += 1
                    continue
                m = re.match(r"^(#{1,6})\s+(.*)$", b)
                if m:
                    inner.append(b_head(min(len(m.group(1)) + 1, 4), inline(m.group(2))))
                    j += 1
                    continue
                if b.startswith("- "):
                    items = []
                    while j < len(block) and block[j].strip().startswith("- "):
                        items.append(block[j].strip()[2:])
                        j += 1
                    inner.append(b_list(items))
                    continue
                para = [b]
                j += 1
                while j < len(block) and block[j].strip() and not block[j].strip().startswith(("-", "#")):
                    para.append(block[j].strip())
                    j += 1
                inner.append(b_para(inline(" ".join(para))))
            out.append(b_quote(inner))
            continue
        m = re.match(r"^(#{2,4})\s+(.*)$", s)
        if m and V2 and len(m.group(1)) == 2:
            titre, a = inline(m.group(2)), design.ancre(_plain(m.group(2)))
            if premier_h2 is None:
                premier_h2 = len(out)
            titres_h2.append((a, titre))
            i += 1
            if re.match(r"^(" + FAQ_RE + ")", m.group(2)):
                paires = []
                while i < len(lines):
                    while i < len(lines) and not lines[i].strip():
                        i += 1
                    k = i
                    while k < len(lines) and lines[k].strip():
                        k += 1
                    mm = _QR.match("\n".join(l.strip() for l in lines[i:k]))
                    if not mm:
                        break
                    paires.append((inline(mm.group(1)), inline(" ".join(mm.group(2).split("\n")))))
                    i = k
                out.append(design.faq(titre, a, paires))
            else:
                out.append(b_head(2, titre, a))
            continue
        if m:
            out.append(b_head(len(m.group(1)), inline(m.group(2))))
            i += 1
            continue
        if re.match(r"^-{3,}$", s):
            out.append(b_sep())
            i += 1
            continue
        if s.startswith("::table-rotative"):
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
            if i < len(lines) and lines[i].strip().startswith("|") and i + 1 < len(lines) \
                    and re.match(r"^\|[\s:|-]+\|$", lines[i + 1].strip()):
                head = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                i += 2
                rows = []
                while i < len(lines) and lines[i].strip().startswith("|"):
                    rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                    i += 1
                rnd = random.Random(f"{datetime.date.today().isoformat()}|{fm.get('slug', '')}")
                rnd.shuffle(rows)
                out.append(b_table(head, rows))
            continue
        if s.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|$", lines[i + 1].strip()):
            head = [c.strip() for c in s.strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            out.append(b_table(head, rows))
            continue
        if s.startswith("- "):
            items = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                items.append(lines[i].strip()[2:])
                i += 1
            out.append(b_list(items))
            continue
        if re.match(r"^\d+\.\s", s):
            items = []
            while i < len(lines) and re.match(r"^\s*\d+\.\s", lines[i]):
                items.append(re.sub(r"^\s*\d+\.\s+", "", lines[i]))
                i += 1
            out.append(b_olist(items))
            continue
        m = re.match(r"^!\[\[(.+?)\]\]$", s)
        if m:
            import images
            chemin, legende, alt, fmt = images.appel_image(m.group(1))
            if chemin.lower().endswith(".svg"):
                out.append(b_svg(chemin, legende))
            else:
                bloc = b_photo(chemin, legende, alt, fmt)
                if bloc:
                    out.append(bloc)
            i += 1
            continue
        if s.startswith("::prix-jour"):
            i += 1
            rangs = []
            while i < len(lines) and lines[i].strip() and "|" in lines[i]:
                v, _, txt = lines[i].strip().partition("|")
                rangs.append((v.strip(), txt.strip()))
                i += 1
            if rangs:
                out.append(design.prix_jour(rangs, inline) if V2 else
                           b_table(["Prix", "Ce qu'il mesure"], [[v, txt] for v, txt in rangs]))
            continue
        if s.startswith("::chiffres"):
            i += 1
            rangs = []
            while i < len(lines) and lines[i].strip() and "|" in lines[i]:
                v, _, txt = lines[i].strip().partition("|")
                rangs.append((v.strip(), txt.strip()))
                i += 1
            if rangs:
                out.append(design.chiffres(rangs, inline) if V2 else
                           b_table(["Chiffre", "Ce qu'il signifie"], [[v, txt] for v, txt in rangs]))
            continue
        if re.match(r"^::(avantages|checklist)\b", s):
            sorte = "checklist" if s.startswith("::checklist") else "avantages"
            titres = [x.strip() for x in s.split(None, 1)[1].split("|")] if len(s.split(None, 1)) > 1 else []
            i += 1
            plus, moins = [], []
            while i < len(lines) and lines[i].strip():
                l = lines[i].strip()
                if l.startswith("+ "):
                    plus.append(l[2:].strip())
                elif l.startswith("- "):
                    moins.append(l[2:].strip())
                i += 1
            if V2:
                out.append(design.duo(sorte, titres, plus, moins, inline))
            else:
                for t, items in ((titres[0] if titres else "Avantages", plus), (titres[1] if len(titres) > 1 else "Inconvénients", moins)):
                    out += [b_para(f"<strong>{inline(t)}</strong>"), b_list(items)]
            continue
        if s.startswith("::choix"):
            i += 1
            cartes = []
            while i < len(lines) and lines[i].strip() and "|" in lines[i]:
                l = lines[i].strip()
                parts = [x.strip() for x in l.lstrip("*").strip().split("|")] + ["", "", "", ""]
                cartes.append((l.startswith("*"), parts[0], parts[1], parts[2], parts[3]))
                i += 1
            if cartes:
                out.append(design.choix(cartes, inline) if V2 else
                           b_table(["Option", "Repère", "Pour qui"], [[c[1], c[2], c[3]] for c in cartes]))
            continue
        if s.startswith("::boton"):
            cle, _, texte = s[len("::boton"):].strip().partition("|")
            url, rel = lien_outil(cle.strip())
            if url:
                out.append(design.bouton(url, rel, inline(texte.strip() or config.OUTILS[cle.strip().lstrip("@").lower()]["nom"])))
            i += 1
            continue
        if s.startswith("::ficha"):
            cle = s[len("::ficha"):].strip().lstrip("@").lower()
            i += 1
            infos, plus, moins = [], [], []
            while i < len(lines) and lines[i].strip():
                l = lines[i].strip()
                if l.startswith("+ "):
                    plus.append(l[2:].strip())
                elif l.startswith("- "):
                    moins.append(l[2:].strip())
                elif "|" in l:
                    k, _, v = l.partition("|")
                    infos.append((k.strip(), v.strip()))
                i += 1
            o = config.OUTILS.get(cle)
            if o:
                url, rel = lien_outil(cle)
                out.append(design.ficha(o["nom"], infos, plus, moins, url, rel, inline))
            continue
        if s.startswith("::citation"):
            t, _, src = s[len("::citation"):].partition("|")
            out.append(design.citation(t.strip(), src.strip(), inline) if V2 else b_quote([b_para(inline(t.strip()))]))
            i += 1
            continue
        if s.startswith("::avis"):
            t = s[len("::avis"):].strip()
            out.append(design.avis(t, inline) if V2 else b_para(f"<strong>Notre avis.</strong> {inline(t)}"))
            i += 1
            continue
        if s.startswith("::tableau"):
            m_av = re.search(r"\d+", s)
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
            if i + 1 < len(lines) and lines[i].strip().startswith("|") and re.match(r"^\|[\s:|-]+\|$", lines[i + 1].strip()):
                head = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                i += 2
                rows = []
                while i < len(lines) and lines[i].strip().startswith("|"):
                    rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                    i += 1
                out.append(b_table(head, rows, int(m_av.group()) if m_av else None))
            continue
        if s.startswith("::guides"):
            out.extend(b_guides(MERE_CSV.get(fm.get("slug", ""), s[len("::guides"):].strip())))
            i += 1
            continue
        if s.startswith("::a-lire-aussi"):
            i += 1  # supprimé : les liens internes vivent dans les phrases, jamais en bloc
            continue
        if s.startswith("::cta-doux"):
            p = [x.strip() for x in s[len("::cta-doux"):].split("|")]
            if avec_form and len(p) >= 2:
                out.append(b_demarreur(p[0], p[1]))
            i += 1
            continue
        if s.startswith("::cta-fort"):
            p = [x.strip() for x in s[len("::cta-fort"):].split("|")]
            if formulaires and p[0]:
                out.append(b_formulaire(verticale, p[0], p[1] if len(p) > 1 else "",
                                        p[2] if len(p) > 2 and p[2] else FORM["bouton"]))
            i += 1
            continue
        if s.startswith("→"):
            i += 1  # supprimé : pas de ligne de renvoi, les liens vivent dans les phrases
            while i < len(lines) and lines[i].strip() and not _FIN_PARA.match(lines[i]):
                i += 1
            continue
        para = [s]
        i += 1
        while i < len(lines) and lines[i].strip() and not _FIN_PARA.match(lines[i]):
            para.append(lines[i].strip())
            i += 1
        texte = " ".join(para)
        if V2 and texte.startswith(SOURCES_DEBUTS):
            out.append(design.sources(inline(texte.strip("*"))))
        else:
            out.append(b_para(inline(texte)))
    if V2:
        if len(titres_h2) >= 4 and premier_h2 is not None:
            # site.json → "sommaire": {"position": "apres_en_bref"} : sommaire juste sous l'« En bref », avant l'intro
            pos = premier_h2
            if config.SITE.get("sommaire", {}).get("position") == "apres_en_bref":
                pos = next((k + 1 for k, b in enumerate(out) if 'class="bcp-bref"' in b), premier_h2)
            out.insert(pos, design.sommaire(titres_h2))
        mots = len(re.sub(r"[#>*|`]", " ", body).split())
        out.insert(0, design.entete(fm, meta or {}, mots))
        if _affilie and config.AFFILIATION.get("mention"):
            out.insert(1, design.mention(config.AFFILIATION["mention"], inline))
        auteur = design.encadre_auteur()
        if auteur:
            out.append(auteur)
    if fm.get("schema") == "FAQPage":
        pairs = faq_pairs(body)
        if len(pairs) >= 2:
            out.append(b_faq_jsonld(pairs))
    # site.json → "schema_service" : balisage Service (absent = rien, rendu des autres sites inchangé)
    svc = config.SITE.get("schema_service")
    if svc and fm.get("besoin") and fm.get("slug") not in svc.get("exclure", []):
        out.append(b_service_jsonld(fm, svc))
    _live = None
    return b_habillage(prix.jour_html("\n\n".join(out)))
