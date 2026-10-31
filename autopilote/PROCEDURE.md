# Une exécution du pilote automatique

Objectif : **environ un article par jour, à une heure qui varie**, sans jamais publier un fait non vérifié, un lien cassé ni une note interne.

Toutes les commandes se lancent depuis le dossier du projet :
`/Users/thomasdufour/Documents/CLAUDE.nosync/SEO LOCAL/sites/bois-chauffage`

## 1. État du site
`python3 tools/autopilote.py etat`

- La commande publie d'abord les articles programmés restés en retard (le cron WordPress ne tourne qu'avec des visites).
- Si elle échoue sur une erreur de connexion (HTTP 401/403, site injoignable) : envoie la notification « Pilote bois : WordPress refuse la connexion, mot de passe d'application à vérifier » et arrête-toi.
- Si **2 articles ou plus sont déjà programmés**, ne rédige rien aujourd'hui : passe à l'étape 6.

## 2. Maillage
`python3 tools/autopilote.py maillage`
Réactive dans les articles en ligne les liens vers les pages publiées depuis, et installe les formulaires de devis dès que le plugin de réception est actif.

## 3. Choisir l'article
`python3 tools/autopilote.py suivant` donne le prochain slug. Lis sa ligne dans `strategie/sitemap-urls.csv` : titre, verticale, cluster, rôle, CTA.

**Rythme voulu par le propriétaire (20/09/2026) : une majorité de pages locales, 4 pour 1 guide.** Le local se référence vite et convertit : chaque page locale porte un formulaire de devis. La file `autopilote/file-attente.txt` applique ce rythme, ne le réordonne pas.

**Page locale** (`/bois-de-chauffage-<ville>/`, `/pellets-<ville>/`) : `categorie: Bois de chauffage` ou `Pellets` (la verticale : c'est elle que montre le fil d'Ariane), `besoin: bois` ou `pellets`, `cluster: Ville` (c'est ce champ qui fait d'elle une page locale). **Une page locale se fait toujours, elle ne se bloque pas faute de fournisseurs** (décision du propriétaire, 29/09/2026). Les données viennent de trois sources, dans cet ordre :
1. **La ligne de la ville** dans `setup/03-donnees-locales-a-collecter.csv` : fournisseurs, communes desservies, délais, contraintes d'accès, prix. Un fournisseur marqué « à confirmer » ou « À VÉRIFIER » est écarté, sauf si son propre site confirme pendant l'exécution ce qu'il vend et où.
2. **Les magasins de la ville et des environs, recherchés pendant l'exécution.** Les magasins de bricolage, de jardin et de bazar (Trafic, Brico, Hubo, Gamma, Mr.Bricolage, Aveve, jardineries) vendent presque toujours des pellets en sac, et souvent des bûches en sac, des briquettes ou du bois d'allumage. Cherche ceux de la commune et des communes voisines sur le site de chaque enseigne (localisateur de magasins, fiche produit) : adresse, produit et format, prix affiché avec la date du relevé, retrait ou livraison. Une enseigne dont le site ne montre pas le produit ou le magasin n'est pas citée. Trafic : localisateur trafic.com/fr_BE/magasins (recherche par ville), puis « Consulter le stock du magasin » sur la fiche pellet ; ses prix ne sont pas lisibles par `prix.py`, suivez la fiche avec `attendu` (exemple : `trafic_green_statut`) et ne les écrivez pas en dur (demande du propriétaire, 10/10/2026). Sans magasin dans la commune, citez ceux à une quinzaine de kilomètres, puis renvoyez au formulaire.
3. **Les fournisseurs qui nomment la ville sur leur propre site** (zone de livraison, page « livraison à <ville> »), trouvés par recherche web. Chacun est vérifié sur son site, jamais repris d'un annuaire seul.

