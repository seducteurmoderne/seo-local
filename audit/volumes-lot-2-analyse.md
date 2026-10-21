# Analyse du lot 2 — volumes Semrush réels
**5 sept. 2026** · Source : `data/volumes-propres.csv` (100 mots-clés, base Belgique)
Le lot 1 (cluster bois de chauffage) n'a pas encore été extrait.

## Totaux par cluster

| Cluster | Volume/mois | Mots-clés | Dont volume > 0 |
|---|---|---|---|
| **Comparateur d'énergies** | **13 640** | 17 | 11 |
| Local — bois par ville | 1 160 | 26 | 25 |
| Poêles / appareils | 860 | 4 | 4 |
| Pellets, compléments | 750 | 26 | 16 |
| Primes / réglementation | 370 | 12 | 7 |
| Local — provinces | 280 | 5 | 3 |
| Local — pellets par ville | 160 | 10 | 7 |
| **Total** | **17 220** | 100 | 73 |

---

## 1. Le comparateur d'énergies écrase tout — mais pas là où je le pensais

| Mot-clé | Volume | KD |
|---|---|---|
| **prix mazout belgique** | **12 100** | **59** |
| prix gaz belgique | 1 300 | 23 |
| chauffage economique | 90 | — |
| cout chauffage maison | 30 | — |

À lui seul `prix mazout belgique` pèse **70 % du lot**. Mais le trafic n'est pas sur « comparaison chauffage » ou « quel chauffage choisir » — il est sur **le prix de l'énergie que les gens utilisent déjà**. Personne ne cherche à comparer ; les gens vérifient ce que coûte leur mazout, et c'est à ce moment-là qu'ils sont réceptifs à une alternative.

**KD 59, c'est hors de portée à court terme** pour un domaine sans autorité. La séquence réaliste :
1. `prix gaz belgique` (1 300, KD 23) — atteignable
2. Les requêtes secondaires du cluster
3. `prix mazout belgique` — objectif à 12-18 mois, pas avant

**L'angle qui relie tout** : quelqu'un qui vérifie le prix du mazout subit une facture. « Le mazout vous coûte X — voici ce que coûterait le pellet chez vous » → calculateur → devis. Le comparateur devient l'aimant à trafic, et le calculateur son outil de conversion.

## 2. Le local fonctionne — villes seulement, bois seulement

| Mot-clé | Volume | KD |
|---|---|---|
| bois de chauffage namur | 210 | 11 |
| bois de chauffage liege | 170 | **6** |
| bois de chauffage brabant wallon | 170 | 17 |
| bois de chauffage charleroi | 110 | **6** |
| bois de chauffage hainaut | 90 | — |
| bois de chauffage mons / nivelles / tournai | 70 chacun | — |

Volumes modestes, **difficulté quasi nulle** (KD 6 sur Liège et Charleroi) et intention d'achat maximale. C'est exactement le profil du lead-gen : peu de trafic, mais le meilleur taux de conversion du site.

**Ce qui est mort, en revanche** :
- **Les provinces** : `province de luxembourg`, `province de namur`, `condroz` → **volume nul**. Seuls `brabant wallon` (170) et `hainaut` (90) tiennent — ce sont des régions que les gens nomment, pas des provinces administratives.
- **Les pellets par ville** : `livraison pellets liege`, `livraison pellets namur`, `livraison pellets charleroi` → **tous à zéro**. Le local, c'est du bois bûche, pas du pellet.

→ Le cluster 3 doit être **exclusivement bois, exclusivement par ville**.

## 3. Les primes wallonnes : thèse à abandonner

| Mot-clé | Volume |
|---|---|
| prime chauffage wallonie | 170 |
| prime poele a pellet | 70 |
| primes habitation wallonie | 50 |
| ramonage obligatoire wallonie | **0** |
| norme ecodesign poele | **0** |
| interdiction feu ouvert belgique | **0** |
| certificat peb chauffage | **0** |

370/mois pour tout le cluster. J'en avais fait un « fossé défensif » : c'est faux. Le sujet est peut-être utile en contenu de confiance, il n'est pas un levier de trafic. **Déclassé.**

## 4. Une piste non prévue : les appareils

| Mot-clé | Volume | KD |
|---|---|---|
| entretien poele a pellet | 480 | **9** |
| prix poele a pellet | 320 | **10** |

Volumes corrects, difficulté très basse. Réserve honnête : celui qui cherche l'entretien de son poêle n'achète pas de pellets dans la minute. À traiter comme trafic d'autorité, pas comme page à leads.

## 5. Ce qui est à zéro — et ce que ça vaut

27 mots-clés sans volume mesuré. Les plus instructifs :

- `combien de pellets par hiver`, `consommation pellets maison`, `combien de sac de pellets par hiver` → **0**
- `pellets ou mazout`, `pellet ou bois de chauffage`, `comparatif energie chauffage belgique` → **0**
- `fournisseur pellets belgique`, `prix palette pellets belgique`, `pellets en vrac prix` → **0**

> **Nuance méthodologique** : Semrush sous-estime la traîne longue, surtout sur un marché aussi petit que la Belgique francophone. Un « 0 » signifie souvent « sous le seuil de mesure », pas « personne ne cherche ». Mais l'ordre de grandeur reste le message : **ces requêtes ne portent pas de trafic**, et rien ne doit être priorisé sur elles.

---

## Conséquence directe : le calculateur de pellets

Je l'ai construit en le présentant comme un aimant à trafic, sur la base d'un raisonnement de marché — pas de données. Les chiffres disent que **la requête n'existe pas** à un volume mesurable.

L'outil garde sa valeur, mais son rôle change : ce n'est **pas une page d'entrée**, c'est un **dispositif de conversion** à placer sur les pages qui, elles, reçoivent du trafic — le comparateur d'énergies, les pages villes, la mère pellets. Il ne mérite pas sa propre page optimisée SEO ; il mérite d'être là où les gens arrivent déjà.

---

## Ce qui manque encore

1. **Le lot 1 n'est pas extrait.** Tout le cluster bois de chauffage — dont la requête mère `bois de chauffage belgique` — reste sans volume. C'est le trou le plus important, et c'est le cluster que le local vient de valider.
2. **Les volumes 2024 doivent être re-mesurés.** Le fichier d'origine annonçait `prime pellet` à 2 400/mois ; Semrush donne aujourd'hui 70 à 170 sur les formulations voisines. Les libellés exacts diffèrent, donc ce n'est pas forcément une contradiction — mais **toute la priorisation du cluster pellets repose sur ces chiffres de 2024**, marques comprises (`pellet piron` 2 400, `pellets gamma` 1 300). Il faut les repasser dans Semrush, même base, même jour, pour disposer d'un jeu de données cohérent.
