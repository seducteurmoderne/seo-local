# Une session de production par lots

Les nouveaux sites n'ont pas de pilote quotidien. Une session (un associé avec Claude) rédige un lot de pages et les programme d'avance ; WordPress les sort au rythme du site. On revient à chaque intervention humaine : nouveau lot, urgence, repriorisation.

Toutes les commandes se lancent depuis le dossier du site, `sites/<site>/`. Le détail de la rédaction d'une page (recherche, modèle de ville, brief, faits sourcés, photos, contrôle) est dans `autopilote/PROCEDURE.md` du site, étapes 3 à 5 : une session de lot les applique page après page.

## 1. Avant de commencer
- `git pull` à la racine du dépôt.
- `python3 tools/autopilote.py etat` : connexion WordPress, pages programmées et jusqu'à quand, formulaires actifs, prochain slug de la file. Cette commande publie aussi les pages programmées restées en retard.
- `python3 tools/autopilote.py maillage` : relie les pages en ligne à celles sorties depuis la dernière intervention (sans pilote quotidien, personne d'autre ne le fait).
- Le panel du parc (`python3 panel/panel.py` à la racine) montre la même chose pour tous les sites, plus les demandes et la Search Console.

## 2. Taille du lot
De quoi tenir **2 à 4 semaines** au rythme du site (`site.json` → `publication` : `par_jour`, `tous_les`). Au-delà, la recherche locale date déjà au moment de la sortie, et chaque changement de priorité oblige à décaler trop de pages.

## 3. Rédiger le lot, page après page
Dans l'ordre de la file : `python3 tools/autopilote.py suivant` donne la page suivante. Pour chacune :
1. **Page de ville** : `python3 tools/autopilote.py modele <slug>`, puis la recherche locale propre à la commune (sources officielles, sourcées dans les notes), juste avant de rédiger. **Guide ou page mère** : `python3 tools/autopilote.py brief <slug>`, puis la rédaction sur son plan.
2. Les photos : de 1 à 4, cherchées et choisies (charte, section « Images »).
3. `python3 tools/autopilote.py verifier <slug>` jusqu'à n'avoir aucun point bloquant.
4. `python3 tools/autopilote.py publier <slug>` : la page prend le créneau suivant, au rythme du site, à une heure au hasard.

Une page impossible à écrire proprement (commune sans aucune donnée publique) : `python3 tools/autopilote.py bloquer <slug> "raison"`, puis la suivante.

## 4. Les interventions entre deux lots
| Situation | Commande |
|---|---|
| Le propriétaire veut une page tout de suite | La rédiger, puis `publier <slug> --urgent` : elle prend le premier créneau, les autres glissent d'un jour |
| La Search Console montre des pages à pousser | `replanifier <slug> [<slug>…]` pour les pages déjà programmées ; pour celles pas encore écrites, les remonter en tête de `autopilote/file-attente.txt` |
| Voir l'ordre de sortie | `etat` |
| Une page déjà en ligne commence à ranker | La laisser tranquille : données à jour oui, texte et titres non (doctrine, `CLAUDE.md`) |

## 5. Fin de session
- Une ligne au journal (`autopilote/journal.md`) : pages programmées, jusqu'à quelle date, ce qui a été bloqué et pourquoi.
- Commit du dossier du site (articles, briefs, photos, état, journal, sitemap) puis `git push`. Jamais `setup/.env`.

## Ce qu'il faut savoir
- **Le cron de WordPress ne tourne qu'avec des visites.** Sur un site neuf, une page programmée peut sortir en retard. Chaque site par lots a besoin d'un vrai cron, chez l'hébergeur ou par un service qui appelle `https://<domaine>/wp-cron.php` toutes les heures.
- **Les liens vers une page pas encore sortie restent éteints** jusqu'au prochain `maillage` : c'est pour ça qu'il ouvre chaque intervention.
