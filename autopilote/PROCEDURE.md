# Une exécution du pilote automatique — elagage-luxembourg.com

Objectif : **un article par jour, à une heure qui varie**, sans jamais publier un fait non vérifié, un lien cassé, une note interne ni une page de ville interchangeable.

Toutes les commandes se lancent depuis le dossier du site :
`/Users/thomasdufour/Documents/CLAUDE.nosync/SITES/sites/elagage`

Les outils (`tools/autopilote.py`, `tools/images.py`) sont des lanceurs du moteur commun (`../../moteur/`). Ne modifie jamais le moteur pendant une exécution du pilote : il sert tous les sites.

## 1. État du site
`python3 tools/autopilote.py etat`

- La commande publie d'abord les articles programmés restés en retard (le cron WordPress ne tourne qu'avec des visites).
- Si elle échoue sur une erreur de connexion (HTTP 401/403, site injoignable) : envoie la notification « Pilote élagage : WordPress refuse la connexion, mot de passe d'application à vérifier » et arrête-toi.
- Si **2 articles ou plus sont déjà programmés**, ne rédige rien aujourd'hui : passe à l'étape 6.

## 2. Maillage
`python3 tools/autopilote.py maillage`
Réactive dans les pages en ligne les liens vers les pages publiées depuis (l'accueil et les mères locales citent déjà toutes les communes : leurs liens s'allument tout seuls).

## 3. Choisir l'article
`python3 tools/autopilote.py suivant` donne le prochain slug. Lis sa ligne dans `strategie/sitemap-urls.csv` : titre, verticale, cluster, rôle, étape, note. **La file `autopilote/file-attente.txt` applique l'ordre voulu par le propriétaire : ne la réordonne pas.** Elle suit la sitemap : les 4 mères locales, puis les villes (Beckerich d'abord, puis par cercles de distance autour de Beckerich, les plus peuplées d'abord ; élagage puis abattage pour chaque ville), puis dessouchage et plantation dans 5 grandes villes, la page test haubanage, puis les guides.

Trois sortes de pages :

**Mère locale** (`elagage-luxembourg`, `abattage-arbre-luxembourg`, `elagage-province-de-luxembourg`, `abattage-arbre-province-de-luxembourg`, `haubanage-arbre-luxembourg`, cluster « Mère locale ») : `type: page`, sans catégorie, `besoin` du service. Elle cible la requête pays ou province (« élagage luxembourg », « élagueur luxembourg »…) avec le **brief complet** (étape 4). Elle présente le service sur ce territoire, la démarche, puis **toutes les communes du territoire présentes dans la sitemap**, groupées par région en cartes `::choix`, chacune avec son lien vers sa page de ville (même non publiée : le maillage l'activera). Lien vers la page service (`/elagage/` ou `/abattage-arbre/`) dans le premier tiers. CTA fort après l'intro et en fin de page.

**Page de ville** (cluster « Ville ») : **elle part toujours du modèle** : `python3 tools/autopilote.py modele <slug>` crée le fichier (élagage, abattage, dessouchage ou plantation) avec la structure, les titres au nom de la ville et les consignes. Le brief n'est pas exigé (réglage du site : `seo.brief_locales_facultatif`) ; une recherche web rapide sur « élagage <ville> » ou « élagueur <ville> » suffit pour les variantes.

**Ce qui rend une page de ville propre** — chaque section repose sur une donnée de *cette* commune, trouvée pendant l'exécution, sourcée dans les notes (« URL DES SOURCES ») :
- les villages et sections de la commune (site officiel de la commune) ;
- le relief et les accès (vallée, plateau, centre ancien, rues étroites) quand une source le décrit ;
- les arbres typiques du coin (vergers, hêtraies, épicéas…) seulement s'ils sont sourcés (commune, ANF, SPW, parc naturel) ;
- le parc à conteneurs ou le recyparc qui sert la commune et ce qu'il accepte en déchets verts (SIDOR, SIGRE, SIDEC… au Grand-Duché ; AIVE en province) ;
- les arbres remarquables classés de la commune, s'il y en a ;
- les communes voisines (liens vers leurs pages dans la sitemap) et la mère locale du pays (colonne `note`).

**Aucune entreprise citée** : la page renvoie au formulaire, qui transmet la demande à un professionnel de la région. Pas de prix chiffré sans source publique datée : explique ce qui fait varier le prix. Les deux pages d'une même ville (élagage, abattage) ne disent pas la même chose et se lient l'une l'autre. Le contrôle refuse une page dont plus de 50 % du texte se retrouve dans une autre page de ville : écris chaque section à partir des données de la ville, jamais en recopiant la ville précédente.

**Guide** : brief complet, `categorie` de sa verticale (Élagage, Abattage, Plantation), liens vers la page service et 2 à 3 guides.

## 4. Rédiger ou terminer
Si `articles/<slug>.md` n'existe pas, écris-le (page de ville : `modele <slug>` d'abord). S'il existe, termine-le.

