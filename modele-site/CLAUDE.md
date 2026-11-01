# Projet : {{DOMAINE}}

<!-- À COMPLÉTER au lancement : la niche, le modèle économique (leads, affiliation), la zone. -->
Site WordPress de génération de leads. Le propriétaire collecte des demandes de devis et les transmet à des partenaires.

## Silo local
Le site suit le principe d'un site local décrit dans `../../CLAUDE.md` (racine de SEO LOCAL).
<!-- À COMPLÉTER au lancement -->
- **Mot-clé principal** : …
- **Catégories** (une page mère chacune, déclinée par ville) : …, plus **Guides**
- **Zone** : … — villes de la plus grosse à la plus petite (population officielle), jusqu'aux villages
- **Data renouvelée** : la donnée de la niche qui bouge chaque jour ou chaque semaine (prix, saison…) et où la relever

## Où est quoi
| Chemin | Rôle |
|---|---|
| `site.json` | Réglages du site pour le moteur : verticales, formulaire, couleurs, publication |
| `strategie/sitemap-urls.csv` | Les URLs prévues et leur `statut` — tableau de bord |
| `articles/00-charte-redactionnelle.md` | **Charte de rédaction — fait foi** |
| `articles/*.md` | Sources des articles ; WordPress n'en reçoit que le rendu |
| `visuels/`, `photos/`, `media/` | Schémas SVG, photos du propriétaire, images prêtes à envoyer |
| `tools/` | Lanceurs du moteur commun (`../../moteur/`) — ne pas modifier |
| `autopilote/` | Procédure, file d'attente, journal et état du pilote |
| `setup/.env` | Identifiants WordPress — **ne jamais afficher ni copier** |

## Règles du site
- URLs de premier niveau ; le silo passe par les catégories WordPress (une par verticale de `site.json`) et les liens internes.
- Accès WordPress : utilisateur `claude`, rôle Éditeur. Ni plugins, ni réglages, ni menu.
- Une page peut exister sans volume de recherche, **jamais sans contenu propre**. Une page locale repose sur des données propres à sa commune, recherchées et sourcées juste avant sa rédaction.
- Ne jamais modifier un contenu WordPress qui n'est pas produit depuis `articles/`.

## Style attendu par le propriétaire
Phrases simples qui expliquent, sans formule d'élan. La réponse avant le premier scroll (encadré « En bref »). Une liste à puces par article, deux au maximum. Toujours un paragraphe entre un H2 et un H3. Détail dans la charte.

Article modèle : <!-- à désigner après le premier article validé par le propriétaire, ex. articles/<slug>.md -->

## Pilote automatique
Tâche planifiée `pilote-{{SLUG_SITE}}`, sur une seule machine : <!-- À COMPLÉTER : la machine (propriétaire ou associé) --> . Chaque jour un article est rédigé, vérifié puis programmé. Procédure : `autopilote/PROCEDURE.md`. Journal : `autopilote/journal.md`.

## En attente du propriétaire
Voir `setup/DEMARRAGE.md`.
