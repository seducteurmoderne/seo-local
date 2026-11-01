# SEO LOCAL — moteur et sites de génération de leads locaux

Sites WordPress de **génération de leads locaux** (demandes de devis transmises à des professionnels), pilotés par un moteur commun. Le moteur est à la racine, chaque site a son dossier dans `sites/`. Détail de l'organisation : `README.md`.

Les sites d'affiliation et de médias (gruptis, tobines, jm-date-replay, youre-precious) ont été séparés le 31/10/2026, à la demande du propriétaire : ils vivent dans `../SEO AFFILIATION/`, avec leur propre moteur. Rien n'est partagé entre les deux dossiers.

## Les sites
Les sites du dépôt partagé sont dans `sites/`. Un associé peut aussi garder des sites **hors du dépôt**, sur sa machine : ils sont décrits dans son `CLAUDE.local.md` (à lire s'il existe), exclus par `.git/info/exclude`, jamais cités dans un fichier ou un message de commit du dépôt partagé.

Chaque site a son propre `CLAUDE.md` : il fait foi pour ce site (règles, charte, accès). Le lire avant de travailler sur un site.

## Principe d'un site local (propriétaire, 31/10/2026)
Tout site et toute évolution du moteur servent ces principes.
- **Silo local par catégorie.** Les catégories sont tirées du mot-clé principal du site. Chaque catégorie a sa page mère, déclinée en pages locales dans un maximum de villes et de villages.
- **Zone et ordre.** Chaque site a sa zone, fixée par le propriétaire. On part toujours des villes les plus grosses vers les plus petites.
- **Une catégorie Guides** dans chaque site : articles généraux et informatifs sur la niche, pour asseoir l'autorité du site et nourrir les liens internes.
- **Maillage.** Les pages locales se lient entre elles ; la page mère lie ses pages locales, et chaque page locale lie sa mère.
- **Multiplier les villes et renouveler la data.** C'est ce qui fait marcher un site local. Selon la thématique, des titles ou des infos qui se mettent à jour chaque jour.
- **Recherche locale juste avant chaque rédaction**, propre à la page et à sa niche. Jamais de base de données commune aux sites : la machine va couvrir des zones et des niches très larges.
- **Accueil.** Assez de texte thématique pour que Google comprenne la cible du site, plus le listing des villes.
- **Rythme et priorités.** Un article par jour, dans l'ordre d'une sitemap définie au lancement. La sitemap se repriorise en cours de route selon la Search Console (données saisies à la main pour l'instant). **Un article demandé par le propriétaire passe avant tout le reste** : en tête de `autopilote/file-attente.txt` s'il n'est pas encore écrit, `publier <slug> --urgent` une fois prêt.
- **Production par lots** (nouveaux sites, depuis le 01/11/2026). Pas de pilote quotidien : une session rédige un lot de pages et les programme d'avance (un article par jour, 2 à 4 semaines d'avance), puis on réadapte à chaque intervention humaine avec `publier --urgent` et `replanifier` (détail dans `README.md`). La recherche locale reste faite juste avant la rédaction de chaque page.

## Règles communes
- **Le moteur (`moteur/`) sert tous les sites locaux.** Une modification se teste sur chaque site avant d'être gardée (procédure dans `README.md`). Les tâches planifiées ne le modifient jamais. Ce qui ne concerne que l'affiliation (relecteur, note sur 10, pages marque…) va dans le moteur de `../SEO AFFILIATION/`, jamais ici.
- Les identifiants WordPress sont dans `sites/<site>/setup/.env` : **ne jamais les afficher ni les copier**.
- Un nouveau site se crée avec `python3 nouveau_site.py <nom> <domaine>`, jamais à la main.
- Les directions de design réutilisables sont dans `designs/` : un nouveau site prend une direction pas encore utilisée.
- Les options propres à un site passent par son `site.json` (libellés `textes`, `brief` par pays, `user_agent`…) : les valeurs par défaut du moteur restent celles des sites belges, dont le rendu ne doit pas changer.

## Dépôt Git partagé (GitHub privé, depuis le 31/10/2026)
- Le propriétaire y travaille avec un associé. Le dépôt contient le moteur, `designs/`, `modele-site/`, la doc et les nouveaux sites. `archives/` et `brouillons/` restent hors du dépôt (`.gitignore`), comme les sites gardés en local.
- **Avant de travailler : `git pull`. Après : commit puis `git push`.** Un travail qui dure plus d'une session passe par une branche.
- **Jamais d'identifiants dans Git** : les `setup/.env` sont exclus ; chacun garde les siens en local.
- **Un site, un seul pilote, sur une seule machine.** Le `CLAUDE.md` du site dit sur quelle machine tourne sa tâche planifiée : sur une deuxième machine, elle publierait une deuxième fois.
- Une modification du **moteur** passe par une branche et un test de rendu de tous les sites avant d'aller sur `main`, y compris les sites gardés hors du dépôt sur la machine où l'on travaille. Sur GitHub, elle passe par une pull request relue par l'autre associé.
