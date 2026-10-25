# Projet : bois-de-chauffage-et-pellets.be

Site WordPress de génération de leads sur le chauffage au bois en Wallonie. Le propriétaire est un **intermédiaire** : il collecte des demandes de devis et les transmet à des partenaires (fournisseurs de bois et de pellets, ramoneurs, poêliers). Pas d'affiliation.

## Où est quoi
| Chemin | Rôle |
|---|---|
| `strategie/00-strategie-globale.md` | Stratégie consolidée |
| `strategie/sitemap-urls.csv` | Les 156 URLs et leur `statut` — tableau de bord |
| `strategie/09-criteres-de-decision.md` | Ce qui décide qu'une page existe (le volume Semrush vient en dernier) |
| `articles/00-charte-redactionnelle.md` | **Charte de rédaction — fait foi** |
| `articles/*.md` | Sources des articles ; WordPress n'en reçoit que le rendu |
| `visuels/` | Schémas SVG |
| `photos/` | Photos sources du propriétaire (déposées telles quelles) |
| `media/` | Images prêtes à envoyer : `une/` (images à la une générées), `photos/` (WebP préparés) |
| `site.json` | Réglages du site pour le moteur commun : verticales, formulaire, couleurs, publication, thème |
| `theme/` | Habillage du thème (design C) : styles, CSS, en-tête, pied de page, gabarits, polices. Envoyé par `python3 tools/autopilote.py theme pousser` |
| `tools/autopilote.py`, `tools/images.py` | **Lanceurs** du moteur commun `../../moteur/` (état, vérification, publication, maillage, images). Le moteur sert tous les sites : voir `../../README.md` avant d'y toucher |
| `autopilote/` | Procédure, file d'attente, journal et état du pilote |
| `setup/.env` | Identifiants WordPress — **ne jamais afficher ni copier** |

