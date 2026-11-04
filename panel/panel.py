#!/usr/bin/env python3
"""Panel de suivi du parc : une ligne par site et la liste des demandes de devis de tous les sites.

    python3 panel/panel.py [port]        puis ouvrir http://127.0.0.1:8765

Lecture seule : le panel lit WordPress (accès de setup/.env de chaque site), le plugin de devis (route /suivi,
version 2) et les relevés Search Console (gsc/*.json, commande `autopilote.py gsc`). Il ne modifie rien.
Il n'écoute que sur la machine (127.0.0.1). Les demandes n'y portent ni nom, ni e-mail, ni téléphone.
Chacun le lance sur sa machine : il montre les sites de sites/ dont il a les accès.
"""
import os, re, sys, csv, io, json, time, base64, threading, datetime as dt, urllib.request, urllib.parse, urllib.error
from concurrent.futures import ThreadPoolExecutor
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

ICI = os.path.dirname(os.path.abspath(__file__))
SITES = os.path.join(os.path.dirname(ICI), "sites")
PERIODE_JOURS = 28
# Seuils Search Console : les mêmes que moteur/gsc.py (SEUILS), réglables par site dans site.json → "search_console_seuils"
SEUILS_GSC = {"impressions_min": 30, "renforcer_de": 8, "renforcer_a": 20, "ranke_position": 10}
UTC = dt.timezone.utc


