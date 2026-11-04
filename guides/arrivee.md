# Arriver sur SEO LOCAL

Bienvenue. Ce dépôt sert à lancer et faire tourner des **sites WordPress de génération de leads locaux** : chaque site attire des personnes qui cherchent un service près de chez elles, et transmet leurs demandes de devis à des professionnels partenaires. Un moteur commun écrit, contrôle et publie les pages ; chaque site a son dossier dans `sites/`.

## À lire, dans cet ordre
1. `CLAUDE.md` : le principe d'un site local, la doctrine du propriétaire, les règles communes et le travail à deux. Claude le lit à chaque session.
2. `README.md` : l'organisation du dépôt, les réglages de `site.json`, les commandes.
3. `charte-base.md` : comment s'écrit une page (copiée dans chaque site).
4. `guides/production-par-lots.md` : une session de travail sur un site.
5. Un site d'exemple : `sites/elagage/` (le plus récent) ou `sites/bois-chauffage/` (le plus fourni). Leur `CLAUDE.md`, leur article modèle, leurs modèles de pages de ville (`articles/_modeles/`).

## Installer
```bash
git clone git@github.com:seducteurmoderne/seo-local.git "SEO LOCAL"
```
Il faut Python 3 et `openssl` (présents sur macOS) et Claude Code, ouvert sur le dossier `SEO LOCAL`. Le moteur n'a pas d'autre dépendance.

## Les accès : chacun les siens, jamais dans Git
- **WordPress** : pour chaque site où tu travailles, un utilisateur et un mot de passe d'application à toi, dans `sites/<site>/setup/.env` (modèle : `setup/.env.exemple`). Le fichier est ignoré par Git ; il ne se colle jamais dans une conversation.
- **Search Console** (à venir : la connexion est écrite, elle sera fusionnée quand la clé Google existera) : une clé de compte de service dans `~/.config/seo-local/search-console.json`, transmise par un gestionnaire de mots de passe, jamais par e-mail ni dans le dépôt.

## Travailler à deux
- **`git pull` avant de travailler, commit puis `git push` après.** Un travail de plusieurs sessions passe par une branche.
- **Le moteur (`moteur/`) sert tous les sites** : une modification passe par une branche, un rendu de tous les articles de tous les sites avant et après (identique pour un article inchangé), `verifier` sur un article de chaque site, puis une pull request relue par l'autre associé.
- **Un site, un seul responsable de la publication.** Les nouveaux sites fonctionnent par lots, sans tâche planifiée. Les deux sites d'exemple ont un pilote quotidien sur la machine du propriétaire : on ne le lance jamais ailleurs, il publierait une deuxième fois.
- **Ce qui est décidé s'écrit.** Une décision prise en session (zone, catégories, règle de rédaction, exception) va dans le `CLAUDE.md` du site ou dans la doc commune. Claude ne se souvient pas d'une machine à l'autre : seul le dépôt est partagé.

## Lancer un site, de A à Z
| Étape | Qui |
|---|---|
| 1. Niche, zone, mot-clé principal, partenaire qui achète les leads | les associés |
| 2. Domaine, hébergement, WordPress installé, utilisateur `claude` avec mot de passe d'application, vrai cron | les associés |
| 3. `python3 nouveau_site.py <nom> <domaine>` à la racine | Claude |
| 4. `sites/<nom>/setup/DEMARRAGE.md` : catégories, villes triées par population, sitemap, `site.json`, design, formulaires, Search Console | Claude, avec les associés pour les choix |
| 5. Premier article rédigé ensemble et validé : l'article modèle | ensemble |
| 6. Premier lot programmé (`guides/production-par-lots.md`) | Claude |
| 7. Le site apparaît dans le panel, sans alerte | vérification |

## Au quotidien
- **Le panel du parc** : `python3 panel/panel.py`, puis http://127.0.0.1:8765. Une ligne par site (pages, Search Console, demandes, alertes) et la liste des demandes de tout le parc.
- **Les commandes d'un site** (depuis `sites/<site>/`) : `etat`, `suivant`, `modele`, `brief`, `verifier`, `publier [--urgent]`, `replanifier`, `maillage`, `photos commune|chercher|prendre|manquantes`, `audit` — toutes sous `python3 tools/autopilote.py`. Sans argument, la commande affiche son aide.
