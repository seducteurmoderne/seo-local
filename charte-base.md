<!-- CHARTE DE BASE du moteur commun. Les exemples viennent du premier site (bois de chauffage) :
     remplacez-les par des exemples de la niche au fil des corrections du propriétaire. -->

# Charte rédactionnelle
**6 sept. 2026**

## Le principe : la réponse d'abord

En 2026 une page doit répondre **avant le premier scroll**. Deux raisons qui se cumulent :

- Les **AI Overviews et les moteurs conversationnels** citent les pages qui répondent directement. Une page qui fait deux paragraphes de mise en bouche avant d'arriver au fait n'est pas citée — elle n'est même pas lue.
- Le lecteur qui ne trouve pas sa réponse en dix secondes repart, et ce retour au SERP est un signal négatif.

D'où le bloc **« En bref »** en tête, dès que la requête appelle une réponse factuelle.

## Structure type

```
Fil d'Ariane — Accueil › page mère › titre court     ← généré
H1 — la requête, formulée naturellement
Cadre auteur — nom, rôle, publié le, mis à jour le    ← généré (site.json → auteur)
┌─────────────────────────────────────┐
│ EN BREF                             │  ← la réponse, 3 à 5 puces
│ ✓ réponse directe                   │     chiffrée quand c'est possible
│ ✓ le chiffre clé                    │
│ ✓ l'exception à connaître           │
└─────────────────────────────────────┘
Intro — 2-3 phrases. Ce que la page couvre, pour qui.
[CTA discret en ligne]
Sommaire                                 ← généré dès 4 H2
H2 — sur une recherche réelle (voir « Les H2 »)
  H3 — sous-points
  [::chiffres] [> 💡 astuce] [> ⚠️ alerte] [tableau]
H2 — …
H2 — FAQ, seulement si elle se justifie (voir « La FAQ »)
[CTA fort]
Sources
Encadré auteur                            ← généré
```

## Les H2 : écrits sur les recherches, pas sur le plan

Une H2 est lue par Google comme le sujet de sa section. « Livraison à Bastogne : ce qu'il faut prévoir » décrit le plan de la page ; « Livraison de bois de chauffage à Bastogne : délais, accès et frais » reprend ce que les gens tapent. La seconde se positionne, la première non.

- **Deux H2 au moins reprennent la requête cible** ou une variante proche (contrôle : aucune H2 sur la requête = publication refusée ; une seule = avertissement)
- Les autres H2 reprennent les **recherches associées** trouvées pendant la rédaction : suggestions et « Autres questions posées » des résultats, titres des pages concurrentes. Elles se notent dans le front-matter, `mots_cles_secondaires:`
- Une H2 reste une phrase naturelle, pas une liste de mots-clés : « Prix du stère de bois à Bastogne » oui, « Bois chauffage Bastogne prix stère pas cher » non
- La forme question (« Combien coûte un stère de bois à Bastogne ? ») marche bien quand c'est la question que se pose l'acheteur

## Le plan d'une page mère

Une page mère ne résume pas ses guides : elle répond elle-même, avec des chiffres, avant d'y renvoyer. Les sections vont dans cet ordre, parce qu'il suit les questions que le visiteur se pose :

| Section | Ce qu'elle doit contenir |
|---|---|
| **Ce que c'est** | La définition concrète du produit, avec ses caractéristiques normées (diamètre, taux, seuil) |
| **Ce que ça coûte** | Le prix relevé le plus récent, daté et sourcé, ramené au kWh ou à l'unité d'achat, plus ce qui le fait varier |
| **Qui l'utilise** | Une statistique d'usage sourcée, et ce qu'elle implique pour l'acheteur (filière, approvisionnement) |
| **Les différences** | Le tableau comparatif des qualités ou des types, valeurs normatives à l'appui |
| **Comment choisir** | La méthode, et le lien vers le comparatif dédié |
| **Où acheter près de chez vous** | Les pages locales, nommées par ville, avec le renvoi au formulaire pour les communes non couvertes |
| **Nos guides** | `::guides` |

Deux règles tiennent tout : **chaque section apporte un fait que le visiteur ne peut pas deviner**, et **aucune section n'est un simple sommaire de liens**. Une page mère sans chiffre daté est une page fade — c'est le défaut qui a fait refaire `/pellets/` le 20 septembre 2026.

