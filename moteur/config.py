"""Réglages du site en cours.

Le moteur est commun à tous les sites ; ce qui change d'un site à l'autre vit dans
<dossier du site>/site.json. Le dossier du site est donné par la variable SITE_DIR
(posée par les lanceurs tools/*.py de chaque site), sinon cherché en remontant
depuis le dossier courant.
"""
import os, json


def _racine():
    d = os.environ.get("SITE_DIR")
    if d:
        return os.path.abspath(d)
    d = os.getcwd()
    while True:
        if os.path.exists(os.path.join(d, "site.json")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            raise SystemExit("site.json introuvable : lancez la commande depuis le dossier d'un site")
        d = parent


ROOT = _racine()
with open(os.path.join(ROOT, "site.json"), encoding="utf-8") as _f:
    SITE = json.load(_f)

# Verticales de contenu : une catégorie WordPress, une page mère, un besoin coché dans le formulaire.
VERTICALES = SITE["verticales"]
LOCAL = SITE.get("categorie_locale") or {}


def est_locale(fm):
    """Page de ville : repérée par son `cluster` (categorie_locale.cluster) ou, à défaut, par sa `categorie`."""
    if LOCAL.get("cluster"):
        return fm.get("cluster") == LOCAL["cluster"]
    return bool(LOCAL.get("categorie")) and fm.get("categorie") == LOCAL["categorie"]


FORM = SITE["formulaire"]
COULEURS = SITE["couleurs"]
# Rythme propre au site : `par_jour` articles chaque jour de sortie, un jour de sortie tous les `tous_les` jours
# (défaut : un article par jour). Le rythme se règle dans site.json, jamais dans le moteur.
PUBLICATION = {"delai_min_heures": 2, "heure_debut": 7, "heure_fin": 22, "par_jour": 1, "tous_les": 1,
               **SITE.get("publication", {})}
# ecart_min_heures et fenetre_heures, encore présents dans certains site.json, ne servent plus.
FUSEAU = SITE.get("fuseau", "Europe/Brussels")

# Tables dérivées, dans la forme où le moteur les utilise.
CATEGORIE_BESOIN = {v["categorie"]: v["besoin"] for v in VERTICALES}          # "Pellets" → "pellets"
MERE_BESOIN = {v["mere"]: v["besoin"] for v in VERTICALES}                    # "pellets" → "pellets"
CATEGORIE_SITEMAP = {v["categorie"]: v["sitemap"] for v in VERTICALES}        # "Pellets" → "Pellets"
MERE_SITEMAP = {v["mere"]: v["sitemap"] for v in VERTICALES}                  # "bois-de-chauffage" → "Bois"
CATEGORIE_MERE = {v["categorie"]: f"/{v['mere']}/" for v in VERTICALES}       # "Pellets" → "/pellets/"

# Affiliation (site.json → "affiliation": {"fichier": "affiliation.json", "mention": "…"}) : outils cités par
# [texte](@cle) dans les articles. Chaque outil : {"nom", "url" (lien affilié, facultatif), "site" (site officiel)}.
# Absent : aucun lien @ n'est rendu (les sites de leads n'en ont pas).
AFFILIATION = SITE.get("affiliation") or {}
OUTILS = {}
if AFFILIATION.get("fichier"):
    try:
        with open(os.path.join(ROOT, AFFILIATION["fichier"]), encoding="utf-8") as _f:
            OUTILS = json.load(_f)
    except (OSError, ValueError):
        OUTILS = {}

# En-tête User-Agent des appels à l'API WordPress (site.json → "user_agent"). Par défaut celui d'un navigateur ;
# certains hébergeurs (gruptis.es) renvoient en boucle (307) les écritures qui se présentent comme un navigateur.
USER_AGENT = SITE.get("user_agent", "Mozilla/5.0")
