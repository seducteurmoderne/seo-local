# Moteur commun des sites de contenu

Un seul moteur, un dossier par site, une tâche planifiée par site.

```
SEO LOCAL/               dépôt GitHub partagé
├── CLAUDE.md            instructions communes (chargées pour tous les sites)
├── moteur/              outils communs : wp.py, autopilote.py, images.py, config.py, design.py, prix.py (prix relus chaque jour)
├── modele-site/         squelette copié pour chaque nouveau site
├── designs/             directions de design en HTML, réutilisables d'un site à l'autre
├── charte-base.md       charte de rédaction de départ
├── tache-planifiee.md   texte de la tâche planifiée à dupliquer
├── nouveau_site.py      crée un dossier de site dans sites/ depuis le modèle
├── panel/               panel de suivi du parc (stats par site, demandes de devis)
├── archives/            anciennes versions des outils (hors du dépôt)
└── sites/
    └── <site>/          un dossier par site
```

Chaque site pointe vers le moteur par `site.json` → `"moteur": "../../moteur"`.

Un associé peut garder des sites hors du dépôt partagé, dans `sites/` sur sa machine : chacun a alors son propre dépôt Git local, exclu par `.git/info/exclude` (jamais par `.gitignore`), et il les décrit dans son `CLAUDE.local.md`, jamais commité.

## Démarrer sur une nouvelle machine
```bash
git clone git@github.com:<compte>/seo-local.git "SEO LOCAL"
```
Python 3 suffit pour le moteur. Pour chaque site sur lequel tu travailles, crée son `setup/.env` à partir de `setup/.env.exemple`, avec tes propres identifiants WordPress : il n'est jamais commité.

## Ce qui vit où
| Commun (`moteur/`) | Propre à chaque site |
|---|---|
| Client WordPress, rendu Markdown → Gutenberg | `site.json` : verticales, formulaire, couleurs, fuseau, rythme de publication |
| Contrôle qualité (`verifier`), publication programmée, maillage, audit | `setup/.env` : identifiants WordPress |
| Images à la une générées, préparation des photos | Stratégie, sitemap, file d'attente, journal, état |
| Formulaire de devis et son plugin de réception (généré depuis `site.json`) | Charte, articles, visuels, photos, données terrain |

Chaque site garde `tools/autopilote.py` et `tools/images.py` : ce sont des **lanceurs** identiques (`moteur/lanceur.py`) qui exécutent le moteur sur ce site. Les commandes restent donc les mêmes partout : `python3 tools/autopilote.py etat`, `verifier`, `publier`…