## Les CTA : deux formes, pas une

C'est le point où l'on ajuste. Un CTA précoce est bon, mais **sa forme doit suivre l'intention** :

| Type de page | CTA précoce | CTA final |
|---|---|---|
| **Locale, mère** | **Fort** — encadré + bouton, juste après l'intro. Le visiteur cherche déjà un prestataire | Fort, répété |
| **Guide** | **Doux** — une ligne en contexte, style « vous cherchez plutôt quelqu'un pour le faire ? » avec un lien | Fort, encadré |
| **Prix, comparateur** | Le **calculateur** joue ce rôle, en milieu de page | Fort |

Un gros encadré de conversion en haut d'un guide se lit comme un appât et fait repartir le lecteur. Une phrase en contexte au même endroit capte celui qui n'avait pas envie de lire, sans chasser celui qui voulait lire. On garde ton CTA précoce, on l'adapte au registre.

## Mise en forme

| Élément | Quand |
|---|---|
| **Gras** | Sur la réponse, le chiffre, le seuil. Jamais plus d'une expression par paragraphe |
| *Italique* | Termes techniques à leur première apparition, nuances |
| Tableaux | Dès qu'on compare 3 éléments ou plus. **C'est le format qui capte les extraits enrichis** |
| Listes à puces | **Rares.** Voir la règle de ratio ci-dessous |
| Citations | Textes réglementaires, normes, avertissements de sécurité |
| Encadrés | « En bref », mises en garde, « à vérifier » |
| Schémas SVG | Quand une mécanique se montre mieux qu'elle ne s'écrit |

### La règle de ratio

C'est le défaut le plus courant, et il est trompeur : chaque liste prise isolément paraît justifiée, mais leur accumulation transforme l'article en notice.

- **Une seule liste à puces par article**, deux au maximum sur un texte long
- **Jamais deux listes consécutives**, ni deux dans la même section
- L'encadré « En bref » et les tableaux ne comptent pas — ils sont d'un autre registre
- Une liste se justifie quand l'**énumération est le propos** : des symptômes à repérer, des critères à cocher. Pas quand il y a une explication à donner

**Le vrai risque n'est pas esthétique.** Passer en puces fait sauter le pourquoi : on écrit « aspirer le creuset » au lieu d'expliquer que ses perforations s'obstruent de mâchefer, que l'air ne passe plus et que le rendement chute avant tout signe visible. La deuxième version est plus longue, plus agréable, et bien plus utile — c'est elle qui fait revenir le lecteur.

En prose, l'action se met **en gras** : le lecteur pressé scanne quand même.

## Images

Trois sortes d'images, chacune avec son rôle (décision du propriétaire, 24 septembre 2026) :

| Image | Quand | D'où elle vient |
|---|---|---|
| **Image à la une** | Tous les articles, automatiquement | Dessin généré par `tools/images.py`, **sans aucun texte** (Discover, partages). Un motif par verticale : bûches, granulés, cheminée, collines de l'Ardenne pour le local. Remplacée par une vraie photo quand elle existe (`image_une:` dans le front-matter) |
| **Schéma SVG** | De temps en temps, quand un mécanisme se montre mieux qu'il ne s'écrit | Écrit en code : conversion d'unités, points d'entretien, courbe de prix |
| **Photo** | Quand le lecteur doit **voir** quelque chose de réel : reconnaître, comparer, vérifier | D'abord les photos du propriétaire (`photos/`). À défaut, une photo documentaire d'une banque libre (Commons, Unsplash, Pexels), sujet vérifié, crédit en texte, téléchargée seulement avec son accord |

**Jamais** : la photo d'ambiance décorative (feu de cheminée, tas de bûches au soleil), une photo de banque sur une page locale (elle ferait croire à un lieu réel), une image générée qui imite une photo.

Les photos sont redressées, recadrées en 3:2, réduites à 1 600 px, converties en WebP et débarrassées de leurs métadonnées (GPS compris) par `tools/images.py`. Chaque image : `alt` descriptif et honnête, `width`/`height` explicites.

## Jamais de H2 collé à un H3

Un titre de section suivi immédiatement d'un sous-titre laisse le lecteur sans repère et casse la lecture. Sous chaque H2 qui ouvre des H3, **un paragraphe de transition** : ce que couvre la section, et selon quelle logique elle est découpée.

