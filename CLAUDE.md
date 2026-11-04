# SEO LOCAL — moteur et sites de génération de leads locaux

Sites WordPress de **génération de leads locaux** (demandes de devis transmises à des professionnels), pilotés par un moteur commun. Le moteur est à la racine, chaque site a son dossier dans `sites/`. Détail de l'organisation : `README.md`.

Les sites d'affiliation et de médias (gruptis, tobines, jm-date-replay, youre-precious) ont été séparés le 31/10/2026, à la demande du propriétaire : ils vivent dans `../SEO AFFILIATION/`, avec leur propre moteur. Rien n'est partagé entre les deux dossiers.

## Les sites
| Dossier | Domaine | Tâche planifiée (machine) | Design |
|---|---|---|---|
| `sites/bois-chauffage/` | bois-de-chauffage-et-pellets.be | `pilote-bois-chauffage` (propriétaire) | direction C (`designs/c-melange.html`) |
| `sites/elagage/` | elagage-luxembourg.com | `pilote-elagage-luxembourg` (propriétaire) | direction A (`designs/a-editorial.html`) |

Ces deux sites, les premiers, servent d'**exemples** pour les nouveaux : article modèle, modèles de pages locales (`articles/_modeles/`), procédure du pilote, thème. Leurs pilotes tournent chaque jour sur la machine du propriétaire et ne commitent pas leur production : le propriétaire la commite et la pousse en session ; l'associé ne lance jamais ces pilotes.

