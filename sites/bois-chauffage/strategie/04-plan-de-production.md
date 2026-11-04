# Plan de production — révisé sur données réelles
> 5 sept. 2026. Remplace la version initiale.
>
> **Base des priorités** : le fichier de mots-clés 2024 (volumes + KD réels) pour tout ce qui touche au pellet. La Search Console sert uniquement à confirmer la thématique et la tendance du domaine — **pas à hiérarchiser** (voir le rappel de portée dans l'audit).
>
> ⚠️ **Angle mort assumé : aucune donnée de volume sur le bois de chauffage.** Le fichier 2024 ne couvrait que le pellet. Toute priorité côté bûches ci-dessous est une hypothèse de marché, à confirmer par une extraction de volumes avant production.

## Phase 0 — Déblocage (cette semaine, ~1 journée) ★ PRIORITÉ ABSOLUE

Rien ne sert de publier tant que ce n'est pas fait : **toute nouvelle page hériterait du sort de `/meilleur-pellet/`** — orpheline, donc jamais indexée.

| # | Action | Pourquoi |
|---|---|---|
| 1 | **Créer un menu de navigation** | La homepage a 1 seul lien interne (le logo). C'est la cause directe de la non-indexation de l'article |
| 2 | **Lier `/meilleur-pellet/` depuis la homepage** | Sort la page de son orphelinat |
| 3 | **Demander l'indexation dans GSC** (inspection d'URL) | Force le recrawl après correction |
| 4 | **robots.txt** : supprimer `Crawl-delay: 10`, ajouter `Sitemap: https://bois-de-chauffage-et-pellets.be/sitemap_index.xml` | Le crawl-delay freine Bing pour rien ; la directive sitemap accélère la découverte |
| 5 | **Installer un cache** (LiteSpeed Cache ou WP Rocket) | TTFB à 1,0-1,4 s, aucun cache détecté. Cible < 0,5 s |
| 6 | **Corriger le `<title>` de l'article** | Faute « caractéritiques » visible dans les résultats |
| 7 | **Supprimer la `<meta description>` en double** sur l'article | Deux balises concurrentes |
| 8 | **`og:locale` → `fr_BE`** | Correction gratuite, cohérence du ciblage |
| 9 | **Retirer « Le site numéro 1 en Belgique »** et « livraison gratuite » | Superlatif invérifiable + promesse au nom de tiers. Encadré par le livre VI du Code de droit économique |

## Phase 1 — Le tunnel (semaines 1-2) ★

**`/devis/` avant tout contenu.** Aujourd'hui il n'existe aucun formulaire : chaque visiteur gagné serait perdu. Pour un modèle de collecte de leads, le formulaire *est* le produit.

Champs qui conditionnent la valeur du lead pour le fournisseur :
- Type de produit (pellets sac / pellets vrac / bûches / allume-feu)
- Quantité estimée
- **Code postal** — la clé de routage, champ le plus important
- Délai souhaité
- Coordonnées

À prévoir dès la conception : mentions RGPD (finalité, base légale, durée de conservation, destinataires), et surtout **la transparence sur le modèle** — le visiteur doit comprendre que ses coordonnées seront transmises à des fournisseurs. C'est une obligation légale, et c'est aussi ce qui fait la différence entre un comparateur crédible et un aspirateur à données.

## Phase 2 — Le gisement à plus fort rendement (semaines 2-6)

Ordre établi par volume ÷ difficulté, avec la saison en tête.

| Ordre | Page | Volume/mois | KD | Pourquoi maintenant |
|---|---|---|---|---|
| 1 | `/pellets/prix/` | 1 300 | **13** | Difficulté la plus basse à volume élevé. Intention commerciale directe |
| 2 | `/pellets/prime/` | 2 400 | 19 | Pic saisonnier **en cours** — on achète son chauffage en automne |
| 3 | `/pellets/marques/piron/` | 2 400 | 17 | Plus gros volume marque. Ouvre le silo |
| 4 | `/pellets/` (hub) | 6 600 | 7 | KD 7 sur 6 600/mois. Consolide le silo une fois les filles en place |
| 5 | `/pellets/marques/` (hub) | — | — | Structure le cluster |

## Phase 3 — Compléter le cluster + amorcer le local (oct.-nov.)

| Page | Volume | KD |
|---|---|---|
| `/pellets/marques/gamma/` | 1 300 | 21 |
| `/pellets/marques/hubo/` | 1 000 | 24 |
| `/pellets/marques/trafic/` | 1 000 | 17 |
| `/pellets/marques/descamps/` | 880 | 10 |
| `/pellets/marques/badger/` | 880 | 11 |
| `/pellets/marques/aveve/` | 880 | 11 |
| `/pellets/marques/brico/` | 880 | 33 |
| `/bois-de-chauffage/stere/` | 1 300 | 20 |
| `/bois-de-chauffage/` (hub) | — | — |
| `/fournisseurs/liege/` · `/namur/` · `/brabant-wallon/` | — | faible |

Les trois premières zones locales sont choisies sur les requêtes **déjà en impression** : `bois de chauffage liège`, `chauffagiste pellet brabant wallon`, `bois de chauffage province luxembourg`.

## Phase 4 — Décembre à février
- Les deux calculateurs (`/outils/`)
- `/bois-de-chauffage/essences/` — chêne, hêtre, frêne, bouleau regroupés (20/mois chacun : une seule page, pas quatre)
- `/partenaires/` — recrutement côté offre
- Extension locale : Charleroi, Mons, Namur, province de Luxembourg

## Phase 5 — Mars à août : la saison décisive
C'est là que le rapport effort/résultat est le meilleur, parce que la concurrence cesse de publier.
- Netlinking : annuaires belges, presse locale, partenariats métiers
- Mise à jour de toutes les pages « prix » **avant août**
- Consolidation : fusionner ou supprimer ce qui n'a rien produit

---

## Le point aveugle du modèle : le côté offre

Un intermédiaire a besoin de **fournisseurs partenaires prêts à recevoir les leads**. Sans eux, le trafic ne se monétise pas et les demandes collectées se périment — en pleine saison, un lead a une durée de vie de quelques jours.

À cadrer en parallèle du SEO, pas après : combien de partenaires, sur quelles zones, à quel tarif par lead ou quelle commission, et avec quel engagement de réactivité. C'est hors périmètre SEO mais **c'est le facteur limitant du chiffre d'affaires**, pas le trafic.

---

## Ordre de grandeur (illustratif, pas une prévision)

Les clusters identifiés totalisent **≈ 20 800 recherches/mois** (volumes 2024 à recontrôler).

En prenant des hypothèses délibérément prudentes — positionnement en page 1 sur *un tiers* du gisement d'ici 12 mois, CTR moyen de 4 %, conversion du trafic en demande de devis de 3 % :

> ≈ 7 000 recherches captées → ≈ 280 visites/mois → **≈ 8 à 10 demandes de devis par mois**

Chiffres à manier avec précaution : ce sont des hypothèses de calcul, pas une projection. Ils servent à donner l'échelle et à décider si le côté offre vaut d'être structuré — pas à fixer un objectif. La variable qui les fera bouger le plus n'est pas le trafic, c'est le taux de conversion du formulaire.
