# Checklist technique WordPress

> À exécuter dès l'accès au site. Ordre = impact décroissant.

## A. Fondations (avant toute publication)

- [ ] **Plugin SEO** — Rank Math de préférence à Yoast ici : le balisage LocalBusiness, les FAQ et les schémas personnalisés sont dans la version gratuite, ce qui compte pour un site local. Ne jamais faire tourner deux plugins SEO en parallèle.
- [ ] **Search Console** — propriété domaine vérifiée, sitemap soumis, export des 16 mois de données
- [ ] **GA4** installé, avec un événement de conversion sur l'envoi du formulaire de devis
- [ ] **Google Business Profile** — pour du lead-gen local, c'est souvent la première source d'appels, devant le site. Fiche complète, zone de service définie (pas une adresse si livraison), photos réelles, avis clients sollicités systématiquement
- [ ] **Indexation** : `site:ledomaine.be` pour vérifier ce que Google connaît déjà ; vérifier que rien n'est en `noindex` par accident (Réglages > Lecture)
- [ ] **HTTPS** partout, redirection 301 des variantes (www/non-www, http/https) vers une seule version canonique
- [ ] **Permaliens** en `/%postname%/` — jamais la structure par date

## B. Performance (Core Web Vitals)

Site de bois de chauffage = beaucoup de photos lourdes. C'est presque toujours là qu'est le problème.

- [ ] Cache : LiteSpeed Cache si l'hébergeur est en LiteSpeed (gratuit, excellent), sinon WP Rocket
- [ ] Images en **WebP**, redimensionnées avant upload (jamais de 4000 px affiché en 800)
- [ ] Lazy loading actif, **sauf** sur l'image principale au-dessus de la ligne de flottaison (sinon le LCP se dégrade)
- [ ] Dimensions `width`/`height` explicites sur toutes les images → évite le CLS
- [ ] Audit des plugins : chaque plugin inutile est du poids mort. Sur un site de 3 pages, il ne devrait pas y en avoir plus de 8-10
- [ ] Vérifier le thème : un thème multi-usage type Divi/Avada sur un petit site local est un handicap de vitesse durable. Si le site est déjà dessus, ne pas migrer en pleine saison — le noter pour le printemps
- [ ] Cible : LCP < 2,5 s sur mobile en 4G

## C. Balisage structuré (schema)

- [ ] **LocalBusiness** sur la homepage, avec `areaServed` listant les provinces/communes couvertes. Si pas de magasin physique, utiliser `serviceArea` et ne pas afficher d'adresse trompeuse
- [ ] **Service** ou **Product** sur les pages `/bois-de-chauffage/` et `/pellets/`, avec `offers` et fourchette de prix si affichée
- [ ] **FAQPage** sur les pages villes et les guides qui ont une vraie FAQ
- [ ] **BreadcrumbList** sur tout le site
- [ ] Avis clients → `AggregateRating`, **uniquement si les avis sont réels et vérifiables**. Le faux balisage d'avis est une des rares choses que Google sanctionne manuellement et rapidement
- [ ] Validation via le test des résultats enrichis de Google après chaque déploiement

## D. On-page, règles par défaut

- [ ] Un seul `<h1>` par page, contenant le mot-clé principal
- [ ] Title ≤ 60 caractères, avec la ville ou "Wallonie"/"Belgique" sur les pages locales et prix
- [ ] Meta description écrite à la main sur les pages stratégiques — c'est un argument commercial, pas un résumé
- [ ] URLs courtes, sans mots vides, jamais modifiées après indexation (sinon 301)
- [ ] Attributs `alt` descriptifs et honnêtes sur les photos
- [ ] Aucune page sans lien interne entrant (page orpheline)

## E. Pièges spécifiques à ce projet

- [ ] **Doorway pages** : le risque n°1. Des pages villes générées par template avec juste le nom qui change = sanction. Voir la règle des 600 mots uniques dans `01-architecture-site.md`
- [ ] **Cannibalisation** : `/prix/bois-de-chauffage/` et `/bois-de-chauffage/` ne doivent pas cibler la même requête. Un mot-clé principal = une page, et on tient un tableau de correspondance
- [ ] **Contenu mince** : sur un site de 3 pages, ajouter 20 pages faibles fait plus de mal que de bien. Chaque page doit pouvoir se défendre seule
- [ ] **Prix affichés** : si des prix sont publiés, ils doivent être maintenus. Un prix périmé sur une page "prix 2026" détruit la confiance et le taux de conversion
- [ ] **Formulaire de devis** : conformité RGPD (finalité, base légale, durée de conservation), et le tester réellement — un formulaire cassé pendant le pic de saison est le pire scénario possible

## F. À faire hors saison (mars-août)
- [ ] Refonte du thème si nécessaire
- [ ] Netlinking : annuaires belges qualitatifs, presse locale, partenariats (ramoneurs, poêliers, pépiniéristes)
- [ ] Nettoyage / consolidation des pages qui n'ont rien donné