## La phrase commence par son sujet

Le défaut le plus tenace : ouvrir une phrase par une formule d'élan qui ne dit rien. Elle donne l'illusion d'un style alors qu'elle retarde l'information.

| ❌ | ✅ |
|---|---|
| « Tout se joue dans le creuset, cette petite cuve percée… » | « Le creuset est la petite cuve percée où… » |
| « Le geste est court : poêle froid, on aspire… » | « Poêle froid, aspirez le creuset… » |
| « Un mot sur l'aspirateur : un modèle ménager n'est pas adapté. » | « Un aspirateur ménager n'est pas adapté. » |
| « C'est le moment d'aspirer la chambre… » | « Aspirez la chambre… » |
| « Le nettoyage mensuel descend d'un cran : conduits, … » | « Aspirez les conduits, … » |

**Formules bannies** : « tout se joue », « le geste est court », « un mot sur », « c'est le moment de », « profitez-en pour », « concrètement », « la bonne nouvelle c'est que », « il faut savoir que », « à noter que », « il convient de », « force est de constater », « plongeons dans ».

Une phrase commence par son sujet et livre son information. Le style vient de la précision, pas de l'élan.

## Une voix incarnée, sans rien inventer

Le propriétaire a jugé les articles « beaucoup trop impersonnels » le 27 septembre 2026. Un article signé doit se lire comme écrit par quelqu'un, pas par un annuaire. Trois leviers, dans cet ordre :

1. **Ce que nous avons fait pour vous.** « Nous avons relevé les prix sur le site de chaque fournisseur le 24 septembre », « nous avons ramené chaque palette au stère » : c'est vrai, vérifiable, et c'est ce qui distingue la page d'un comparateur automatique. Le « nous » est celui de la rédaction.
2. **Un avis assumé.** Après les faits, dites ce que vous feriez : « Si votre foyer accepte des bûches de 30 cm, c'est l'offre que nous regarderions en premier. » Une recommandation argumentée vaut mieux qu'un « à vous de voir ». Encadré `> 💡` quand elle mérite de ressortir.
3. **Le vécu du terrain, seulement s'il est réel.** Les expériences, anecdotes et constats personnels viennent **uniquement** de `setup/terrain-auteur.md`, que le propriétaire remplit. Jamais d'expérience inventée (« j'ai testé », « chez moi », « un client m'a dit ») : c'est faux, et Google comme le lecteur le détectent.

## La voix : écrire comme quelqu'un qui connaît le métier

Bannir les formules d'élan ne suffit pas à rendre un texte vivant. Un article où chaque phrase a la même forme — sujet, verbe, fait — se lit comme une notice technique. C'est le défaut que le propriétaire a qualifié de « robotique, sans âme » le 20 septembre 2026, et il venait d'une lecture trop mécanique de la règle précédente.

**Partez de la situation du lecteur, pas de la définition.** Il est devant un devis, pas devant une encyclopédie.

| ❌ Encyclopédie | ✅ Quelqu'un qui connaît |
|---|---|
| « Le stère désigne un volume empilé. » | « Un stère est un mètre cube empilé : le bois n'en occupe qu'environ 0,57 m³, le reste est l'air entre les bûches. » |
| « La longueur de coupe influence le volume réel. » | « Un mètre cube empilé de bûches de 33 cm contient plus de 40 % de bois en plus que le même volume en bûches d'un mètre. » |
| « Le taux de cendres varie selon la qualité. » | « Un granulé A2 laisse près du double de cendres d'un A1 : autant de nettoyages en plus. » |

**Nommez l'enjeu, pas seulement le fait.** Un chiffre sans conséquence ne se retient pas. « 488 kg contre 315 kg » ne dit rien ; « pour le même volume facturé, un tiers de chaleur en plus » décide d'un achat.

**Le test du « et alors ? ».** C'est le contrôle le plus important, et celui que je rate le plus souvent. Chaque fait publié doit survivre à la question que se pose le lecteur : qu'est-ce que j'en fais ?

