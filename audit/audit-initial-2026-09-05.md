# Audit initial — bois-de-chauffage-et-pellets.be
**Date : 5 septembre 2026** · Sources : export GSC 16 mois (mai 2025 → sept 2026), crawl direct du site, fichier de recherche de mots-clés 2024

---

## 1. État des lieux chiffré

| Indicateur | Valeur |
|---|---|
| Impressions, 16 mois | **721** |
| Clics, 16 mois | **3** |
| CTR | 0,42 % |
| Position moyenne | 56,2 (page 6) |
| Pages générant des impressions | **1** (la homepage) |
| URLs totales dans le sitemap | **2** |
| Dernière modification du sitemap | **13 septembre 2024** |

Le site est en sommeil depuis exactement deux ans. Les 721 impressions viennent intégralement de la homepage ; l'article `/meilleur-pellet/` n'a généré **aucune impression en 16 mois**.

### Le signal positif : la position progresse toute seule
| Période | Impressions | Position moyenne |
|---|---|---|
| Saison 2025 (mai-oct) | 249 | **72,8** |
| Hiver / printemps 25-26 | 251 | **44,0** |
| Récent (mai-sept 26) | 221 | **51,1** |

Sans qu'une ligne n'ait été publiée, la position moyenne est passée de ~73 à ~44-51. C'est l'effet de l'ancienneté du domaine : Google accorde progressivement du crédit. Autrement dit, **le domaine gagne en confiance mais n'a rien à proposer**. C'est exactement la situation où l'ajout de contenu produit un effet immédiat et disproportionné.

### Répartition desktop / mobile : 634 vs 85 impressions
Contre-intuitif pour du B2C, mais logique : les SERP mobiles affichent moins de résultats par page, donc une position 56 y devient quasi invisible. **Ce déséquilibre est un symptôme du classement, pas d'un bug mobile.** Il se corrigera mécaniquement en remontant. Le viewport est correctement configuré.

---

## 2. Ce que Google associe déjà au site

> ⚠️ **Portée limitée de ces données — à lire avant d'en tirer des priorités.**
> Ces requêtes ne décrivent **pas la demande du marché**. Elles décrivent ce qu'une seule homepage générique a réussi à faire remonter, sur 721 impressions en 16 mois — soit ~45/mois.
> Le biais est un biais de sélection : **tout cluster sans page est absent par construction** (`prime pellet`, `pellet piron`, `stère de bois`, comparatif chauffage : zéro impression, faute de page et non faute de demande). À des positions 40-80, les impressions sont en outre erratiques et non proportionnelles au volume.
> **Usage valide** : confirmer que Google a compris la thématique, et que l'intention penche vers le commercial. **Usage invalide** : dimensionner une opportunité ou hiérarchiser des pages.

Les 43 requêtes en impression sont presque toutes **commerciales et belges**. Extraits :

| Requête | Impr. | Position |
|---|---|---|
| bois de chauffage belgique | 204 | 53,6 |
| vente de bois de chauffage belgique | 88 | 70,2 |
| chauffage bois | 73 | 69,2 |
| bois de chauffage | 36 | 80,9 |
| pellets en belgique | 26 | 98,7 |
| vente de bois de chauffage | 18 | 79,4 |
| livraison bois de chauffage | 13 | 62,4 |
| fournisseurs pellets belgique | 9 | 81,9 |
| bois de chauffage liège | 6 | 55,8 |
| chauffagiste pellet brabant wallon | 6 | 92,2 |
| bois de chauffage province luxembourg | 4 | 60,0 |

Deux enseignements :
1. **Le positionnement thématique est acquis.** Google sait de quoi parle le site. Le problème n'est pas la pertinence, c'est l'absence de pages.
2. **La demande locale est déjà visible** (Liège, Brabant wallon, province de Luxembourg) alors qu'aucune page locale n'existe. Ces requêtes sortent de la seule homepage.

---

## 3. Le gisement du fichier de mots-clés 2024

Le fichier `Sitemap - BOIS - Pellets.csv` contenait déjà un plan complet, avec volumes et difficulté. **Il n'a jamais été exécuté** : sur ~20 URLs prévues, 2 existent.

### Cluster marques & enseignes belges — le gisement principal
| Requête | Volume/mois | KD |
|---|---|---|
| pellet piron | 2 400 | 17 |
| pellets gamma | 1 300 | 21 |
| pellet hubo | 1 000 | 24 |
| pellet trafic | 1 000 | 17 |
| badger pellets | 880 | 11 |
| aveve pellets | 880 | 11 |
| descamps pellet | 880 | 10 |
| pellets brico | 880 | 33 |
| **Total** | **≈ 9 220** | **10-33** |

Des volumes élevés avec une difficulté très basse, sur des requêtes **100 % belges** qu'aucun site français ne couvrira jamais. C'est le meilleur rapport volume/effort de tout le projet.