## Panel du parc
```bash
python3 panel/panel.py
```
puis ouvrir http://127.0.0.1:8765. Deux pages :
- **Stats** : une ligne par site et le total du parc. Pages en ligne, programmées (et jusqu'à quand), restant en file ; clics, impressions, position, pages qui rankent et à renforcer (dernier relevé `gsc`) ; demandes sur 28 jours et depuis le début, demandes pour 100 clics ; alertes (connexion refusée, formulaires masqués, rien de programmé, plugin à mettre à jour).
- **Demandes** : toutes les demandes du parc, avec leur site, leur page d'origine, leurs besoins, code postal et délai, par période et par site, avec le total par mois et un export CSV.

Lecture seule, sur la machine seulement (127.0.0.1) : le panel ne modifie rien. Il montre les sites de `sites/` dont la machine a le `setup/.env`. Les demandes n'y portent ni nom, ni e-mail, ni téléphone : le détail reste dans l'admin WordPress de chaque site.

Pour compter les demandes, le plugin de devis doit être en **version 2** (route `/suivi`, réservée aux comptes connectés) : `python3 tools/autopilote.py plugin` le régénère dans `setup/mu-plugins/leads.php`, à redéposer dans `wp-content/mu-plugins/` à la place de l'ancien (même nom de fichier, jamais deux copies).

## Créer un site
Depuis la racine du dépôt :
```bash
python3 nouveau_site.py nom-du-site domaine.be
```
Puis suivre `sites/<nom-du-site>/setup/DEMARRAGE.md`, et créer la tâche planifiée à partir de `tache-planifiee.md` en dernier.

## Programmer d'avance et réadapter
`publier <slug>` programme chaque article au créneau suivant, à une heure au hasard, au rythme du site (`site.json` → `publication`, un article par jour par défaut) : un lot rédigé en une session sort donc tout seul à ce rythme.

| Besoin | Commande |
|---|---|
| Faire passer un article prêt avant tous les autres | `python3 tools/autopilote.py publier <slug> --urgent` |
| Remonter des articles déjà programmés (Search Console…) | `python3 tools/autopilote.py replanifier <slug> [<slug>…]` |
| Voir l'ordre de sortie | `python3 tools/autopilote.py etat` |

Les créneaux ne changent pas : les articles cités prennent les premiers, les autres glissent d'un jour, et chaque article déplacé est renvoyé avec sa nouvelle date dans le cadre auteur. Un article retouché à la main dans WordPress garde sa date.

Sans pilote quotidien, personne ne rattrape une sortie manquée : le cron WordPress ne tourne qu'avec des visites. Chaque site par lots a besoin d'un vrai cron (chez l'hébergeur, ou un service qui appelle `/wp-cron.php` toutes les heures).

## Modifier le moteur
Une modification du moteur touche **tous les sites** dès leur prochaine exécution. Avant de la garder :
1. rendre tous les articles de chaque site avant et après, et comparer (le rendu d'un article inchangé doit rester identique) ;
2. lancer `python3 tools/autopilote.py verifier <slug>` sur un article de chaque site.

Les tâches planifiées ne modifient jamais le moteur : seules les sessions de travail avec le propriétaire le font.

## Réglages de `site.json`
| Clé | Rôle |
|---|---|
| `moteur` | Chemin du moteur, relatif au dossier du site |
| `verticales` | Pour chaque verticale : `categorie` WordPress, `besoin` coché par défaut, slug de la page `mere`, valeur `sitemap` de la colonne `verticale`, `motif` de l'image à la une |
| `categorie_locale` | Pages de ville et leur `motif` d'image : repérées par `cluster` (ex. `"Ville"`, la page garde la catégorie de sa verticale) ou, à défaut, par une `categorie` dédiée |
| `formulaire` | Adresse de réception (`endpoint`), page de confidentialité, besoins et leurs champs, délais, format du code postal, textes. `"mode": "simple"` : formulaire court (prénom, nom, e-mail, téléphone, message facultatif), besoin déduit du `besoin` de la page, sans code postal ni délai ; titre écrit dans l'article (`::cta-fort Un élagage à faire ? …`), sous-titre `sous_titre`, texte d'aide `placeholder_message`. Le plugin généré (`autopilote.py plugin`) suit le mode |
| `couleurs`, `habillage_css` | Couleurs du formulaire, style ajouté au contenu pour le thème du site |
| `publication` | Rythme du site : `par_jour` articles chaque jour de sortie (défaut 1), un jour de sortie tous les `tous_les` jours (défaut 1), entre `heure_debut` et `heure_fin` (défaut 7 h et 22 h), jamais avant maintenant + `delai_min_heures` (défaut 2). Ex. `"par_jour": 2` : deux articles par jour ; `"tous_les": 2` : un article tous les deux jours |
| `seo` | Seuils du contrôle qualité (`moteur/seo.py`, `SEUILS`). `"brief_locales_facultatif": true` : les pages locales n'exigent plus l'analyse des 10 résultats ni le brief (avertissement seulement) ; tout le reste, dont le refus au-delà de 50 % de texte commun entre pages locales, s'applique |
| `audit_exclus`, `formules_bannies_en_plus` | Pages ignorées par l'audit, formules interdites propres au site |
| `design` | `2` active le design v2 (`moteur/design.py`) : fil d'Ariane, cadre auteur et dates, En bref stylé, sommaire, chiffres clés, encadrés, FAQ en accordéon, encadré auteur. Absent : rendu d'origine |
| `theme` | Thème en blocs officiel habillé par l'API (`moteur/theme.py`, commande `autopilote.py theme [pousser\|retirer]`) : `slug` du thème, `polices` (nom, slug, pile, fichier, graisse). Sources dans `<site>/theme/`. Avec `design: 2`, les articles ne portent plus de CSS : le thème le fournit. Tant que le thème n'est pas actif, l'envoi se fait en aperçu |
| `auteur` | `nom`, `role`, `bio`, `photo` (URL), `page` : cadre et encadré auteur du design v2. Jamais d'auteur fictif |
| `polices` | `titres`, `texte` : polices déjà chargées par le thème |

Motifs d'image à la une : `bois`, `pellets`, `ramonage`, `local`, `formes` (neutre, aux couleurs du site). Un site peut en ajouter dans `tools/motifs.py` (dict `MOTIFS`).
