# Performances — ce qui vaut le coup, et quand

**Départ mesuré** : 72 mobile / 82 ordinateur · TTFB 1,0 à 1,4 s (3 mesures) · aucun plugin de cache détecté

---

## La cible réaliste

| | Aujourd'hui | Atteignable | Coût |
|---|---|---|---|
| Mobile | 72 | **90-95** | ~2 h |
| Ordinateur | 82 | **95-100** | inclus |
| 100 mobile | — | seulement sans Elementor | refonte des gabarits |

Elementor Pro charge son bundle sur chaque page. C'est le plancher, et il ne se franchit pas par réglage. Hello Elementor comme thème de base est en revanche un bon choix — le problème n'est pas le thème.

## Ce qui rapporte, par ordre d'impact

### 1. Le cache — de très loin le plus gros gain
TTFB à 1,2 s sans aucun cache, c'est le principal frein. Un cache de pages bien réglé le ramène autour de 0,2-0,4 s.

- **LiteSpeed Cache** si l'hébergeur tourne sous LiteSpeed — gratuit et le meilleur dans ce cas
- **WP Rocket** sinon
- Activer : cache de pages, minification CSS/JS, préchargement, `font-display: swap`

*Vérifier d'abord si l'hébergeur est en LiteSpeed : l'en-tête HTTP du site indique `server: Apache`, donc probablement pas — WP Rocket est le pari sûr.*

### 2. Les images
Trois images seulement aujourd'hui, toutes en JPG/PNG, **aucune en WebP, aucun lazy loading**. Marginal maintenant, bloquant dès qu'on ajoutera des photos de livraison sur 86 pages locales.

- Conversion WebP automatique (incluse dans les deux plugins de cache)
- Lazy loading partout **sauf** l'image d'en-tête — la charger en priorité, c'est elle qui porte le LCP
- `width` et `height` explicites → supprime le CLS

### 3. Elementor lui-même
Dans `Elementor → Réglages → Fonctionnalités`, plusieurs options réduisent le poids et sont souvent désactivées par défaut : DOM optimisé, chargement amélioré des ressources, chargement conditionnel des widgets, hébergement local des polices Google.

### 4. Le ménage
Chaque plugin inutile est du poids mort. Sur un site de 3 pages, il ne devrait pas y en avoir plus de huit.

---

## Quel accès pour que je le fasse

| Accès | Ce que je peux faire |
|---|---|
| **Éditeur** (prévu) | **Rien** côté performances |
| Administrateur via API REST | Installer des plugins, partiellement. Les réglages des plugins de cache ne passent pas par l'API — donc peu utile |
| **SSH / WP-CLI** | **Tout** : plugins, options, images, `.htaccess`, mesures avant/après |

**En pratique** : cocher les réglages d'un plugin de cache va plus vite à la main qu'en pilotant l'API. La checklist ci-dessus te prend une heure. Je ne demande un accès SSH que si tu veux que je gère aussi les optimisations serveur — et seulement si ton hébergeur le permet.

---

## Le verdict de priorité

Ton goulot d'étranglement n'est pas la vitesse, c'est que **le site a deux pages**. Aller chercher 72 → 100 pendant qu'il reste 154 pages à écrire, c'est optimiser la mauvaise variable — et le score de labo n'a de toute façon aucun effet tant qu'il n'y a pas de données terrain.

**Ce qui se justifie maintenant** : le cache et le WebP, points 1 et 2, une heure de travail. Non pas pour le score, mais parce que **1,2 s de TTFB coûte des leads** — un formulaire lent est un formulaire abandonné. Ça, c'est du chiffre d'affaires, pas du référencement.

**Ce qui attend mars-août** : le reste. Hors saison, quand la production de contenu ralentit, une refonte des gabarits pour viser réellement 95+ devient un projet légitime. Et à ce moment-là tu auras du trafic, donc de vraies données CrUX à optimiser plutôt qu'un score de laboratoire.