Un associé peut aussi garder des sites **hors du dépôt**, sur sa machine : ils sont décrits dans son `CLAUDE.local.md` (à lire s'il existe), exclus par `.git/info/exclude`, jamais cités dans un fichier ou un message de commit du dépôt partagé.

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
- **Rythme et priorités.** Au rythme du site (un article par jour par défaut), dans l'ordre d'une sitemap définie au lancement. La sitemap se repriorise en cours de route selon la Search Console (données saisies à la main pour l'instant). **Un article demandé par le propriétaire passe avant tout le reste** : en tête de `autopilote/file-attente.txt` s'il n'est pas encore écrit, `publier <slug> --urgent` une fois prêt.
- **Production par lots** (nouveaux sites, depuis le 01/11/2026). Pas de pilote quotidien : une session rédige un lot de pages et les programme d'avance, au rythme du site (2 à 4 semaines d'avance), puis on réadapte à chaque intervention humaine avec `publier --urgent` et `replanifier` (détail dans `guides/production-par-lots.md`). La recherche locale reste faite juste avant la rédaction de chaque page.

## Doctrine du propriétaire (apprise sur les premiers sites, vaut pour tous)
La rédaction d'un article suit la charte (`charte-base.md`, copiée dans chaque site en `articles/00-charte-redactionnelle.md`) : réponse d'abord, H2 sur les recherches, voix d'un professionnel qui parle à un acheteur en « vous », liens internes dans les phrases, aucun lien sortant, faits sourcés ou retirés, photos. Le reste :
- **Le lead d'abord.** Avant de créer ou d'écarter une page : quel professionnel paierait ce lead ? La page peut-elle porter un contenu propre ? Les volumes Semrush ne servent qu'à ordonner la production : sur du local, un « 0 » veut dire « sous le seuil », pas « aucune demande ».
- **Des catégories par produit ou service recherché, jamais par métier** (pas de page « Poêlier » ou « Élagueur » sans contenu). Une page par produit et par ville, au titre qui porte l'intention d'achat : « Bois de chauffage à Arlon », « Élagage à Mamer ». Ce qui est un besoin (entretien, dépannage) devient un cluster dans sa catégorie et un champ du formulaire, pas une catégorie.
- **Le local d'abord : 4 pages locales pour 1 guide** dans la file, formulaire de devis sur chaque page locale.
- **Pages locales : jamais interchangeables.** Chacune repose sur des données publiques de sa commune, cherchées et sourcées juste avant sa rédaction, sinon tout le domaine risque d'être vu comme des pages satellites. Une offre locale maigre devient l'argument du formulaire (« on vous trouve un professionnel ») ; on ne bloque une ville que si rien de propre ne peut s'écrire.
- **Page mère** : ce que c'est · ce que ça coûte (chiffre daté et sourcé) · qui l'utilise · les différences · comment choisir · où le trouver près de chez vous (liens vers les pages locales) · les guides. Aucune section qui ne soit qu'un sommaire de liens.
- **Laisser tranquilles les pages qui rankent.** Mettre à jour leurs données (prix, dates, liens vers les nouvelles pages, photos) oui ; réécrire leur texte ou leurs titres, non, sauf raison venue de la Search Console et accord du propriétaire. Pas de réécriture dans les 90 jours qui suivent une publication.
- **Rien à faire valider par le partenaire qui achète les leads.** Choix par défaut assumés : toute l'offre de la niche est couverte, prix et délais du marché sourcés et datés. Jamais de « à confirmer avec le partenaire » dans une sitemap, une stratégie ou un message. L'honnêteté reste entière : jamais un usage, un avis ou une photo prétendus.
- **Faire soi-même.** En session, ce qui se fait par l'API WordPress (réglages, pages, médias, extensions sur demande) se fait directement, sans écrire de procédure au propriétaire ; ne lui renvoyer que ce que lui seul peut fournir (domaine, hébergement, mots de passe, décisions business). Toute suppression est confirmée avant. Les pilotes, eux, gardent leurs interdits.
- **Une limite n'est pas un blocage.** Une source illisible, un site qui refuse la lecture, une API en panne : passer à la méthode suivante (autre page, autre source, autre moteur de recherche). Le résultat de recherche de référence est celui de Google dans le pays du site (google.be pour la Belgique), lu dans le navigateur, cookies refusés.
- **Tester avant de réécrire.** Une nouvelle règle de rédaction ou du moteur s'essaie d'abord sur des essais (`articles/_essais/`, ignorés par le maillage) avant de toucher aux pages en ligne.
- **Design** : pas de constructeur de pages (Elementor). Thème officiel Twenty Twenty-Five habillé par l'API (`moteur/theme.py`), une direction de `designs/` par site, maquettes HTML autonomes avant tout thème. Les composants des articles (En bref, chiffres, cartes de choix, avantages et inconvénients, checklist, FAQ) sont des syntaxes Markdown rendues par `moteur/design.py`.

## Règles communes
- **Le moteur (`moteur/`) sert tous les sites locaux.** Une modification se teste sur chaque site avant d'être gardée (procédure dans `README.md`). Les tâches planifiées ne le modifient jamais. Ce qui ne concerne que l'affiliation (relecteur, note sur 10, pages marque…) va dans le moteur de `../SEO AFFILIATION/`, jamais ici.
- Les identifiants WordPress sont dans `sites/<site>/setup/.env` : **ne jamais les afficher ni les copier**.
- Un nouveau site se crée avec `python3 nouveau_site.py <nom> <domaine>`, jamais à la main.
- Les directions de design réutilisables sont dans `designs/` : un nouveau site prend une direction pas encore utilisée.
- **Le rythme de publication se règle par site**, dans `site.json` → `publication` (`par_jour`, `tous_les`), jamais en modifiant le moteur : le défaut du moteur (un article par jour) ne change pas.
- Les options propres à un site passent par son `site.json` (libellés `textes`, `brief` par pays, `user_agent`…) : les valeurs par défaut du moteur restent celles des sites belges, dont le rendu ne doit pas changer.

## Dépôt Git partagé (GitHub privé, depuis le 31/10/2026)
- Le propriétaire y travaille avec un associé. Le dépôt contient le moteur, `designs/`, `modele-site/`, la doc et les nouveaux sites. `archives/` et `brouillons/` restent hors du dépôt (`.gitignore`), comme les sites gardés en local.
- **Guides** : `guides/arrivee.md` (arriver sur le projet, lancer un site de A à Z) et `guides/production-par-lots.md` (une session de travail sur un site).
- **Le panel du parc** (`python3 panel/panel.py`, détail dans `README.md`) suit tous les sites : stats par site, demandes de devis. Lecture seule.
- **Avant de travailler : `git pull`. Après : commit puis `git push`.** Un travail qui dure plus d'une session passe par une branche.
- **Jamais d'identifiants dans Git** : les `setup/.env` sont exclus ; chacun garde les siens en local.
- **Un site, un seul pilote, sur une seule machine.** Le `CLAUDE.md` du site dit sur quelle machine tourne sa tâche planifiée : sur une deuxième machine, elle publierait une deuxième fois.
- Une modification du **moteur** passe par une branche et un test de rendu de tous les sites avant d'aller sur `main`, y compris les sites gardés hors du dépôt sur la machine où l'on travaille. Sur GitHub, elle passe par une pull request relue par l'autre associé.
