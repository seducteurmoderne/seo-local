# Sitemap — URLs plates
**5 sept. 2026** · Liste complète des 228 URLs : [`sitemap-urls.csv`](sitemap-urls.csv)

Deux catégories (bois, pellets), chacune avec ses guides et son local. Le reste hors catégorie.
**Toutes les URLs sont de premier niveau.** Le silo se construit par les liens internes et les catégories WordPress, jamais par la profondeur d'URL.

---

## Convention de nommage

Comme tous les slugs partagent un seul espace de noms, le préfixe porte la catégorie :

| Type | Modèle | Exemple |
|---|---|---|
| Mère | `/<categorie>/` | `/bois-de-chauffage/` · `/pellets/` |
| Guide bois | sujet explicite | `/stere-de-bois/` · `/longueur-buches/` |
| Guide pellets | sujet explicite | `/pellets-piron/` · `/taux-cendres-pellets/` |
| Guide en doublon de sujet | préfixé par catégorie | `/stockage-bois-de-chauffage/` vs `/stockage-pellets/` · `/prix-bois-de-chauffage/` vs `/prix-pellets/` |
| Local ville | `<categorie>-<ville>` | `/bois-de-chauffage-namur/` · `/pellets-namur/` |
| Local région | `<categorie>-<region>` | `/bois-de-chauffage-ardenne/` |
| Local province | `<categorie>-province-<nom>` | `/bois-de-chauffage-province-namur/` |

**Aucune collision** sur les 228 slugs (vérifié).

Deux conséquences agréables :
- **`/meilleur-pellet/` ne bouge pas.** Ton article existant est déjà à sa place définitive — zéro redirection.
- Le slug province se distingue naturellement du slug ville (`province-namur` ≠ `namur`), alors que le **H1 emploie le nom naturel** : « Bois de chauffage en Hainaut », jamais « en province de Hainaut ». Les données montrent que le mot « province » n'est jamais tapé.

---

## Implémentation WordPress

En URLs plates, la structure n'existe plus dans l'adresse — elle doit vivre ailleurs :

- **Permaliens** : `/%postname%/`
- **Catégories WP** : `Bois de chauffage` et `Pellets` — c'est elles qui portent la structure
- **Étiquette ou taxonomie** : `guide` / `local` pour la seconde dimension
- **Fil d'Ariane** : à construire **depuis la catégorie**, pas depuis l'URL. Yoast le fait nativement si les catégories sont bien assignées.
- **Menu** : c'est lui qui rend la hiérarchie visible aux visiteurs et aux robots. Sur un site à URLs plates, il n'est plus optionnel — et le tien n'existe pas encore.

---

## Guides — classés par intention

Cinq étages identiques dans les deux catégories. Ce sont les questions de l'acheteur, pas des sujets.

| Intention | Bois de chauffage (20) | Pellets (20) |
|---|---|---|
| **Quoi acheter** | `quel-bois-de-chauffage-choisir` *(sous-hub)* → `-chene` `-hetre` `-charme` `-frene` `-bouleau` · `bois-dur-ou-bois-tendre` · `longueur-buches` · `buches-densifiees` · `bois-a-ne-pas-bruler` | `quelle-marque-de-pellets` *(sous-hub)* → `pellets-piron` `-gamma` `-hubo` `-trafic` `-badger` `-aveve` `-descamps` `-brico` · `certifications-pellets` · `pellets-resineux-ou-feuillus` · `pellets-6-ou-8-mm` |
| **Combien il m'en faut** | `stere-de-bois` · `stere-m3-corde` · `combien-de-steres` *(calculateur)* | `combien-de-pellets` *(calculateur)* · `sac-palette-vrac-pellets` |
| **Bonne marchandise ?** | `bois-de-chauffage-sec` · `verifier-bois-sec` · `temps-sechage-bois` | `meilleur-pellet` *(existe + analyseur)* · `taux-cendres-pellets` · `reconnaitre-mauvais-pellet` |
| **Ce que ça coûte** | `prix-bois-de-chauffage` | `prix-pellets` |
| **Comment m'en servir** | `stockage-bois-de-chauffage` · `allumage-feu-bois` · `quel-appareil-bois` | `stockage-pellets` · `entretien-poele-a-pellets` |