## Règles du site
- **URLs toutes de premier niveau.** Le silo passe par les catégories WordPress et les liens internes : Bois de chauffage, Pellets, Ramonage et, depuis le 24/10/2026 (décision du propriétaire), **Poêle à pellets** et **Poêle à bois** (pages mères `/poele-a-pellets/`, `/poele-a-bois/`, leads de pose, d'entretien et de dépannage, `besoin: poelier`), plus **Fournisseurs** (fiches de sociétés à l'URL de premier niveau, hub `/fournisseurs/`). Toujours pas de catégorie par métier (pas de « Poêlier ») ni de catégorie Entretien : l'entretien est un cluster dans chaque verticale poêle, relié au ramonage par les liens. Le besoin réel du visiteur est capté par le champ `besoin` du formulaire, indépendant de la catégorie.
- Pages poêle : le terme générique (« poêle à pellets ») est tenu par les boutiques sur google.be ; on vise les pages de ville (`poele-a-pellets-<ville>`, `poele-a-bois-<ville>`, modèles dans `articles/_modeles/`, poêleries vérifiées sur leur site) et les guides prix, installation, prime, modèles. Les modèles de poêles se présentent sur la fiche du fabricant, sans affiliation pour l'instant.
- Fiches fournisseurs : modèle `articles/_modeles/fiche-fournisseur.md`. Faits tirés du site de la société et datés, encadré « Page indépendante », ni logo, ni avis, ni dénigrement, rien qui laisse croire à un partenariat (Code de droit économique, livre VI). Une société qui demande le retrait de sa fiche : le propriétaire décide.
- Pages locales : la catégorie de leur verticale (`pellets-<ville>` → Pellets), pour que le fil d'Ariane Yoast affiche Accueil » Pellets » … (demande du propriétaire, 04/10/2026). Elles se repèrent par `cluster: Ville` (image à la une « local »). La catégorie WordPress `Local` est vide depuis : la supprimer ou non reste au propriétaire.
- Guides = articles catégorisés. Pages mères, `/devis/`, `/a-propos/`, `/partenaires/` = pages.
- Accès WordPress : utilisateur `claude`, rôle **Administrateur** depuis le 04/10/2026 (décision du propriétaire, qui veut que Claude fasse lui-même ce qu'il peut). En session avec le propriétaire : plugins, réglages, menu, médias possibles sur sa demande ; suppressions toujours confirmées. Le **pilote automatique garde ses interdits** (ni réglage, ni catégorie, ni contenu hors `articles/`).
- Une page peut exister sans volume de recherche, **jamais sans contenu propre**. Une page locale repose sur des données propres à sa ville : données terrain du propriétaire, magasins de bricolage/jardin proches (ils vendent presque toujours des pellets), fournisseurs qui nomment la ville sur leur site. Depuis le 04/10/2026, toutes les pages de ville partent d'un **modèle commun** (`articles/_modeles/`, commande `modele <slug>`) : même structure, mêmes titres au nom de la ville, fournisseurs en tableau court. Ce qui reste interdit, c'est le texte identique d'une ville à l'autre (« doorway pages ») : le contrôle refuse une page dont plus de 50 % du texte se retrouve dans une autre page locale. Une offre maigre ne bloque pas la page : elle devient l'argument du formulaire (« nous trouvons un fournisseur qui livre chez vous »).
- Thème : **Twenty Twenty-Five** habillé par l'API (design C, `theme/`), depuis le 04/10/2026. Elementor et Elementor Pro sont désactivés. L'accueil est la page `accueil` (articles/accueil.md, `entete: accueil` : bandeau photo, chapô, formulaire, prix Valbiom, villes, guides), réglée comme page d'accueil le 16/10/2026 ; l'ancienne homepage Elementor (`home-perso`, id 28906) est gardée de côté. Ajouter chaque nouvelle ville publiée à la section « dans votre ville » de l'accueil.
- Ne jamais modifier un contenu WordPress qui n'est pas produit depuis `articles/`. Les contenus « repris à la main » (ramonage, ramonage-arlon, bois-a-ne-pas-bruler, temps-sechage-bois) et `/meilleur-pellet/` gardent leur texte, affiché avec le gabarit `avec-titre`.

## Style attendu par le propriétaire
Phrases simples qui expliquent, sans formule d'élan. La réponse avant le premier scroll : l'encadré « En bref » est un paragraphe de 2-3 phrases qui répond au mot-clé principal, jamais une liste de puces (demande du propriétaire, 16/10/2026). Une liste à puces par article, deux au maximum. Toujours un paragraphe entre un H2 et un H3. Détail et exemples dans la charte.

## Pilote automatique
Tâche planifiée `pilote-bois-chauffage` : chaque jour un article est rédigé, vérifié puis programmé à une heure aléatoire. Procédure : `autopilote/PROCEDURE.md`. Journal : `autopilote/journal.md`.

## En attente du propriétaire
- Phase 0 (`setup/02-phase-0-checklist.md`) : le menu est fait (confirmé le 26/09/2026), reste le reste de la checklist.
- Formulaires de devis **actifs** depuis le 04/10/2026 (plugin `bcp-leads` + politique de confidentialité au nom d'Indexio EOOD, contact@bois-de-chauffage-et-pellets.be). Plugin 1.1 : réception sur contact@bois-de-chauffage-et-pellets.be. Les demandes arrivent dans l'admin du plugin, ça suffit au propriétaire (16/10/2026) : plus de test d'envoi à demander.
- Les données terrain des zones pilotes (`setup/03-donnees-locales-a-collecter.csv`) avant toute page locale.
- Les 3 catégories `Guides` (créées hors du plan) sont vides depuis le 04/10/2026 (articles rendus à leur verticale, fil d'Ariane Google cohérent) : les supprimer ou non reste au propriétaire. L'auteur WordPress des articles s'affiche « La rédaction ».
- Valider la promesse « réponse sous 48 h » des CTA avec les partenaires.
- Page catalogue de poêles à pellets : en attente du choix des programmes d'affiliation.
- Mots-clés de la Search Console à recevoir : ils alimentent la sitemap, notamment les fiches fournisseurs (aucune n'est encore dans la file).
