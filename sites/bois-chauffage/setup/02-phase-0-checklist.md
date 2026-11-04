# Phase 0 — à faire par toi (≈ 1 h)

Tâches d'administration qui demandent le rôle Administrateur. **Rien ne doit être publié avant que le point 3 soit fait** : sans menu, chaque page produite serait orpheline et non indexée, exactement comme `/meilleur-pellet/` depuis deux ans.

## Structure
- [ ] **1.** `Réglages → Permaliens` → **Titre de la publication** (`/%postname%/`)
- [ ] **2.** Créer les catégories : `Bois de chauffage`, `Pellets`, `Ramonage`, `Poêlier`, `Local`
- [ ] **3.** `Apparence → Menus` → **créer le menu principal** : Bois de chauffage · Pellets · Ramonage · Poêlier · Devis
- [ ] **4.** Lier `/meilleur-pellet/` depuis la homepage *(sort la page de son orphelinat)*

## Technique
- [ ] **5.** `robots.txt` : supprimer `Crawl-delay: 10`, ajouter `Sitemap: https://bois-de-chauffage-et-pellets.be/sitemap_index.xml`
- [ ] **6.** Installer un cache — **LiteSpeed Cache** si l'hébergeur tourne sous LiteSpeed (gratuit, excellent), sinon WP Rocket. *TTFB mesuré à 1,0-1,4 s, cible < 0,5 s*
- [ ] **7.** Activer la conversion **WebP** et le lazy loading dans le plugin de cache

## Correctifs de contenu
- [ ] **8.** Corriger le title de `/meilleur-pellet/` : « caractéri**ti**ques » → « caractéri**sti**ques »
- [ ] **9.** Supprimer la `<meta description>` en double sur ce même article *(deux balises concurrentes)*
- [ ] **10.** Retirer de la homepage « Le site numéro 1 en Belgique » et « livraison gratuite » — superlatif invérifiable et promesse au nom de tiers, tous deux encadrés par le livre VI du Code de droit économique
- [ ] **11.** `og:locale` → `fr_BE`

## Search Console
- [ ] **12.** Inspection d'URL sur `/meilleur-pellet/` → **Demander l'indexation** *(après le point 4)*
- [ ] **13.** Vérifier que le sitemap est bien soumis

## Accès
- [ ] **14.** Créer l'utilisateur `claude` (Éditeur) + mot de passe d'application → voir `01-acces-wordpress.md`
- [ ] **15.** Déposer le fichier `mu-plugins/expose-yoast-rest.php`