---

## Local — la grille géographique

**5 provinces · 10 régions naturelles · 74 villes**, déclinées dans les deux catégories.

**Provinces** — Brabant wallon · Hainaut · Liège · Luxembourg · Namur

**Régions** — Ardenne · Famenne · Condroz · Gaume · Hesbaye · Pays de Herve · Hautes Fagnes · Botte du Hainaut · Entre-Sambre-et-Meuse · Ourthe-Amblève

**Villes** par province :

| Province | Villes |
|---|---|
| Brabant wallon (12) | Wavre, Nivelles, Ottignies-LLN, Braine-l'Alleud, Waterloo, Tubize, Rixensart, Jodoigne, Genappe, Perwez, Lasne, Court-Saint-Étienne |
| Hainaut (18) | Charleroi, Mons, Tournai, La Louvière, Mouscron, Ath, Soignies, Binche, Châtelet, Courcelles, Fleurus, Thuin, Chimay, Péruwelz, Lessines, Enghien, Braine-le-Comte, Saint-Ghislain |
| Liège (16) | Liège, Seraing, Verviers, Herstal, Ans, Flémalle, Huy, Waremme, Visé, Herve, Spa, Malmedy, Eupen, Hannut, Aywaille, Stavelot |
| Luxembourg (14) | Arlon, Marche-en-Famenne, Bastogne, Libramont, Neufchâteau, Virton, Bouillon, Saint-Hubert, Durbuy, La Roche-en-Ardenne, Houffalize, Bertrix, Vielsalm, Aubange |
| Namur (14) | Namur, Dinant, Ciney, Andenne, Gembloux, Philippeville, Rochefort, Couvin, Walcourt, Sambreville, Beauraing, Florennes, Éghezée, Fosses-la-Ville |

---

## Maillage

| Depuis | Vers | Règle |
|---|---|---|
| Guide fille | Sous-hub, puis mère de catégorie | Lien contextuel, premier tiers de page |
| Guide | 2-3 guides sœurs, + 1-2 guides d'une autre verticale si le sujet l'appelle | La mère reste le premier lien |
| Ville | Sa province + 2-3 villes voisines | Remonte la hiérarchie et tisse le réseau |
| Ville | `/devis/` | **Court-circuit** — le visiteur cherche déjà un fournisseur |
| Région | Ses villes + sa province | — |
| Province | Ses régions et villes + la mère | — |
| Mère | ↔ les autres mères | — |
| Hors catégorie | Les deux mères | Le comparateur est transversal |

---

## Le compte

| Bloc | Pages |
|---|---|
| Homepage | 1 |
| Mères de catégorie | 2 |
| Guides (20 + 20) | 40 |
| Local — villes (74 × 2) | 148 |
| Local — régions (10 × 2) | 20 |
| Local — provinces (5 × 2) | 10 |
| Hors catégorie | 7 |
| **Total** | **228** |

À 3 pages par semaine : **18 mois**. C'est le calendrier réel.

### Phasage
1. **Vague 1** — mères, `/devis/`, les 24 villes déjà mesurées, les 5 provinces
2. **Vague 2** — les 50 villes restantes, une fois le gabarit validé et le relevé de prix en place
3. **Guides** — en continu, par ordre de volume, en commençant par le cluster pellets

### Arbitrage encore ouvert
168 des 228 pages sont locales, et la moitié duplique la géographie entre bois et pellets. Si les deux jumelles d'une commune décrivent la même zone et les mêmes fournisseurs, c'est le profil d'une *doorway page* — et la sanction frappe le domaine.

Fusionner le local (une page par zone couvrant les deux produits, rattachée aux deux mères) ramènerait le total à **144 pages**, chacune deux fois plus riche, sans toucher à la séparation des guides.
