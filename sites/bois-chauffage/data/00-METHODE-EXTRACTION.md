# Extraction Semrush — méthode

## ⚠️ Réglage critique, avant tout
**Base de données : Belgique.** Pas France, pas « Worldwide ».
C'est l'erreur qui invaliderait tout : `pellet hubo`, `pellets aveve`, `pellets brico` sont des enseignes belges. En base France elles sortent à zéro, et on conclurait à tort qu'il n'y a pas de marché.

---

## Ordre des trois passes

Elles ne se remplacent pas : la première décrit le marché réel, la deuxième découvre ce qu'on n'a pas imaginé, la troisième valide l'architecture. Faites dans cet ordre, chacune informe la suivante.

### Passe 1 — Les concurrents (la plus riche)
C'est la seule source qui montre le marché tel qu'il est, et pas tel qu'on l'imagine.

1. `Organic Research` → entrer **bois-de-chauffage-et-pellets.be** → onglet **Competitors**
   Semrush sort les domaines qui se positionnent sur les mêmes requêtes. Noter les 3-5 plus proches qui sont réellement belges.
2. Pour chacun : `Organic Research` → **Positions** → filtrer **Volume > 50** → exporter en CSV.
3. Déposer les exports ici, nommés `concurrent-<domaine>.csv`.

> Si l'onglet Competitors ne renvoie rien d'exploitable (probable, le site n'a qu'une page positionnée), passer directement par une requête : chercher `bois de chauffage belgique` dans **Keyword Overview**, regarder qui occupe la première page, et prendre ces domaines-là.

### Passe 2 — Keyword Magic Tool (découverte)
Trois seeds, base Belgique, une extraction chacun :

- `bois de chauffage`
- `pellets`
- `stère`

Trier par volume décroissant, exporter les 500 premiers de chaque. C'est ce qui rattrapera les formulations auxquelles on n'a pas pensé — et dans cette niche, le vocabulaire belge réserve des surprises.

Fichiers : `magic-bois.csv`, `magic-pellets.csv`, `magic-stere.csv`

### Passe 3 — Bulk Analysis (validation)
`Keyword Overview` → **Bulk Analysis** → coller le contenu de `mots-cles-lot-1.txt`, exporter. Puis idem avec le lot 2.

Ces deux listes couvrent exactement les trous de l'architecture : la mère du cluster bois, les prix, les unités, les essences, le local, le comparateur d'énergies, et les compléments pellets absents de la recherche de 2024.

Fichiers : `bulk-lot-1.csv`, `bulk-lot-2.csv`

---

## Ce qu'on en fera
Croisement des trois passes pour produire, par cluster : le volume réel de la mère, la hiérarchie des filles, les pages à abandonner faute de demande, et les pages auxquelles on n'avait pas pensé. C'est ce qui débloque les clusters 2 et 3, aujourd'hui construits à l'aveugle.

## Ce qui n'attend pas
La Phase 0 (navigation, cache, robots.txt, correctifs) et le cluster pellets sont déjà chiffrés. Ils avancent pendant l'extraction.