« Un stère ne contient pas un mètre cube de bois : 0,57 m³ en moyenne, le reste est de l'air » ne survit pas. Le lecteur a déjà vu un tas de bûches, il sait qu'il y a de l'air entre elles, et ce chiffre ne lui dit ni quoi demander, ni quoi vérifier, ni quoi comparer. Il se dit « qu'est-ce qu'il me raconte ». Le propriétaire a relevé cette phrase mot pour mot le 20 septembre 2026.

« Un fournisseur qui vous livre un tas d'un mètre cube en bûches de 33 cm vous donne plus de 40 % de bois en plus qu'en bûches d'un mètre. Demandez la longueur de coupe avant de comparer deux prix » survit : le lecteur repart avec une question à poser.

**L'encadré « En bref » est le premier endroit où appliquer ce test.** Il porte les réponses de l'acheteur — combien ça coûte, combien il m'en faut, comment je ne me trompe pas, qui me livre — jamais les faits que la rédaction a trouvés intéressants en chemin. Une statistique de marché, une part de ménages, une définition d'unité n'y ont pas leur place.

**La chute qui sonne bien et n'apprend rien est bannie.** C'est le tic le plus reconnaissable d'un texte écrit par une IA : une phrase courte, détachée, qui donne l'impression d'une révélation sans apporter d'information. « Le reste, vous l'avez payé aussi. » « Et ça change tout. » « La différence est là. » Une phrase courte se garde seulement si elle contient un fait que la précédente ne contenait pas.

**Vérifiez que la formule ne ment pas.** Une tournure qui insinue une arnaque là où il n'y en a pas — laisser croire qu'on facture de l'air alors que le prix au stère intègre les vides par définition — fait perdre la confiance du lecteur qui connaît le sujet, et c'est celui-là qui achète.

**Variez la longueur des phrases**, sans en faire un procédé. Un article dont toutes les phrases font vingt mots endort ; un article qui alterne mécaniquement long-court-long sonne faux.

**Dites « vous ».** Le lecteur achète du bois, il ne consulte pas une fiche produit.

**Ce qui ne change pas** : aucune formule d'élan, aucun superlatif non étayé, aucune mise en bouche. Le style vient de la précision, du rythme et de l'enjeu — jamais de l'ornement.

## Du rythme dans la page

Un mur de paragraphes décourage, même bien écrit. Chaque article de plus de 800 mots porte **au moins deux** de ces éléments, là où ils servent le propos :

| Élément | Syntaxe | Quand |
|---|---|---|
| Chiffres clés | `::chiffres` puis une ligne `valeur \| ce qu'elle signifie` par chiffre (3 idéalement) | Trois chiffres sourcés qui résument la décision. Un bloc par article au plus |
| Astuce | `> 💡 texte` | Le conseil que vous donneriez à un proche |
| Alerte | `> ⚠️ texte` | Sécurité, piège coûteux |
| À savoir | `> ℹ️ texte` | Une précision réglementaire ou une exception |
| Tableau | Markdown | Dès qu'on compare 3 éléments ou plus |
| Schéma | `![[visuels/…svg]]` | Un mécanisme |

Deux encadrés au plus par article : au-delà, plus rien ne ressort.

## La FAQ : seulement quand elle apporte quelque chose

Pas de FAQ par défaut. Une FAQ se justifie quand la recherche fait apparaître **au moins trois questions réelles** (« Autres questions posées », suggestions) auxquelles le corps de l'article ne répond pas déjà sous une H2. Sinon, ces questions deviennent des H2, ou rien. Une FAQ qui répète l'article est du remplissage.

Quand elle existe : section `## Questions fréquentes`, rendue en accordéon, avec `schema: FAQPage`.

## À éviter

- ❌ « Ce n'est pas X, c'est Y » — construction sur-employée
- ❌ Introductions qui annoncent le plan au lieu de répondre
- ❌ Conclusions qui résument ce qu'on vient de lire
- ❌ Le superlatif non étayé — « le meilleur », « le numéro 1 »

## Métadonnées, à chaque article