**Le brief** (mères locales et guides) : `python3 tools/autopilote.py brief <slug>`. S'il s'arrête sur « IA non joignable », lis le fichier `.prompt.md` indiqué, réponds-y toi-même en JSON dans le `.json` indiqué (sérieusement : c'est l'analyse qui fait l'article), et relance la même commande jusqu'au bout. Rédige ensuite en suivant le plan de `briefs/<slug>/brief.md`.

Relis d'abord `articles/00-charte-redactionnelle.md` et l'article modèle `articles/elagage.md`. Ils font foi pour la forme, le ton et la syntaxe. Les règles qui comptent le plus sur ce site :
- **L'« En bref » est un paragraphe de 2 à 3 phrases**, jamais une liste, qui donne la réponse et le conseil à retenir ; **l'introduction ne le répète pas** : elle part de la situation du lecteur, avec une entrée en matière différente à chaque page.
- **Au moins trois blocs différents par page** : `::choix`, `::citation` (une phrase forte de la page, jamais attribuée à quelqu'un), `::avis`, `::checklist` ou `::avantages`, `::chiffres` (chiffres sourcés seulement), encadrés `> 💡` / `> ⚠️`, tableau.
- Phrases simples, sans formule d'élan ; une liste à puces par article (deux au plus) ; toujours un paragraphe entre un H2 et un H3.

**Front-matter** : les mêmes champs que l'article modèle et que le modèle de ville. `categorie` : Élagage, Abattage ou Plantation (jamais pour une `type: page`). `besoin` : elagage, abattage, dessouchage, haubanage ou plantation, selon la page : c'est lui que le formulaire transmet.

**Les faits sont sourcés ou retirés.** Toute affirmation réglementaire, normative ou chiffrée repose sur une source primaire trouvée pendant l'exécution (site de la commune, intercommunale, administration, organisme officiel). Source trouvée : écris le fait et cite-la sur la ligne finale `*Sources : Nom · Nom — vérifié en <mois année>.*`. **Le nom seul, jamais de lien sortant** (contrôle bloquant) : les URL vont dans les notes, sous « URL DES SOURCES ». Pas de source : reformule sans le fait. **Il ne doit rester aucun marqueur `[À VÉRIFIER]` ni aucune consigne entre crochets du modèle.** Pas de pages sur les permis et la réglementation d'abattage (choix du propriétaire) : une phrase prudente suffit quand le sujet se présente.

Si le cœur de la page repose sur des données introuvables (commune sans aucune information publique exploitable) : `python3 tools/autopilote.py bloquer <slug> "raison courte"`, puis retour à l'étape 3. **Deux tentatives au maximum par exécution.**

**Liens internes, toujours dans les phrases** (ou dans les cartes `::choix`) : jamais de bloc « À lire aussi », jamais de ligne `→`. L'ancre reprend le mot-clé de la page cible (« élagage à Arlon », « abattage d'arbre au Luxembourg »). Utilise les slugs de la sitemap même si les pages ne sont pas encore publiées. Vérifie que la page reçoit au moins un lien entrant (l'accueil et les mères locales en donnent aux villes).

**Images** : l'image à la une est posée par `publier`. Les photos déjà dans `photos/` (crédits dans `photos/credits.json`) peuvent servir quand elles montrent exactement le sujet de la section. Ne télécharge pas de nouvelle photo pendant une exécution : note le besoin sous « PHOTOS À TROUVER ».

## 5. Contrôler puis programmer
**Relis la liste des H2 seule**, puis la première phrase de chaque paragraphe.

`python3 tools/autopilote.py verifier <slug>` : corrige chaque point bloquant et relance jusqu'à ce qu'il n'en reste aucun. Corrige aussi les avertissements quand c'est raisonnable (texte commun avec une autre ville au-delà de 35 % : réécris).

`python3 tools/autopilote.py publier <slug>` : programme l'article à une heure aléatoire, au moins 18 h après le précédent. Aucune autre voie de publication.

## 6. Compte rendu
Trois lignes au plus : l'article programmé et sa date de sortie · ce qui a été bloqué et pourquoi · ce qui attend le propriétaire (d'après `etat`). Ajoute une ligne au journal `autopilote/journal.md` : sources trouvées pour la ville, données manquantes.

Le **lundi** (commande `date`), lance aussi `python3 tools/autopilote.py audit`.

## Interdits
- Afficher le contenu de `setup/.env`.
- Modifier ou supprimer un contenu WordPress non produit depuis `articles/`, une catégorie, un réglage, une extension.
- Retoucher un article signalé « repris à la main ».
- Publier plus d'un article par exécution.
- Modifier le moteur commun, lancer `autopilote.py theme` ou toucher à `theme/` : l'habillage se règle en session avec le propriétaire.
- Citer une entreprise d'élagage, ou utiliser le nom « Élagage Luxembourg » (entreprise existante).
