# Projet : elagage-luxembourg.com

Site WordPress de génération de leads sur l'élagage, l'abattage, le dessouchage, le haubanage et la plantation d'arbres. Nom affiché : **Devis Élagage Lux** (jamais « Élagage Luxembourg », nom d'une entreprise existante, elagage-luxembourg.lu). Les demandes sont transmises à un élagueur partenaire (Histoires d'Arbres, Beckerich). Mentions légales et confidentialité au nom d'**Indexio EOOD**.

**Zone** : Grand-Duché de Luxembourg et province de Luxembourg (Belgique), en partant de Beckerich. **Langue** : français seul. **Logo et favicon** (propriétaire, 20/10/2026) : `media/marque/` (logo « Elagage Luxembourg » dans l'en-tête via `theme/parts/header.html`, favicon = icône du site WordPress) ; le nom WordPress reste « Devis Élagage Lux ». **Schema.org** (20/10/2026) : Organization « Elagage Luxembourg » dans `theme/parts/footer.html` ; Service généré par le moteur sur chaque page avec `besoin` (`site.json` → `schema_service`). **Design** : direction A (`../../designs/a-editorial.html`). Stratégie : `strategie/00-strategie-globale.md` (sections 9 et 10 pour les décisions les plus récentes).

## Où est quoi
| Chemin | Rôle |
|---|---|
| `site.json` | Réglages du site pour le moteur : verticales, formulaire, couleurs, publication |
| `strategie/sitemap-urls.csv` | Les URLs prévues et leur `statut` — tableau de bord |
| `articles/00-charte-redactionnelle.md` | **Charte de rédaction — fait foi** |
| `articles/*.md` | Sources des articles ; WordPress n'en reçoit que le rendu |
| `visuels/`, `photos/`, `media/` | Schémas SVG, photos du propriétaire, images prêtes à envoyer |
| `tools/` | Lanceurs du moteur commun (`../../moteur/`) — ne pas modifier |
| `autopilote/` | Procédure, file d'attente, journal et état du pilote |
| `setup/.env` | Identifiants WordPress — **ne jamais afficher ni copier** |

## Règles du site
- URLs de premier niveau ; le silo passe par les catégories WordPress (une par verticale de `site.json`) et les liens internes.
- Accès WordPress : utilisateur `claude`, rôle **Administrateur** (choix du propriétaire, 16/10/2026). En session avec le propriétaire : réglages, extensions, thème possibles sur sa demande ; suppressions toujours confirmées. Le **pilote automatique** n'y touche jamais.
- Une page peut exister sans volume de recherche, **jamais sans contenu propre**. Une page de ville repose sur des données publiques propres à sa commune (villages, relief, arbres, parc à conteneurs, communes voisines), trouvées et sourcées pendant l'exécution ; aucune entreprise citée.
- Ne jamais modifier un contenu WordPress qui n'est pas produit depuis `articles/`.

## Style attendu par le propriétaire
Phrases simples qui expliquent, sans formule d'élan. La réponse avant le premier scroll : l'encadré « En bref » est un paragraphe de 2-3 phrases qui répond au mot-clé principal, jamais une liste de 4 puces (demande du propriétaire, 16/10/2026). Une liste à puces par article, deux au maximum. Toujours un paragraphe entre un H2 et un H3. Détail dans la charte.

Article modèle : `articles/elagage.md` (page service validée par le propriétaire le 16/10/2026). Pages de ville : modèles `articles/_modeles/locale-*.md` (commande `modele <slug>`).

## Pilote automatique
Tâche planifiée `pilote-elagage-luxembourg` : chaque jour un article de la file (`autopilote/file-attente.txt`) est rédigé, vérifié puis programmé. Procédure : `autopilote/PROCEDURE.md`. Journal : `autopilote/journal.md`.

## En attente du propriétaire
Voir `setup/DEMARRAGE.md`.