| Champ | Règle |
|---|---|
| Title SEO | ≤ 60 caractères, requête en tête, année si pertinent |
| Meta description | 150-160 car. Un argument, pas un résumé |
| H1 | Unique, la requête formulée naturellement. Différent du title |
| Slug | Celui de la sitemap, jamais modifié après publication |
| Catégorie | Bois / Pellets / Ramonage / Poêlier |
| Liens internes | **Toujours dans les phrases**, jamais en bloc. L'ancre reprend le mot-clé de la page cible (« taux de cendres », « ramonage d'un poêle à pellets »), pas « ici » ni un titre entier. La mère d'abord, dans le premier tiers. Puis 2-3 sœurs. 1-2 liens vers une autre verticale si le sujet l'appelle vraiment. Ancres variées |
| Schema | FAQPage seulement si la FAQ se justifie (voir « La FAQ »). HowTo si procédure |
| `mots_cles_secondaires` | Les recherches associées reprises dans les H2 |
| `mis_a_jour` | Facultatif (`AAAA-MM-JJ`) : force la date « Mis à jour le ». Sinon elle est posée seule quand le texte change |
| `fil_ariane` | Facultatif : libellé court de la page dans le fil d'Ariane (par défaut, le H1 jusqu'au « : ») |

## Faits vérifiables : sourcés ou retirés

Toute affirmation réglementaire, normative ou chiffrée (prix, fréquence légale, seuil d'une norme, montant d'une prime) repose sur une **source primaire**, citée en fin d'article :

*Sources : SPW Énergie · ENplus — vérifié en septembre 2026.*

**La source est nommée, jamais liée.** Aucun lien sortant dans un article : ni sur la ligne de sources, ni dans le texte. L'URL reste dans les notes de production, que le pipeline ne publie pas, pour que le fait reste vérifiable côté rédaction. Une seule ligne de sources par article, à la fin.

Sans source primaire, on reformule sans le fait. Pour un prix : ce qui le fait varier, puis le devis.

Pendant la rédaction, un fait en attente se note ainsi, et **aucun article ne peut partir tant qu'il en reste un** :

> [À VÉRIFIER] Fréquence légale du ramonage en Wallonie.

## Syntaxe de production

Ce que le pipeline de publication (`tools/wp.py`) comprend en plus du Markdown standard :

| Syntaxe | Rendu |
|---|---|
| `::cta-doux Question ? \| accroche` | Ligne compacte « code postal → Continuer » juste après l'intro : elle fait descendre jusqu'au formulaire, code postal prérempli |
| `::cta-fort Titre \| sous-texte \| bouton (facultatif)` | Formulaire de devis complet en fin d'article, besoin de l'article pré-coché |
| `![[visuels/fichier.svg\|légende]]` | Schéma SVG intégré au contenu |
| `![[photos/fichier.jpg\|légende\|texte alternatif]]` | Photo : préparée, envoyée dans la médiathèque et intégrée à la publication |
| `::table-rotative` suivi d'un tableau | Même tableau, ordre des lignes tiré au hasard chaque jour (le maillage quotidien republie). Pour une liste de prestataires sans en favoriser aucun : pas de lien ni de contact dans les colonnes |
| `::guides` | Liste des guides en ligne de la verticale, groupés par intention. **Sur chaque page mère** |
| `::chiffres` + lignes `valeur \| texte` | Cartes de chiffres clés |
| `> 💡 …` · `> ⚠️ …` · `> ℹ️ …` | Encadré astuce, alerte, à savoir |
| `> [À VÉRIFIER] …` | Bloque la publication |
| `<!-- … -->` | Notes internes, jamais publiées |

**Pas de « À lire aussi », pas de ligne de renvoi `→`, pas de liste de liens en fin de section** : le pipeline les refuse (contrôle bloquant). Chaque lien interne est une expression de la phrase, ancrée sur le sujet de la page cible. Seul `::guides` reste, sur les pages mères : c'est leur sommaire.

**Liens internes** : on lie la mère et 2-3 sœurs selon la sitemap, même si ces pages n'existent pas encore. Au rendu, un lien vers une page absente devient du texte simple ; le maillage quotidien le réactive le jour où la page sort. Les formulaires n'apparaissent que si le plugin de réception est actif et la politique de confidentialité en ligne.

**FAQ** (facultative) : section `## Questions fréquentes`, chaque question en gras sur sa ligne, la réponse juste en dessous. Rendue en accordéon ; avec `schema: FAQPage`, le balisage JSON-LD est généré automatiquement.

**Généré par le rendu, à ne pas écrire** : fil d'Ariane, H1 affiché, cadre auteur avec les dates, sommaire (dès 4 H2), encadré auteur en fin d'article.
