# Monétisation : tunnel unique vers le lead
> Révisé le 5 sept. 2026. **Décision : pas d'affiliation.** Toutes les pages convergent vers le comparatif général, qui converge vers le devis.

## La décision
Un seul modèle, un seul tunnel :

```
Page marque / prix / locale  →  COMPARATIF GÉNÉRAL  →  /devis/
```

Pourquoi l'affiliation est écartée :
- Une commission de GSB tourne à 2-5 %, soit 8 à 20 € sur une palette. Un lead chauffage qualifié vaut structurellement plus.
- L'existence de programmes exploitables en Belgique n'est pas établie — plusieurs de ces enseignes sont des groupes néerlandais dont les programmes ciblent parfois les Pays-Bas seuls. Bâtir sur une hypothèse non vérifiée coûte cher.
- Deux modèles sur un site de deux pages, c'est de la complexité prématurée : deux tunnels à construire, à mesurer, à optimiser, pour diluer les deux.

## Le pivot marque → comparatif

Le chercheur « pellet hubo » ne cherche pas Hubo. Il cherche **combien coûtent des pellets corrects et où les prendre** ; Hubo est simplement le nom d'enseigne qui lui vient à l'esprit. Le pivot est donc légitime — à une condition stricte.

### La condition : répondre d'abord, comparer ensuite
La page doit **réellement répondre à la question posée** avant de proposer autre chose. Prix constatés chez l'enseigne, certification des pellets vendus, conditionnement, verdict honnête. Si le verdict est « c'est correct », on l'écrit.

Une page qui esquive la question pour pousser vers un formulaire est un appât : rebond immédiat, signal négatif envoyé à Google, et réputation détruite auprès du seul public qui compte. C'est la différence entre un comparateur et une page satellite — et Google a précisément durci son traitement des secondes.

### Le pont : l'écart de prix
Le passage naturel de « pellets Hubo » vers le comparatif, c'est **l'écart de prix au kilo entre la vente au sac en grande surface de bricolage et la livraison en palette ou en vrac par un fournisseur spécialisé.**

Cet écart est l'argument le plus fort du site, il est factuel, et il justifie le pivot sans manipulation : *« voici le prix chez Hubo, voici ce que coûte la même quantité livrée — à vous de voir »*.

> ⚠️ Cet écart est **supposé, pas mesuré**. Il doit être établi par des relevés réels avant d'être affirmé où que ce soit. S'il s'avère faible sur certaines gammes, on l'écrit aussi : c'est ce qui rend le reste crédible.

## L'actif à construire : le relevé de prix

C'est la recommandation la plus importante de ce document. Un relevé de prix régulier — enseignes, marques, conditionnements, prix au kg et à la tonne, daté — est :

- **la donnée propre** qui sort le site du contenu mince et le qualifie comme comparateur réel ;
- **le carburant de toutes les pages** : chaque page marque, chaque page prix, le comparatif général en vivent ;
- **la raison pour laquelle on vous liera** — les données de prix originales sont ce qui attire des liens spontanés dans cette niche ;
- **la barrière à l'entrée** : un concurrent peut copier un texte, pas un historique de relevés.

Cadence réaliste : un relevé mensuel en saison (sept.-févr.), trimestriel hors saison. Le stocker dans `data/` sous forme de tableau daté, jamais uniquement dans les pages.

## Architecture de conversion

| Type de page | Rôle | Sortie |
|---|---|---|
| Pages marques (`piron`, `hubo`, `gamma`…) | Capter le trafic de marque | → comparatif général |
| Pages prix | Capter l'intention prix | → comparatif général |
| Comparatif général (`/pellets/`) | **Page pivot centrale** | → `/devis/` |
| Pages locales (`/fournisseurs/…`) | Intention livraison, déjà mûre | → `/devis/` directement |
| `/devis/` | Le formulaire | Le lead |

Les pages locales court-circuitent le comparatif : leur visiteur cherche déjà un fournisseur, l'envoyer comparer le fait reculer d'une étape.

## Ce qu'on garde en réserve
L'affiliation n'est pas interdite à jamais, elle est **reportée**. Si un programme exploitable se confirme et que les données montrent qu'un segment de trafic ne convertit pas en lead, on pourra l'activer sur ce segment précis. Décision à reprendre sur données, pas avant.