# ---------------------------------------------------------------- lecture d'un site
def lire_env(dossier):
    """WP_URL, WP_USER, WP_APP_PASSWORD de setup/.env, ou None. Jamais affichés."""
    chemin = os.path.join(dossier, "setup", ".env")
    if not os.path.exists(chemin):
        return None
    env = {}
    with open(chemin, encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.strip()
            if ligne and not ligne.startswith("#") and "=" in ligne:
                k, v = ligne.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    if not all(env.get(k) for k in ("WP_URL", "WP_USER", "WP_APP_PASSWORD")):
        return None
    return env


class WP:
    def __init__(self, env, user_agent):
        self.url = env["WP_URL"].rstrip("/")
        jeton = f"{env['WP_USER']}:{env['WP_APP_PASSWORD'].replace(' ', '')}"
        self.auth = "Basic " + base64.b64encode(jeton.encode()).decode()
        self.ua = user_agent

    def get(self, chemin, auth=True):
        """(statut, données, en-têtes). Une seconde tentative après une erreur passagère (réseau, 5xx)."""
        s, r, h = self._get(chemin, auth)
        if s is None or s >= 500:
            time.sleep(3)
            s, r, h = self._get(chemin, auth)
        return s, r, h

    def _get(self, chemin, auth):
        req = urllib.request.Request(self.url + chemin)
        req.add_header("User-Agent", self.ua)
        if auth:
            req.add_header("Authorization", self.auth)
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status, json.loads(r.read().decode()), r.headers
        except urllib.error.HTTPError as e:
            return e.code, None, e.headers
        except Exception as e:
            return None, {"erreur": str(e)}, {}

    def contenus(self, kind):
        """Tous les articles ou pages, sans leur texte (slug, statut, date)."""
        out, page = [], 1
        while True:
            s, items, h = self.get(f"/wp-json/wp/v2/{kind}?per_page=100&page={page}&status=any&context=edit"
                                   "&_fields=id,slug,status,date_gmt")
            if s != 200:
                return None, s
            out += items
            if page >= int(h.get("X-WP-TotalPages") or 1):
                return out, 200
            page += 1


def file_attente(dossier):
    chemin = os.path.join(dossier, "autopilote", "file-attente.txt")
    if not os.path.exists(chemin):
        return []
    out = []
    with open(chemin, encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.split("#")[0].strip()
            if ligne:
                out.append(ligne.split()[0])
    return out


def lire_json(chemin, defaut=None):
    try:
        with open(chemin, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return defaut


def releves_gsc(dossier):
    d = os.path.join(dossier, "gsc")
    if not os.path.isdir(d):
        return []
    return [lire_json(os.path.join(d, f)) for f in sorted(os.listdir(d)) if re.match(r"\d{4}-\d{2}-\d{2}\.json$", f)]


def resume_gsc(releves, seuils):
    """Clics, impressions, position moyenne, pages qui rankent et à renforcer du dernier relevé ; évolution des clics
    par rapport au relevé précédent qui ne chevauche pas sa période. Même calcul que moteur/gsc.py (analyser)."""
    releves = [r for r in releves if r and r.get("pages") is not None]
    if not releves:
        return None
    r = releves[-1]
    pages = r["pages"].values()
    impressions = sum(p["impressions"] for p in pages)
    pos = sum((p["position"] or 0) * p["impressions"] for p in pages)
    out = {"debut": r["debut"], "fin": r["fin"], "clics": sum(p["clics"] for p in pages), "impressions": impressions,
           "position": round(pos / impressions, 1) if impressions else None,
           "rankent": sum(1 for p in pages if p["position"] is not None and p["position"] <= seuils["ranke_position"]
                          and p["clics"] > 0),
           "renforcer": sum(1 for p in pages if p["position"] is not None
                            and not (p["position"] <= seuils["ranke_position"] and p["clics"] > 0)
                            and seuils["renforcer_de"] <= p["position"] <= seuils["renforcer_a"]
                            and p["impressions"] >= seuils["impressions_min"]),
           "clics_avant": None}
    precedents = [x for x in releves[:-1] if x["fin"] < r["debut"]]
    if precedents:
        out["clics_avant"] = sum(p["clics"] for p in precedents[-1]["pages"].values())
    return out


def chemin_page(url):
    return urllib.parse.urlparse(url or "").path.strip("/") or "/"


def lire_site(nom):
    dossier = os.path.join(SITES, nom)
    conf = lire_json(os.path.join(dossier, "site.json"), {})
    env = lire_env(dossier)
    form = conf.get("formulaire", {})
    libelles = {b["cle"]: b.get("libelle_court", b.get("libelle", b["cle"])) for b in form.get("besoins", [])}
    seuils = {**SEUILS_GSC, **conf.get("search_console_seuils", {})}
    etat = lire_json(os.path.join(dossier, "autopilote", "etat.json"), {})
    site = {"nom": nom, "domaine": conf.get("nom") or nom, "alertes": [], "demandes": None, "wp": None,
            "gsc": resume_gsc(releves_gsc(dossier), seuils), "rythme": conf.get("publication", {})}
    if not env:
        site["alertes"].append("pas d'accès WordPress sur cette machine (setup/.env absent)")
        return site
    site["domaine"] = urllib.parse.urlparse(env["WP_URL"]).hostname or site["domaine"]
    wp = WP(env, conf.get("user_agent", "Mozilla/5.0"))
    posts, s1 = wp.contenus("posts")
    pages, s2 = wp.contenus("pages")
    if posts is None or pages is None:
        s = s1 if posts is None else s2
        site["alertes"].append(f"WordPress refuse la connexion (HTTP {s})" if s in (401, 403)
                               else f"WordPress injoignable (HTTP {s})")
        return site
    tous = posts + pages
    statut = {p["slug"]: p["status"] for p in tous}
    futurs = sorted(p["date_gmt"] for p in tous if p["status"] == "future")
    restant = [s for s in file_attente(dossier)
               if statut.get(s) not in ("publish", "future") and (etat.get(s) or {}).get("statut") != "bloqué"]
    site["wp"] = {"en_ligne": sum(p["status"] == "publish" for p in tous), "programmes": len(futurs),
                  "programme_jusqu_au": futurs[-1][:10] if futurs else None, "file": len(restant)}
    if not futurs:
        site["alertes"].append("rien de programmé")

    endpoint = form.get("endpoint")
    politique = (form.get("politique") or "").strip("/")
    if endpoint:
        s_plugin, _, _ = wp.get(endpoint, auth=False)
        if s_plugin != 200 or (politique and statut.get(politique) != "publish"):
            site["alertes"].append("formulaires masqués (plugin ou page de confidentialité absents)")
        s, r, _ = wp.get(endpoint.rstrip("/") + "/suivi")
        if s == 200 and isinstance(r, dict):
            site["demandes"] = []
            for d in r.get("demandes", []):
                site["demandes"].append({"site": nom, "date": d.get("date", ""), "page": chemin_page(d.get("source")),
                                         "besoins": [libelles.get(b, b) for b in d.get("besoins") or []],
                                         "cp": d.get("cp", ""), "delai": d.get("delai", "")})
        elif s == 404:
            site["alertes"].append("plugin de devis à mettre à jour (version 2) pour compter les demandes")
        else:
            site["alertes"].append(f"demandes illisibles (HTTP {s})")
    return site


# ---------------------------------------------------------------- parc
def noms_sites():
    if not os.path.isdir(SITES):
        return []
    return sorted(n for n in os.listdir(SITES) if os.path.exists(os.path.join(SITES, n, "site.json")))


def date_demande(d):
    try:
        return dt.datetime.fromisoformat(d["date"]).astimezone(UTC)
    except (ValueError, KeyError):
        return None


def stats_demandes(demandes, maintenant):
    if demandes is None:
        return None
    dates = [x for x in (date_demande(d) for d in demandes) if x]
    return {"total": len(demandes), "periode": sum(1 for x in dates if x >= maintenant - dt.timedelta(days=PERIODE_JOURS)),
            "derniere": max(dates).isoformat() if dates else None}


def construire_parc():
    maintenant = dt.datetime.now(UTC)
    with ThreadPoolExecutor(max_workers=8) as ex:
        sites = list(ex.map(lire_site, noms_sites()))
    lignes, demandes = [], []
    for s in sites:
        ld = stats_demandes(s["demandes"], maintenant)
        g = s["gsc"]
        conv = round(100 * ld["periode"] / g["clics"], 1) if ld and g and g["clics"] else None
        lignes.append({"nom": s["nom"], "domaine": s["domaine"], "wp": s["wp"], "gsc": g, "demandes": ld,
                       "conversion": conv, "alertes": s["alertes"]})
        demandes += s["demandes"] or []
    demandes.sort(key=lambda d: d["date"], reverse=True)

    def somme(cle, sous):
        vals = [l[cle][sous] for l in lignes if l[cle] and l[cle].get(sous) is not None]
        return sum(vals) if vals else None
    total = {"sites": len(lignes),
             "wp": {k: somme("wp", k) for k in ("en_ligne", "programmes", "file")},
             "gsc": {k: somme("gsc", k) for k in ("clics", "impressions", "rankent", "renforcer", "clics_avant")},
             "demandes": {k: somme("demandes", k) for k in ("total", "periode")},
             "alertes": sum(len(l["alertes"]) for l in lignes)}
    if any(l["gsc"] and l["gsc"]["clics_avant"] is None for l in lignes):
        total["gsc"]["clics_avant"] = None     # évolution du parc : seulement si chaque site relevé a un relevé précédent
    clics, dem = total["gsc"]["clics"], total["demandes"]["periode"]
    total["conversion"] = round(100 * dem / clics, 1) if clics and dem is not None else None
    par_mois = {}
    for d in demandes:
        par_mois[d["date"][:7]] = par_mois.get(d["date"][:7], 0) + 1
    return {"genere_le": maintenant.isoformat(timespec="seconds"), "periode_jours": PERIODE_JOURS, "sites": lignes,
            "total": total, "demandes": demandes, "par_mois": dict(sorted(par_mois.items(), reverse=True))}


_cache = {"parc": None}
_verrou = threading.Lock()


def parc(rafraichir=False):
    with _verrou:
        if rafraichir or _cache["parc"] is None:
            _cache["parc"] = construire_parc()
        return _cache["parc"]


def csv_demandes(demandes):
    sortie = io.StringIO()
    w = csv.writer(sortie, delimiter=";")
    w.writerow(["date", "site", "page", "besoins", "code postal", "délai"])
    for d in demandes:
        w.writerow([d["date"][:16].replace("T", " "), d["site"], "/" if d["page"] == "/" else f"/{d['page']}/",
                    " + ".join(d["besoins"]), d["cp"], d["delai"]])
    return "﻿" + sortie.getvalue()     # BOM : Excel lit les accents


# ---------------------------------------------------------------- serveur
class Panel(BaseHTTPRequestHandler):
    def envoyer(self, code, corps, type_contenu, extra=None):
        data = corps.encode() if isinstance(corps, str) else corps
        self.send_response(code)
        self.send_header("Content-Type", type_contenu)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(u.query)
        if u.path in ("/", "/index.html"):
            with open(os.path.join(ICI, "index.html"), encoding="utf-8") as f:
                return self.envoyer(200, f.read(), "text/html; charset=utf-8")
        if u.path == "/api/parc":
            return self.envoyer(200, json.dumps(parc("rafraichir" in q), ensure_ascii=False), "application/json; charset=utf-8")
        if u.path == "/api/demandes.csv":
            demandes = parc()["demandes"]
            if q.get("site"):
                demandes = [d for d in demandes if d["site"] == q["site"][0]]
            if q.get("depuis"):
                demandes = [d for d in demandes if d["date"][:10] >= q["depuis"][0]]
            nom = f"demandes-{dt.date.today().isoformat()}.csv"
            return self.envoyer(200, csv_demandes(demandes), "text/csv; charset=utf-8",
                                {"Content-Disposition": f'attachment; filename="{nom}"'})
        self.envoyer(404, "introuvable", "text/plain; charset=utf-8")

    def log_message(self, *args):
        pass


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    try:
        serveur = ThreadingHTTPServer(("127.0.0.1", port), Panel)
    except OSError:
        sys.exit(f"Le port {port} est déjà pris : le panel tourne sans doute déjà, ouvrir http://127.0.0.1:{port}\n"
                 f"(ou le lancer sur un autre port : python3 panel/panel.py {port + 1})")
    print(f"Panel du parc : http://127.0.0.1:{port}  (Ctrl+C pour arrêter)")
    try:
        serveur.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
