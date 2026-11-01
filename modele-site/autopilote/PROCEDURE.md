# Une exécution du pilote automatique

Objectif : **environ un article par jour, à une heure qui varie**, sans jamais publier un fait non vérifié, un lien cassé ni une note interne.

Toutes les commandes se lancent depuis le dossier du site (`sites/<site>/` du dépôt, celui qui contient `site.json`).

Les outils (`tools/autopilote.py`, `tools/images.py`) sont des lanceurs du moteur commun (`../../moteur/`). Ne modifie jamais le moteur pendant une exécution du pilote : il sert tous les sites.

## 1. État du site
`python3 tools/autopilote.py etat`

- La commande publie d'abord les articles programmés restés en retard (le cron WordPress ne tourne qu'avec des visites).
- Si elle échoue sur une erreur de connexion (HTTP 401/403, site injoignable) : envoie la notification « Pilote {{DOMAINE}} : WordPress refuse la connexion, mot de passe d'application à vérifier » et arrête-toi.
- Si **2 articles ou plus sont déjà programmés**, ne rédige rien aujourd'hui : passe à l'étape 6.

## 2. Maillage
`python3 tools/autopilote.py maillage`
Réactive dans les articles en ligne les liens vers les pages publiées depuis, et installe les formulaires de devis dès que le plugin de réception est actif.

## 3. Choisir l'article
`python3 tools/autopilote.py suivant` donne le prochain slug. Lis sa ligne dans `strategie/sitemap-urls.csv` : titre, verticale, cluster, rôle, CTA. La file `autopilote/file-attente.txt` fixe l'ordre voulu par le propriétaire : ne la réordonne pas.

**Page locale** (si le site en a) : `categorie` = la catégorie locale de `site.json`, `besoin` explicite. Le contenu vient de la ligne de la ville dans le fichier de données terrain du propriétaire (`setup/donnees-locales.csv`) et de rien d'autre ; une colonne vide n'est pas comblée, un prestataire marqué « à confirmer » ou « À VÉRIFIER » est écarté. Une page locale est unique par ses données : jamais un gabarit dont on remplace le nom de la ville. Si la ville n'a pas assez de données propres (moins de deux prestataires utilisables), `python3 tools/autopilote.py bloquer <slug> "raison courte"` et passe à la suivante : mieux vaut sauter une ville que publier une page mince (risque « doorway pages » sur tout le domaine). CTA fort juste après l'intro et en fin de page.

## 4. Rédiger ou terminer
Si `articles/<slug>.md` n'existe pas, écris-le. S'il existe, termine-le.

Relis d'abord `articles/00-charte-redactionnelle.md` et l'article modèle désigné dans `CLAUDE.md`. Ils font foi pour la forme, le ton et la syntaxe.

**Front-matter** : les mêmes champs que l'article modèle. `categorie` vaut l'une des catégories de `site.json` → `verticales`. Les pages mères prennent `type: page`, sans catégorie : elles présentent la verticale, répondent elles-mêmes avec des chiffres sourcés, renvoient vers leurs guides (`::guides`) et portent un CTA fort.

**Champ `besoin`** : la case cochée par défaut dans le formulaire de devis, selon le besoin réel du visiteur (une des `cle` de `site.json` → `formulaire.besoins`). Omets-le quand il coïncide avec la catégorie.

**Avant d'écrire : les recherches réelles.** Recherche web sur la requête cible ; note les recherches associées (suggestions, « Autres questions posées », titres des premiers résultats) dans `mots_cles_secondaires:`. Les H2 en sont tirées : deux au moins reprennent la requête cible (contrôle bloquant). Pas de FAQ sauf si trois questions réelles restent sans réponse dans le corps.

**Ton.** Ce que `setup/terrain-auteur.md` contient sur le sujet est repris ; rien d'autre ne se raconte à la première personne. Dis ce que la rédaction a fait (relevés, calculs) et donne un avis argumenté. Au moins deux éléments de rythme (`::chiffres`, encadré `> 💡`/`> ⚠️`, tableau) au-delà de 800 mots.

**Les faits sont sourcés ou retirés.** Toute affirmation réglementaire, normative ou chiffrée (prix, obligation légale, seuil de norme, montant de prime) doit reposer sur une source primaire trouvée pendant l'exécution : site officiel pour la réglementation, organisme émetteur pour une norme, source publique datée pour un prix (avec le mois du relevé).
Source trouvée : écris le fait et cite-la sur la ligne finale `*Sources : Nom · Nom — vérifié en <mois année>.*`. **Le nom seul, jamais de lien sortant** (contrôle bloquant) : les URL vont dans les notes de production, sous « URL DES SOURCES ».
Pas de source primaire : reformule sans le fait. **Il ne doit rester aucun marqueur `[À VÉRIFIER]`.**

Si le cœur de l'article repose sur des données introuvables : `python3 tools/autopilote.py bloquer <slug> "raison courte"`, puis retour à l'étape 3. **Deux tentatives au maximum par exécution.**

**Liens internes, toujours dans les phrases** : jamais de bloc « À lire aussi », jamais de ligne `→`, jamais de liste de liens en fin de section (contrôle bloquant). L'ancre reprend le mot-clé de la page cible. D'abord la page mère, dans le premier tiers du texte (contrôle bloquant), puis 2 à 3 guides de la même verticale. Utilise les slugs de la sitemap même si ces pages ne sont pas encore publiées : le rendu retire les liens vers des pages absentes, le maillage les réactive le jour où elles sortent. Vérifie que l'article reçoit au moins un lien entrant d'un article existant.

**Image à la une** : rien à faire, `publier` la génère (dessin sans texte, un motif par verticale). Une photo du propriétaire dans `photos/` peut la remplacer : `image_une: photos/<fichier>` et `image_une_alt: <description>`.

**Photos** : seulement celles du propriétaire (`photos/`), intégrées par `![[photos/<fichier>|légende|texte alternatif]]`. Ne télécharge jamais de photo depuis le web : note le besoin sous « PHOTOS À TROUVER ».

**Schémas** : un SVG seulement s'il montre un mécanisme mieux qu'un paragraphe, un par article au plus, dans `visuels/`.

## 5. Contrôler puis programmer
`python3 tools/autopilote.py verifier <slug>` : corrige chaque point bloquant et relance jusqu'à ce qu'il n'en reste aucun.

`python3 tools/autopilote.py publier <slug>` : programme l'article à une heure aléatoire. Aucune autre voie de publication.

## 6. Compte rendu
Trois lignes au plus : l'article programmé et sa date de sortie · ce qui a été bloqué et pourquoi · ce qui attend le propriétaire (d'après `etat`).

Le **lundi**, lance aussi `python3 tools/autopilote.py audit`.

## Interdits
- Afficher le contenu de `setup/.env`.
- Modifier ou supprimer un contenu WordPress non produit depuis `articles/`, une catégorie, un réglage.
- Retoucher un article signalé « repris à la main ».
- Publier plus d'un article par exécution.
- Modifier le moteur commun.