### Autres requêtes chiffrées du fichier
| Requête | Volume/mois | KD |
|---|---|---|
| pellets | 6 600 | 7 |
| prime pellet | 2 400 | 19 |
| pellet prix | 1 300 | 13 |
| stère de bois | 1 300 | 20 |

Les requêtes « essences » (chêne, hêtre, frêne, bouleau, longueur de bûches) sont à 20/mois avec KD 0 : à produire, mais en remplissage, pas en priorité.

> ⚠️ Volumes datant de 2024, à recontrôler. Les ordres de grandeur et surtout la hiérarchie restent valables ; le marché du pellet a connu de fortes variations de prix depuis, ce qui a plutôt gonflé les recherches « prix » et « prime ».

---

## 4. Problèmes techniques relevés

### Bloquants
| # | Problème | Détail | Effet |
|---|---|---|---|
| 1 | **Contenu quasi inexistant** | 2 URLs | Cause racine de tout le reste |
| 2 | **`Crawl-delay: 10` dans robots.txt** | Demande 10 s entre chaque requête | Ignoré par Google, mais **respecté par Bing** et les autres. Freine l'exploration pour rien |
| 3 | **Aucune directive `Sitemap:` dans robots.txt** | Absente | Découverte du sitemap ralentie |
| 4 | **TTFB 1,0 à 1,4 s** | Mesuré 3× | Lent. Aucun plugin de cache détecté. Cible : < 0,5 s |

### Importants
| # | Problème | Détail |
|---|---|---|
| 5 | **Double `<meta name="description">`** sur `/meilleur-pellet/` | Deux balises concurrentes (Yoast + une autre source). Google en choisit une au hasard |
| 6 | **Faute dans le `<title>` de l'article** | « 9 **caractéritiques** » → caractéristiques. Visible dans les résultats de recherche |
| 7 | **Incohérence interne de l'article** | Annonce « les 9 caractéristiques » puis « les 10 caractéristiques » deux paragraphes plus loin |
| 8 | **Schema.org minimal** | Uniquement les types par défaut de Yoast (Organization, WebSite, WebPage, BreadcrumbList). Ni LocalBusiness, ni Service, ni FAQPage, ni Product |
| 9 | **Images non optimisées** | 3 images, toutes en JPG/PNG, **aucune en WebP, aucun `loading="lazy"`**. Peu grave aujourd'hui, bloquant dès qu'on ajoutera des photos |
| 10 | **`og:locale` = `fr_FR`** | Devrait être `fr_BE` pour un site ciblant la Belgique. Correction gratuite |

### Points sains
- HTTPS actif avec HSTS
- Un seul `<h1>` par page, hiérarchie de titres correcte
- Canonicals propres
- Aucune balise `noindex` parasite
- Attributs `alt` présents sur toutes les images
- Viewport mobile correct
- Thème **Hello Elementor** : base légère, bon choix. Elementor Pro alourdit un peu, mais rien de rédhibitoire — pas de refonte nécessaire

### À vérifier de ton côté (nécessite l'accès GSC)
- **`/meilleur-pellet/` est-il réellement indexé ?** 1 672 mots sans une seule impression en 16 mois, c'est anormal même pour une requête concurrentielle. À passer dans l'outil d'inspection d'URL de la Search Console.

---

## 5. Écart de positionnement à trancher

La homepage se présente comme un **annuaire / comparateur** :
> « Nous référençons tous les fournisseurs en Belgique francophone »
> « Le site numéro 1 en Belgique dans le conseil de fournisseurs »

Or le modèle annoncé est la **génération de demandes de devis**. Les deux sont compatibles — un comparateur qui capte des demandes et les route vers des fournisseurs, c'est un modèle solide — mais l'architecture des pages locales change du tout au tout selon la réponse. Voir la question posée en fin d'analyse.

Deux formulations à corriger dans tous les cas :
- **« Le site numéro 1 en Belgique »** : superlatif invérifiable, et en Belgique la publicité comparative non étayée est encadrée par le Code de droit économique. À remplacer par une promesse factuelle.
- **« Livraison gratuite, meilleurs prix »** en meta description : intenable si le site ne livre pas lui-même. Promesse au nom de tiers.

---

## 6. Conclusion

Le site n'a aucun problème de fond. Il a un domaine de 2 ans, une thématique correctement comprise par Google, une position qui s'améliore passivement, une demande locale déjà visible en impressions — et **2 pages**.

Le facteur limitant est unique et c'est le volume de contenu. Les correctifs techniques listés ci-dessus se règlent en une demi-journée ; ils sont nécessaires mais ne produiront rien seuls. Le levier réel, c'est l'exécution du plan éditorial qui existait déjà en 2024 et qui n'a jamais été mis en œuvre.
