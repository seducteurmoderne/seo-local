# Lancer elagage-luxembourg.com

Cochez dans l'ordre. Le pilote n'est activé qu'à la dernière étape.

## Côté propriétaire (WordPress, 30 minutes)
- [ ] Créer l'utilisateur `claude`, rôle **Éditeur** (jamais Administrateur)
- [ ] Sur son profil, créer un **mot de passe d'application** nommé `Claude Code`
- [ ] Le coller dans `setup/.env` (modèle : `setup/.env.exemple`) — jamais dans le chat
- [ ] Déposer `setup/mu-plugins/expose-yoast-rest.php` dans `wp-content/mu-plugins/` (Yoast requis)
- [ ] Créer les catégories WordPress : une par verticale de `site.json`, plus la catégorie locale si le site a des pages de ville
- [ ] Menu de navigation vers les pages mères (sans lui, les articles publiés sont peu découvrables)

## Côté stratégie (avec Claude, dans ce dossier)
- [ ] Niche, zone, partenaires : compléter l'en-tête de `CLAUDE.md`
- [ ] `site.json` : verticales, besoins et champs du formulaire, couleurs, code postal du pays
- [ ] `strategie/sitemap-urls.csv` : les URLs prévues (colonnes `verticale`, `role` = `mère` pour les pages mères, `cluster`)
- [ ] `autopilote/file-attente.txt` : l'ordre de production
- [ ] Charte : adapter les exemples de `articles/00-charte-redactionnelle.md` à la niche
- [ ] Premier article rédigé ensemble, validé par le propriétaire, désigné comme **article modèle** dans `CLAUDE.md`
- [ ] Données terrain (`setup/donnees-locales.csv`) avant toute page locale

## Formulaires de devis
- [ ] `python3 tools/autopilote.py plugin` génère `setup/mu-plugins/leads.php` depuis `site.json`
- [ ] Le propriétaire le dépose dans `wp-content/mu-plugins/` et ajoute `define('BCP_LEADS_EMAIL', 'adresse@domaine');` dans `wp-config.php`
- [ ] Page `/politique-de-confidentialite/` publiée
- Tant que ces deux éléments manquent, les formulaires restent masqués automatiquement.

## Activer le pilote
- [ ] `python3 tools/autopilote.py etat` répond « Connexion WordPress OK »
- [ ] Créer la tâche planifiée à partir de `../../tache-planifiee.md` (racine de SITES/), à une heure différente des autres sites (30 minutes d'écart au moins)
