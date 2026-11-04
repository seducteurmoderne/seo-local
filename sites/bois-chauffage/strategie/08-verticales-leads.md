# Le site n'est pas un site de bois de chauffage

> **24/10/2026 — décision du propriétaire.** La verticale « Poêlier » devient deux verticales produit, **Poêle à pellets** et **Poêle à bois** (pages mères `/poele-a-pellets/`, `/poele-a-bois/`, besoin `poelier`), avec des pages de ville pour les grandes villes (Namur, Liège, Charleroi, Mons, Arlon, Tournai, Verviers, Wavre, Marche-en-Famenne, Bastogne). L'entretien est un cluster de chacune, pas une catégorie. Une catégorie **Fournisseurs** accueille des fiches de sociétés (coordonnées, produits, zone), nourries par les requêtes de marque de la Search Console. Sur google.be (24/10/2026), « poêle à pellets » est tenu par les boutiques et les marques ; « poêle à pellets namur » ou « poêle à bois liège » montrent des poêleries locales et un annuaire d'installateurs : c'est là que se prend le lead.

**6 sept. 2026** — correction de cadrage

## L'erreur

J'ai jugé chaque requête à l'aune d'un seul produit : « est-ce que ça vend du bois ? » Non → page d'autorité, priorité basse.

Mais le modèle n'est pas la vente de bois, c'est **la collecte et le routage de leads**. Chaque requête doit être jugée à une autre question : **existe-t-il un réseau de partenaires prêt à payer pour ce lead ?**

Deux verdicts à réviser :

| Requête | Volume | KD | Mon verdict | Le bon verdict |
|---|---|---|---|---|
| `entretien poele a pellet` | **480** | **9** | « autorité, ne convertit pas » | **Lead poêlier** |
| `prix poele a pellet` | 320 | 10 | « autorité » | **Lead poêlier** |
| Ramonage | à tester | — | « cul-de-sac » | **Lead ramoneur** |

## Le site est une plateforme de leads du chauffage au bois

Quatre verticales possibles, une seule audience, une seule grille géographique, un seul routage par code postal :

| Verticale | Partenaires | Nature du besoin |
|---|---|---|
| **Bois de chauffage** | Négociants, scieries, exploitants | Saisonnier, souvent ponctuel |
| **Pellets** | Négociants, GSB, producteurs | Saisonnier, récurrent |
| **Ramonage** | Ramoneurs agréés | **Annuel et obligatoire en Wallonie** |
| **Poêlier** | Installateurs, dépanneurs | Ponctuel, panier élevé |

### Ce que ça change vraiment
**Un même visiteur peut produire deux leads.** Quelqu'un qui demande un devis bois est, par définition, un utilisateur de foyer — donc soumis à l'obligation de ramonage annuelle. Le formulaire pose la question, le coût d'acquisition du second lead est nul.

Et le ramonage est **récurrent** là où une commande de bois peut être ponctuelle : le même contact revient chaque année.

## La conséquence sur l'architecture

Quatre verticales × 86 zones géographiques = 344 pages locales. Ingérable, et c'est le profil doorway garanti.

**La solution, qui règle aussi l'arbitrage laissé ouvert : une seule page locale par zone, couvrant toutes les verticales.**

> `/chauffage-bois-namur/` — « Se chauffer au bois à Namur : fournisseurs de bûches et de pellets, ramoneurs, poêliers »

Un seul formulaire, dont **la première question est « de quoi avez-vous besoin ? »**. Ce n'est pas deux CTA en concurrence : c'est un CTA unique avec une étape de qualification — exactement le rôle que joue déjà le calculateur.

Trois bénéfices d'un coup :
- La page devient réellement riche, ce qui la sort du risque doorway
- Le nombre de pages locales tombe de 344 à **86**
- Chaque visiteur local est exposé aux quatre offres, sans friction

Les **guides restent totalement séparés** par verticale : c'est là que la distinction produit sert le lecteur.

### Nouveau décompte indicatif
| Bloc | Pages |
|---|---|
| Homepage | 1 |
| Mères de verticale | 4 |
| Guides bois / pellets | 40 |
| Guides ramonage / poêlier | ~16 |
| Local, toutes verticales confondues | 86 |
| Hors catégorie | 7 |
| **Total** | **~154** |

Moins de pages qu'avant (222), pour deux fois plus de produits.

## Le préalable, qui n'est pas du SEO

Chaque verticale exige **son propre réseau de partenaires**. Un lead ramonage sans ramoneur à qui l'envoyer ne vaut rien, et une page qui promet trois devis sans pouvoir les livrer détruit la confiance plus vite qu'elle ne la construit.

L'ordre logique : ouvrir une verticale **quand le réseau existe**, pas avant. Le SEO peut préparer les pages, il ne peut pas fabriquer les partenaires.

## À mesurer avant de décider
`mots-cles-lot-5-services.txt` — 100 mots-clés : ramonage national et par ville, poêlier et installation, tubage, élagage et abattage, bois en grume.

C'est le test qui dira si ces verticales pèsent réellement. Note que je n'avais jamais testé la bonne requête : j'ai jugé le ramonage sur `ramonage obligatoire wallonie` (0) alors que la requête à leads est **`ramoneur [ville]`** — l'exact équivalent de `bois de chauffage [ville]`, qui lui a du volume dans 24 villes sur 26.
