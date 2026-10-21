# Architecture du site — modèle intermédiaire
> Révisé le 5 sept. 2026, après audit. Remplace la version générique initiale.

## Le modèle
Le site capte des demandes de devis et les route vers des fournisseurs partenaires. Conséquence structurante : **le contenu est celui d'un comparateur, le tunnel est celui d'un vendeur unique.**

Ça change deux choses par rapport à un vendeur classique :
1. Les pages locales n'ont plus besoin de preuve de terrain propre (tournées, camions). Elles décrivent **le marché local** — qui livre dans la zone, quelles fourchettes de prix s'y pratiquent, quelles contraintes d'accès. C'est du contenu réel, produisible à grande échelle, et ça ne tombe pas dans le piège des *doorway pages*.
2. Les pages « marques et enseignes » deviennent parfaitement légitimes. Un comparateur qui compare, c'est sa raison d'être.

## Arborescence cible

```
/                                     Homepage — comparateur + entrée du tunnel
│
├── /devis/                           ★ LE TUNNEL — à construire en premier
│
├── /pellets/                         ★ COMPARATIF GÉNÉRAL — page pivot du tunnel
│   ├── /pellets/prix/                        « pellet prix » 1 300/mois · KD 13
│   ├── /pellets/prime/                       « prime pellet » 2 400/mois · KD 19
│   ├── /pellets/marques/                     Hub comparatif des marques
│   │   ├── /pellets/marques/piron/           2 400 · KD 17
│   │   ├── /pellets/marques/gamma/           1 300 · KD 21
│   │   ├── /pellets/marques/hubo/            1 000 · KD 24
│   │   ├── /pellets/marques/trafic/          1 000 · KD 17
│   │   ├── /pellets/marques/badger/            880 · KD 11
│   │   ├── /pellets/marques/aveve/             880 · KD 11
│   │   ├── /pellets/marques/descamps/          880 · KD 10
│   │   └── /pellets/marques/brico/             880 · KD 33
│   └── /meilleur-pellet/                     ← existant, on ne le déplace pas
│
├── /bois-de-chauffage/               Hub bois
│   ├── /bois-de-chauffage/prix/
│   ├── /bois-de-chauffage/stere/             « stère de bois » 1 300/mois · KD 20
│   └── /bois-de-chauffage/essences/          regroupé : chêne, hêtre, frêne, bouleau (20/mois chacun)
│
├── /fournisseurs/                    ★ Hub local — cœur du modèle
│   ├── /fournisseurs/liege/
│   ├── /fournisseurs/namur/
│   ├── /fournisseurs/charleroi/
│   ├── /fournisseurs/brabant-wallon/
│   └── /fournisseurs/luxembourg/
│
├── /outils/
│   ├── /outils/calculateur-pellets/
│   └── /outils/calculateur-steres/
│
└── /partenaires/                     Recrutement de fournisseurs (côté offre)
```

**Décision sur `/meilleur-pellet/`** : on le laisse à la racine. Il a zéro impression, donc zéro risque à le déplacer — mais zéro gain aussi. La profondeur d'URL ne pèse quasiment rien au classement. On corrige son contenu, pas son adresse. Pas de churn inutile.

## Modèle de page « marque / enseigne »
C'est le format le plus rentable du projet. Structure qui fonctionne :

1. **H1** : `Pellets [Marque] : prix, qualité et avis en Belgique (2026)`
2. **Réponse directe en 3 lignes** — le lecteur doit avoir sa réponse avant de scroller
3. **Fiche technique factuelle** : certification (ENplus A1 / DINplus), essence, pouvoir calorifique, taux de cendres, conditionnement, origine
4. **Prix constatés**, datés, avec la mention du mois de relevé
5. **Où l'acheter** : points de vente, disponibilité saisonnière
6. **Comparaison honnête** avec 2-3 alternatives, en tableau
7. **FAQ** (balisage FAQPage)
8. **CTA unique** : vers le **comparatif général** `/pellets/` — jamais vers le devis directement, et jamais deux sorties sur la même page

### Les règles à ne pas enfreindre
Ces pages parlent de marques et d'enseignes tierces. En Belgique la publicité comparative est **licite mais encadrée** (Code de droit économique, livre VI) : elle doit être objective, vérifiable, non trompeuse et non dénigrante.

- Aucune formulation laissant croire à un partenariat ou une affiliation avec Gamma, Hubo, Aveve, Brico, etc.
- Pas de logos de marque dans un contexte suggérant une approbation
- Chaque affirmation comparative doit reposer sur une donnée vérifiable et sourcée
- Pas de dénigrement : on compare des caractéristiques, on ne disqualifie pas un concurrent

Au-delà du droit, c'est aussi une exigence SEO : une page de comparaison sans données réelles est du contenu mince, et Google traite sévèrement les comparateurs sans valeur ajoutée propre.

## Modèle de page locale (`/fournisseurs/[zone]/`)
1. **H1** : `Bois de chauffage et pellets à [Zone] : fournisseurs, prix et livraison`
2. Le marché local : qui livre dans la zone, quels types de fournisseurs (scieries, négociants, GSB, indépendants)
3. Fourchettes de prix **constatées dans cette zone**, datées
4. Spécificités réelles : distances, contraintes d'accès rurales, délais typiques en pleine saison
5. Communes et codes postaux couverts
6. FAQ locale (balisage FAQPage)
7. CTA vers `/devis/` pré-rempli avec la zone

**Règle de production** : si les points 2, 3 et 4 ne peuvent pas être remplis avec de l'information vraie et propre à la zone, la page n'est pas créée. Cinq pages solides valent mieux que trente clonées — le clonage déclenche la sanction *doorway pages* sur l'ensemble du site.

## Maillage — au service du tunnel unique

Le tunnel est : **page d'entrée → comparatif général → devis.** Le maillage doit le servir, pas le contredire.

- Chaque page marque → `/pellets/marques/` → **`/pellets/` (le comparatif)**. C'est le chemin principal, il doit être évident dans le corps du texte, pas seulement en menu
- Chaque page marque → `/pellets/prix/` : celui qui compare une marque veut le prix
- **Pages locales : elles court-circuitent le comparatif et vont droit à `/devis/`.** Leur visiteur cherche déjà un fournisseur ; l'envoyer comparer le fait reculer d'une étape
- Chaque page locale → 2-3 zones voisines, pour former un réseau et non une étoile
- `/devis/` ne renvoie jamais vers du contenu éditorial : c'est un cul-de-sac volontaire
- `/meilleur-pellet/` (existant) → à relier vers toutes les pages marques : il devient le pilier éditorial du silo

**Règle de sortie unique** : une page = une intention = un appel à l'action. Deux CTA concurrents sur une même page n'en font fonctionner aucun.