Chaque fait est sourcé ; une colonne vide du CSV n'est pas inventée. **Une page locale part toujours du modèle** : `python3 tools/autopilote.py modele <slug>` crée le fichier avec la structure, les titres au nom de la ville et les données de la ville en notes. Le modèle donne la structure ; le texte de chaque section repose sur les données de *cette* ville (le contrôle refuse une page dont plus de la moitié du texte se retrouve dans une autre page locale). Les fournisseurs tiennent dans le tableau : pas de paragraphe par fournisseur. **Ce qui la rend propre** : les magasins et fournisseurs réellement proches de *cette* ville, leurs distances, leurs prix relevés, et le constat honnête de l'offre sur place. Si deux villes voisines partagent les mêmes fournisseurs (Libramont et Neufchâteau), la page part de ce que la seconde a en propre (magasins de la commune, distance aux dépôts, communes rurales autour), cite les fournisseurs communs sans recopier les paragraphes de l'autre page et renvoie vers elle par un lien.

**Une offre locale maigre est un argument, pas un motif de blocage.** Quand la ville compte peu de fournisseurs qui livrent, dites-le clairement (« à Neufchâteau, un seul fournisseur livre les pellets à domicile ; les magasins vendent au sac, à emporter ») et présentez le formulaire comme la solution : nous trouvons pour le visiteur un fournisseur qui livre chez lui. Le texte des formulaires est fixe sur toutes les pages locales (demande du propriétaire, 10/10/2026) : `::cta-fort Gratuit. Réponse rapide. Trouvez les meilleurs fournisseurs près de <Ville>`, sans sous-texte ; l'argument de l'offre maigre se dit dans le texte, pas dans le formulaire. `bloquer` ne sert plus, sur une page locale, que si **aucun point de vente** (fournisseur ou magasin) n'est trouvable à moins de 30 km : c'est alors le signe que la ville n'a pas sa place dans la file. Deux formulaires par page : `::cta-doux` après l'intro (sur une page locale, le CTA précoce est fort : `::cta-fort` juste après l'intro, comme pour une page mère) et `::cta-fort` en fin de page. Liens dans les phrases : la mère de la verticale, la page sœur de la même ville (bois ↔ pellets), `ramonage-<ville>` si elle existe, et les villes voisines de la file quand elles sont en ligne.

**Page locale poêle** (`/poele-a-pellets-<ville>/`, `/poele-a-bois-<ville>/`, depuis le 24/10/2026) : `categorie: Poêle à pellets` ou `Poêle à bois`, `besoin: poelier`, `cluster: Ville`, créée avec `modele <slug>`. Le lead est une pose, un entretien ou un dépannage, pas un achat de combustible. Les données sont les **poêleries et installateurs** de la commune et des communes à moins de 20 km, chacun vérifié sur son propre site : adresse, marques exposées, pose, entretien, dépannage, prix publiés (en balise de prix suivi). Un annuaire (Pages d'Or, « Top 10 des installateurs ») sert à trouver des noms, jamais de source. Les magasins de bricolage qui vendent des poêles sans les poser se citent comme tels. Formulaires : `::cta-fort Gratuit. Réponse rapide. Trouvez les meilleurs installateurs près de <Ville>`. Liens : la mère de la verticale poêle, la page `pellets-<ville>` ou `bois-de-chauffage-<ville>` de la même ville, `ramonage-<ville>` si elle existe, les villes voisines en ligne. `bloquer` seulement si aucune poêlerie n'est trouvable à moins de 30 km.

**Fiche fournisseur** (`categorie: Fournisseurs`, URL de premier niveau au nom de la société) : modèle `articles/_modeles/fiche-fournisseur.md`, copié à la main. Tout vient du site de la société et des sources publiques, daté : coordonnées, produits, zone de livraison, prix publiés en balise. L'encadré « Page indépendante » reste ; ni logo, ni avis, ni jugement de qualité, ni formulation qui laisse croire à un partenariat (Code de droit économique, livre VI). Le `besoin` suit le métier principal de la société. Lien vers la page de ville qu'elle dessert et vers la mère de sa verticale ; la page de ville renvoie vers la fiche.

## 4. Rédiger ou terminer
Si `articles/<slug>.md` n'existe pas, écris-le (page locale : crée-le d'abord avec `modele <slug>`). S'il existe, termine-le.

**D'abord le brief, avec le moteur en cascade** (charte, « Le brief SEO, avant d'écrire une ligne ») : si le navigateur est disponible, relève les liens des 10 premiers résultats de google.be ; puis `python3 tools/autopilote.py brief <slug> [<liens google.be>…]`. S'il s'arrête sur « IA non joignable », lis le fichier `.prompt.md` indiqué, réponds-y toi-même en JSON dans le `.json` indiqué (sérieusement : c'est l'analyse qui fait l'article), et relance la même commande jusqu'au bout. Pour une page locale, crée d'abord le fichier avec `modele <slug>`. Rédige ensuite en suivant le plan de `briefs/<slug>/brief.md`.

Relis d'abord `articles/00-charte-redactionnelle.md` et l'article modèle `articles/entretien-poele-a-pellets.md`. Ils font foi pour la forme, le ton et la syntaxe.

**Front-matter** : les mêmes champs que l'article modèle. `categorie` vaut Bois de chauffage, Pellets, Ramonage, Poêle à pellets, Poêle à bois ou Fournisseurs (la verticale de la ligne de sitemap) — pas de catégorie par métier ni de catégorie Entretien : l'entretien d'un poêle est un guide de sa verticale poêle. Les pages mères (`bois-de-chauffage`, `pellets`, `ramonage`, `poele-a-pellets`, `poele-a-bois`, `fournisseurs`) prennent `type: page`, sans catégorie : ce sont des pages hub qui présentent la verticale, renvoient vers ses guides et portent un CTA fort.

**Page mère** (`bois-de-chauffage`, `pellets`, `ramonage`, `poele-a-pellets`, `poele-a-bois` ; `fournisseurs` est un simple annuaire des fiches, publié après les premières) : `type: page`, sans catégorie, et **le plan imposé par la charte** — ce que c'est · ce que ça coûte · qui l'utilise · les différences · comment choisir · où acheter près de chez vous · `::guides`. Chaque section porte un fait sourcé et daté ; une page mère sans chiffre est refusée par le propriétaire. La section locale nomme les villes de la file en cours avec leurs liens, même non publiées. CTA fort après l'intro, CTA doux après la section prix, CTA fort en fin de page.

**Champ `besoin`** : le formulaire de devis coche une case selon le besoin réel du visiteur (bois, pellets, ramonage, ou `poelier` — entretien/dépannage/installation d'un appareil), indépendamment de la `categorie` de la page. Un article sur l'entretien ou le prix d'un poêle (à bois ou à pellets) prend `besoin: poelier` même classé en Pellets ou Bois de chauffage : c'est ce besoin-là que le visiteur exprime, pas l'achat de combustible. Omets le champ quand `besoin` et `categorie` coïncident (un article sur le prix du bois de chauffage n'a pas besoin de `besoin: bois`, c'est déjà la valeur par défaut). Une page locale porte toujours un `besoin` explicite : `besoin: bois` pour `/bois-de-chauffage-<ville>/`, `besoin: pellets` pour `/pellets-<ville>/`.

**Avant d'écrire : les recherches réelles.** Lance une recherche web sur la requête cible et note les recherches associées (suggestions, « Autres questions posées », titres des trois premiers résultats) dans `mots_cles_secondaires:`. Les H2 en sont tirées : deux au moins reprennent la requête cible (contrôle bloquant). Pas de FAQ sauf si trois questions réelles restent sans réponse dans le corps (voir la charte, « La FAQ »).

**Ton.** Relis `setup/terrain-auteur.md` : ce qu'il contient sur le sujet (expérience, anecdote, constat) est repris, reformulé. Rien d'autre ne se raconte à la première personne. Dis ce que la rédaction a fait (relevés, calculs) et donne un avis argumenté (charte, « Une voix incarnée »). Au moins deux éléments de rythme (`::chiffres`, encadré, tableau) sur un article de plus de 800 mots.

**Les faits sont sourcés ou retirés.** Toute affirmation réglementaire, normative ou chiffrée (prix, fréquence légale, seuil de norme, montant de prime) doit reposer sur une source primaire trouvée pendant l'exécution :
- réglementation et primes : sites officiels (wallonie.be, energie.wallonie.be, wallex.wallonie.be, economie.fgov.be, ejustice.just.fgov.be) ;
- normes et certifications : l'organisme émetteur (enplus-pellets.eu, DINplus…) ;
- prix : source publique datée (sites des enseignes, SPF Économie), avec le mois du relevé.

Source trouvée : écris le fait et cite-la sur la ligne finale `*Sources : Nom · Nom — vérifié en <mois année>.*`. **Le nom seul, jamais de lien sortant** (contrôle bloquant) : les URL vont dans les notes de production, sous « URL DES SOURCES », que le rendu ne publie pas.
Pas de source primaire : reformule sans le fait. Pour un prix, explique ce qui le fait varier et renvoie vers le devis. **Il ne doit rester aucun marqueur `[À VÉRIFIER]`.**

**Prix dynamiques (depuis le 09/10/2026, demande du propriétaire).** Un prix relevé sur le site d'un fournisseur ne s'écrit plus en dur : il devient une balise, relue chaque jour par le maillage.
- Ajoutez chaque prix à `prix/releves.json` : `source`, `libelle`, `url`, `motif` (expression cherchée dans le texte de la page, balises retirées ; le groupe 1 est le prix), `valeur`, `verifie_le`, `echecs: 0`. Testez le motif : `python3 -c "import sys; sys.path.insert(0,'../../moteur'); import prix, serp; print(prix.actualiser(serp.lire))"` ne doit rien signaler.
- Dans l'article : `{{prix:id}}` (le nombre, l'unité s'écrit après), `{{calc:(id_a*5+id_b)/5}}` pour un prix ramené au stère ou livré, `{{releve}}` pour la date du plus ancien relevé de l'article, `{{releve:id}}` pour celle d'un prix. Un état (« rupture de stock », « plus disponible ») se suit avec `attendu` au lieu de `valeur`.
- Les comparaisons s'écrivent avec les deux chiffres (« 101 € livré, contre 126 € de moyenne wallonne »), jamais « sous la moyenne » ou « le moins cher » : la phrase doit rester vraie si un prix bouge.
- Une moyenne publiée en image (Valbiom) garde sa valeur saisie à la main : `attendu` suit le mois affiché et le journal signale le nouveau mois.
- La date n'avance que si le prix a été relu le jour même. Le journal signale un prix changé (« relire les phrases qui comparent ») ou illisible : traitez ces lignes à l'exécution suivante.
- `{{aujourdhui}}` écrit la date du jour : dans le texte, le navigateur du visiteur la met à son jour ; dans `title_seo`, `meta_description` ou `h1`, le maillage la renvoie chaque matin. Réservé aux pages prix (`/prix-pellets/`, `/prix-bois-de-chauffage/`, demande du propriétaire du 09/10/2026), dont tous les prix sont relus chaque jour.
- Pas de prix chiffré dans `title_seo` ni `meta_description`.
- **Conversion des anciens articles** : après avoir programmé l'article du jour, convertissez au plus un article listé dans `prix/a-convertir.txt` (le premier), puis retirez-le de la liste. Contrôle : `verifier` ne doit pas signaler de prix dynamique inconnu, et le texte rendu ne garde aucune balise `{{`.

Si le cœur de l'article repose sur des données introuvables (page prix sans aucun prix sourçable, page marque sans fiche produit publique) : `python3 tools/autopilote.py bloquer <slug> "raison courte"`, puis retour à l'étape 3. **Deux tentatives au maximum par exécution.**

**Liens internes, toujours dans les phrases** : jamais de bloc « À lire aussi », jamais de ligne de renvoi `→`, jamais de liste de liens en fin de section (contrôle bloquant). L'ancre reprend le mot-clé de la page cible (« taux de cendres », « ramonage d'un poêle à pellets »), jamais « ici » ni un titre entier ; la phrase doit rester correcte quand le lien est retiré. **Variez l'ancre vers une même page** (demande du propriétaire, 15/10/2026) : vers la page mère, alternez « bois de chauffage », « bois de chauffage en Wallonie », « bois de chauffage en Belgique », « acheter du bois de chauffage », « pellets en Belgique », « granulés de bois », « pellets de chauffage »… Avant d'écrire le lien, regardez les ancres que les autres articles utilisent déjà (`grep -o "\[[^]]*\](/pellets/)" articles/*.md`) et prenez une variante peu employée. N'empruntez jamais l'ancre d'une autre page (« prix du bois de chauffage » mène à `/prix-bois-de-chauffage/`). D'abord la page mère, dans le premier tiers du texte (contrôle bloquant). Puis 2 à 3 guides de la même verticale. Un ou deux liens vers un guide d'une autre verticale sont permis quand le sujet l'appelle vraiment (l'entretien du poêle renvoie vers la qualité des pellets, le ramonage vers l'entretien), jamais pour remplir. Utilise les slugs de la sitemap, **même si ces pages ne sont pas encore publiées** : le rendu retire les liens vers des pages absentes, le maillage les réactive le jour où elles sortent. Jamais de lien vers une URL absente de la sitemap.

**Maillage généré** : seule la page mère place `::guides` là où elle présente ses guides ; il se remplit seul avec les pages en ligne et se met à jour chaque matin. Un guide n'a aucun bloc généré : ses liens vers les sœurs sont écrits dans son texte. Vérifie avant de programmer qu'il reçoit au moins un lien entrant d'un article existant (sinon, ajoute une phrase avec un lien dans cet article).

**Pages marques** (Piron, Gamma, Hubo…) : publicité comparative encadrée par le Code de droit économique (livre VI). Caractéristiques factuelles et sourcées uniquement, aucun dénigrement, aucune formulation qui laisse croire à un partenariat, aucun logo.

**Image à la une** : rien à faire, `publier` la génère et la pose (dessin sans texte, un motif par verticale). Si une photo du propriétaire convient au sujet dans `photos/`, mets-la en front-matter : `image_une: photos/<fichier>` et `image_une_alt: <description>`.

**Photos** : si `photos/` contient une photo utile au lecteur (reconnaître, comparer, vérifier), intègre-la par `![[photos/<fichier>|légende|texte alternatif]]` ; `publier` la prépare et l'envoie. Regarde-la d'abord (outil Read) : sujet exact, bien redressée. Ne télécharge **jamais** de photo depuis le web pendant une exécution : note le besoin dans les notes de production, sous « PHOTOS À TROUVER ».

**Schémas** : un SVG seulement s'il montre un mécanisme mieux qu'un paragraphe, un par article au plus. Même style que `visuels/` : traits en `currentColor`, texte de 11 à 13 px, `aria-label` complet. Fichier `visuels/<slug>-<sujet>.svg`, intégré par `![[visuels/…svg|légende]]`.

## 5. Contrôler puis programmer
**Relis la liste des H2 seule**, sans le texte : chaque titre doit dire de quoi parle sa section et à quelle recherche il répond. Puis relis la première phrase de chaque paragraphe : elle doit porter l'idée.

`python3 tools/autopilote.py verifier <slug>` : corrige chaque point bloquant et relance jusqu'à ce qu'il n'en reste aucun. Corrige aussi les avertissements quand c'est raisonnable.

`python3 tools/autopilote.py publier <slug>` : programme l'article à une heure aléatoire, au moins 18 h après le précédent, jamais entre 22 h et 7 h. Aucune autre voie de publication.

## 6. Compte rendu
Termine par trois lignes au plus : l'article programmé et sa date de sortie · ce qui a été bloqué et pourquoi · ce qui attend le propriétaire (d'après `etat` : menu, `/devis/`, articles bloqués).

Le **lundi** (commande `date`), lance aussi `python3 tools/autopilote.py audit`.

Notification : **seulement** en cas d'échec de connexion, ou le lundi — une ligne : articles publiés la semaine passée, pages sans lien entrant, et ce qui attend le propriétaire.

## Interdits
- Afficher le contenu de `setup/.env`.
- Modifier ou supprimer un contenu WordPress non produit depuis `articles/`, une catégorie, un réglage.
- Retoucher un article signalé « repris à la main » : le propriétaire l'a modifié, il est à lui.
- Publier plus d'un article par exécution.
- Modifier le moteur commun (`../../moteur/`) : il sert tous les sites.
- Lancer `autopilote.py theme` ou toucher à `theme/` : l'habillage du site se règle en session avec le propriétaire.
