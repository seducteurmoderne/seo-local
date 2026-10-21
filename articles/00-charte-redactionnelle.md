# Charte rédactionnelle
**6 sept. 2026**

## Le principe : la réponse d'abord

En 2026 une page doit répondre **avant le premier scroll**. Deux raisons qui se cumulent :

- Les **AI Overviews et les moteurs conversationnels** citent les pages qui répondent directement. Une page qui fait deux paragraphes de mise en bouche avant d'arriver au fait n'est pas citée — elle n'est même pas lue.
- Le lecteur qui ne trouve pas sa réponse en dix secondes repart, et ce retour au SERP est un signal négatif.

D'où le bloc **« En bref »** en tête, dès que la requête appelle une réponse factuelle.

**L'« En bref » est un court paragraphe, pas une liste** (demande du propriétaire, 16/10/2026) : 2 ou 3 phrases qui répondent au mot-clé principal de la page et résument ce que dit l'article, chiffre clé compris. Sa longueur et son contenu changent d'une page à l'autre ; jamais 4 puces de même structure plaquées sur chaque page. Syntaxe : `> ### En bref` puis une seule ligne `> texte`. Il n'est jamais obligatoire. **Les pages prix** (`/prix-pellets/`, `/prix-bois-de-chauffage/`) sont des pages, pas des articles, et n'en ont pas : elles ouvrent sur le titre daté en carte (`entete: carte`, H1 « Prix du pellet le {{aujourdhui}} ») puis sur la carte du prix du jour (`::prix-jour`, première ligne en grand, repères dessous) — demande du propriétaire, 10/10/2026.

## Structure type

```
Fil d'Ariane — Accueil › page mère › titre court     ← généré
H1 — la requête, formulée naturellement
Cadre auteur — nom, rôle, publié le, mis à jour le    ← généré (site.json → auteur)
┌─────────────────────────────────────┐
│ EN BREF                             │  ← la réponse en 2-3 phrases (voir ci-dessous)
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

## Le brief SEO, avant d'écrire une ligne

Un article répond à une intention, pas à un mot-clé. Le brief se fait avec **le moteur de brief en cascade** :

```
python3 tools/autopilote.py brief <slug> [<liens google.be>…]
```

Il enchaîne sept étapes, chacune avec ses solutions de repli, et reprend là où il s'est arrêté :

| Étape | Ce qu'elle fait | Si ça bloque |
|---|---|---|
| 1. Suggestions | Les variantes que les Belges tapent (suggestions Google Belgique, puis DuckDuckGo) | Source suivante |
| 2. Candidats | Jusqu'à 30 pages classées : les liens google.be donnés en argument d'abord, puis DuckDuckGo région Belgique | Source suivante |
| 3. Lecture | Lit les pages une à une **jusqu'à 10 lisibles** : une page bloquée, vide ou vidéo est sautée, on passe à la suivante | Page suivante |
| 4. Lecteur | **Notre propre analyse, par l'IA, sans regarder les concurrents** : qui cherche, dans quelle situation, ce qu'il veut lire en premier, ses questions dans l'ordre, ses objections, ce qui le ferait demander un devis | L'agent répond lui-même au prompt |
| 5. Concurrents | L'IA lit les plans des 10 pages : intention que Google récompense, sections incontournables, différenciantes, lacunes, faiblesses | Idem |
| 6. Brief | L'IA croise 4 et 5 avec la charte : intention, plan H2/H3 avec le contenu et la forme de chaque section, données à sourcer, décision | Idem |
| 7. Critique | L'IA relit le brief en directeur SEO exigeant et le corrige | Idem |

L'IA est appelée par `claude -p` (l'abonnement du propriétaire) ; si elle ne répond pas, le moteur écrit la question dans `briefs/<slug>/<étape>.prompt.md` et l'agent qui l'exécute y répond en JSON dans `<étape>.json`, puis relance. Le bloc `BRIEF SEO` final s'inscrit dans les notes de production de l'article, le détail (contenu de chaque section, objections, déclencheur du devis) dans `briefs/<slug>/brief.md`. **On rédige ensuite en suivant ce plan** : le contrôle signale une H2 hors plan et une section du plan absente.

**Les liens google.be** se relèvent dans le navigateur : `https://www.google.be/search?q=<requête>&hl=fr&gl=be&num=10` (bannière de cookies : « Tout refuser »), liens des résultats organiques et « Autres questions posées ». Sans navigateur ou devant un CAPTCHA (on ne le contourne jamais), le moteur se contente de DuckDuckGo région Belgique.

Le bloc inscrit dans les notes ressemble à ceci :

```
BRIEF SEO
Intention : ce que veut la personne qui tape la requête, et ce qu'elle fera après
Format SERP : quels types de pages occupent le top 10 (guides, pages de services, pages locales, forums, vidéos)
Structure SERP : ce que les pages ont en commun (longueur médiane, H2 récurrents, formats), d'après briefs/<slug>.md
Variantes : variante 1 ; variante 2 ; …        (suggestions, recherches associées)
Termes : terme 1 ; terme 2 ; …                 (le vocabulaire que les pages classées emploient)
Questions :
- question réelle 1                             (titres en question du top 10, « Autres questions posées »)
Plan :
- H2 : titre
  - H3 : titre
Décision : l'angle retenu, et ce que nous ferons mieux que le top 10
```

**L'intention décide de la page.** Quand le top 10 est fait de pages de services (dépanneurs, livreurs), la requête est commerciale : la page ouvre sur la demande de devis, puis apporte ce que les pages de services n'ont pas (le diagnostic, les prix, la comparaison). Quand il est fait de guides, la page est un guide, au format qui domine.

Le front-matter porte aussi `entites:` : l'objet de l'article tel que les gens le nomment (« poêle à pellets », « bois de chauffage », « ramonage »). Une page locale porte en plus `ville:`.

## Les titres : chacun se lit seul, comme une recherche Google

Une H2 est lue par Google comme le sujet de sa section, et par le lecteur comme une ligne du sommaire. Elle doit dire **de quoi elle parle sans le reste de la page**. C'est la règle que le contrôle applique : **80 % des H2 au moins nomment l'objet de l'article** (une de ses `entites`, ou la ville d'une page locale), sinon la publication est refusée.

| ❌ Titre d'accroche | ✅ Titre qui se classe |
|---|---|
| Les deux gestes qui aggravent la panne | Les 2 gestes qui aggravent la panne d'un poêle à pellets |
| Le poêle ne s'allume pas | Poêle à pellets qui ne s'allume pas : les 4 causes |
| Comparer trois offres qui ne parlent pas la même langue | Comparer 3 devis de bois de chauffage à Arlon : stère, m³ et longueur |
| Livraison : ce que chaque fournisseur décrit | Livraison de pellets à Arlon : délais, minimum et accès |
| Les essences : ce qui change vraiment | Quelle essence de bois de chauffage choisir : chêne, hêtre, charme |

- **Les nombres en chiffres** (« 3 causes », pas « trois causes ») : ils attirent l'œil dans les résultats
- **Une question quand c'est la question de l'acheteur** (« Combien coûte un stère de bois à Bastogne ? »), suivie d'une réponse directe de 40 à 60 mots
- **Deux H2 au moins reprennent la requête cible** ou une variante du brief ; les autres reprennent les variantes et les questions du brief
- **Une phrase naturelle**, jamais une liste de mots-clés : « Prix du stère de bois à Bastogne » oui, « Bois chauffage Bastogne prix stère pas cher » non
- **Jamais de titre d'accroche** : « vraiment », « ce qu'il faut savoir », « le bon réflexe », « en pratique », « fausse bonne idée », « quel X pour quel Y »… (liste dans `moteur/seo.py`, contrôle bloquant)
- Les H3 suivent la même règle quand ils portent une recherche (« Poêle à pellets en alarme : lire le code d'erreur »)

**La relecture des titres** : avant de publier, lisez la liste des H2 seule, sans le texte. Si on ne devine pas l'article ni la recherche à laquelle chaque section répond, réécrivez.

## Paragraphes et phrases : lisibles du premier coup

Le lecteur parcourt avant de lire. Il lit la première phrase de chaque paragraphe et décide de continuer ou non.

- **La première phrase porte l'idée du paragraphe.** Les suivantes la prouvent ou la précisent. Un paragraphe = une idée
- **4 phrases et 80 mots au plus par paragraphe** (avertissement au-delà de 80, refus au-delà de 110)
- **Des phrases de 20 mots en moyenne**, et 10 % au plus au-delà de 30 mots (refus au-delà de 20 %). Une phrase longue se coupe à son « et », à son « parce que », à sa relative
- **Un sujet concret** : « le creuset s'encrasse », pas « l'encrassement du creuset intervient »
- **La requête ou l'objet de l'article dans la première phrase de l'introduction** (contrôle bloquant)
- Le contrôle donne chaque phrase et chaque paragraphe en trop : on corrige ceux-là, pas tout l'article

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
| Tableaux | Dès qu'on compare 3 éléments ou plus. **C'est un des formats qui captent les extraits optimisés** (voir « Ce que Google affiche ») |
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

Une image se prévoit dans le brief, section par section, quand elle montre quelque chose d'utile : reconnaître, comparer, situer, retenir un chiffre. Jamais d'image d'ambiance (feu de cheminée, salon cosy, tas de bûches au soleil).

| Image | Quand | D'où elle vient |
|---|---|---|
| **Image à la une** | Tous les articles, automatiquement | Dessin généré par `tools/images.py`, **sans aucun texte**. Remplacée par une vraie photo quand elle existe (`image_une:`) |
| **Photo** | Le lecteur doit voir un objet réel | 1. les photos du propriétaire (`photos/`) ; 2. **vraies photos de la banque Canva**, choisies par le propriétaire dans l'éditeur Canva (le connecteur ne donne pas accès à la banque : ce qu'il « crée » est généré par IA) ; 3. photos libres Openverse / Wikimedia Commons, licence vérifiée, crédit en légende |
| **Illustration IA** | Quand on veut une illustration, décidé au cas par cas | Générée dans Canva, **assumée comme illustration** (légende « Illustration »), jamais présentée comme une photo d'un lieu, d'un produit ou d'une personne réels. Jamais sur une page locale |
| **Visuel d'information** | Un repère chiffré, des étapes, un comparatif qui se lisent mieux en image | Conçu dans Canva aux couleurs du site |
| **Schéma, courbe, carte** | Un mécanisme, une évolution de prix, les vendeurs autour d'une ville | Générés par le moteur en SVG (`visuels/`) |

**Formats** (syntaxe : `![[photos/<fichier>|légende|texte alternatif|format]]`) :

| Format | Affichage | Fichier préparé | Usage |
|---|---|---|---|
| `600` (par défaut) | 600 × 400, centré dans le texte | 1 200 × 800 WebP | L'image descriptive qui coupe l'article |
| `banniere` | 3:1 sur toute la largeur | 1 800 × 600 WebP | Ouvrir ou séparer une grande section, un visuel d'information |
| `large` | Pleine largeur du texte, 3:2 | 1 600 × 1 067 WebP | Une photo qui doit se voir en détail |

Le moteur redresse, recadre, réduit, convertit en WebP et retire toutes les métadonnées (GPS compris). Cible : **moins de 100 Ko par image** (un 600 × 400 pèse 20 à 60 Ko).

**Le nom du fichier décrit l'image**, en minuscules et tirets, avec le mot-clé de l'article quand il décrit vraiment ce qu'on voit, une fois : `creuset-poele-a-pellets-encrasse.jpg`, `sac-pellets-enplus-a1-15-kg.jpg`. Jamais `IMG_2034.jpg`, `canva-design.png` ni `pellets-pellets-arlon-pellets.jpg`. Ce nom part tel quel dans la médiathèque (contrôle bloquant si le nom ne décrit rien).

**Le texte alternatif dit ce qu'on voit**, en 25 à 140 caractères, avec le mot-clé s'il en fait partie naturellement : « Creuset d'un poêle à pellets encrassé de mâchefer, trous d'arrivée d'air bouchés ». Pas de « image de », pas de liste de mots-clés (contrôle : absent = bloquant ; sans l'objet de l'article ni dans le nom ni dans l'alt = avertissement).

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

## Les pages locales : un modèle, des données propres

Toutes les pages de ville suivent **le même modèle** (`articles/_modeles/locale-<verticale>.md`), créé par `python3 tools/autopilote.py modele <slug>` : mêmes sections, mêmes titres au nom de la ville. Une structure commune est normale et efficace ; ce que Google sanctionne (« doorway pages »), c'est le **texte** identique dont seul le nom de ville change.

- **Chaque section porte au moins une donnée propre à la ville** : fournisseurs qui la livrent, prix relevé, délai, minimum de commande, accès, communes desservies. Une donnée absente se dit absente, elle ne s'invente pas
- **Les fournisseurs tiennent dans le tableau** (nom, commune, formats, livraison à la ville). Pas de paragraphe par fournisseur ni de catalogue de leurs marques : le lecteur veut savoir qui le livre, pas lire leurs fiches
- **Les explications générales** (formats, certifications, essences) tiennent en 2 ou 3 phrases et renvoient à la page mère
- **Garde-fou automatique** : le contrôle compare la page aux autres pages locales de sa verticale. Plus de 35 % de texte commun avec l'une d'elles = avertissement, plus de 50 % = refus

## Ce que Google affiche, et comment le capter

Les résultats enrichis par balisage ne concernent presque plus un site comme le nôtre : **Google a supprimé les FAQ dépliées le 7 mai 2026** (réservées aux sites publics et de santé depuis 2023) et **HowTo depuis septembre 2023**. Ce qui reste à capter tient à la **forme du texte**, pas à un balisage. On choisit le format selon la page, jamais tous à la fois.

| Ce que Google affiche | Ce qui le déclenche | À viser quand |
|---|---|---|
| Extrait optimisé « paragraphe » | Une H2 en question, suivie d'une **réponse directe de 40 à 60 mots** qui se lit seule (le chiffre, la règle, la condition), puis le détail | La requête est une question : combien, quand, à quelle fréquence, qu'est-ce que. Une ou deux H2 par article, celles qui portent la requête cible |
| Extrait « liste » | Une **liste numérotée** d'étapes courtes, verbe à l'impératif, sous une H2 « Comment… » | Une procédure : allumer, entretenir, vérifier, stocker. Elle compte comme la liste de l'article |
| Extrait « tableau » | Un tableau de 3 lignes au moins, l'élément comparé en première colonne | Comparatif, prix, valeurs normatives |
| « Autres questions posées » et réponses des IA | Des questions réelles reprises en H2 ou en FAQ, la réponse dans la première phrase | La recherche fait apparaître des questions que le corps ne traite pas |
| Fil d'Ariane, article, organisation | Générés (Yoast et le rendu) | Toujours : rien à écrire |
| Image dans les résultats | Une photo propre au sujet, avec un texte alternatif descriptif | Dès qu'une photo du propriétaire existe |
| Vidéo avec moments clés | Une vidéo intégrée et son balisage VideoObject | Seulement si le propriétaire fournit une vidéo |

**Par type de page :**
- **Guide pratique** (entretien, allumage, séchage) : une réponse directe sous la H2 qui porte la requête, une liste numérotée si l'article décrit une procédure.
- **Guide de choix ou de qualité** : le tableau, puis une réponse directe à « lequel choisir ».
- **Page mère** : un tableau et une réponse directe dans la section prix. Pas de FAQ.
- **Page locale** : le modèle local (voir « Les pages locales : un modèle, des données propres »), avec ses réponses directes à « Qui livre … à <ville> ? » et « Prix … à <ville> ». FAQ seulement si des questions propres à la ville existent.

**Jamais de balisage Product, Review ni LocalBusiness** : nous ne vendons pas, nous ne notons pas les prestataires et nous ne sommes pas un commerce local. Le déclarer serait trompeur, et Google le sanctionne.

### La FAQ : seulement quand elle apporte quelque chose

Pas de FAQ par défaut. Une FAQ se justifie quand la recherche fait apparaître **au moins trois questions réelles** (« Autres questions posées », suggestions) auxquelles le corps de l'article ne répond pas déjà sous une H2. Sinon, ces questions deviennent des H2, ou rien. Une FAQ qui répète l'article est du remplissage.

Quand elle existe : section `## Questions fréquentes`, rendue en accordéon, avec `schema: FAQPage`. Le balisage est gardé parce que Bing et les assistants IA le lisent, mais il ne donne plus rien dans Google : ce n'est jamais la raison d'ajouter une FAQ.

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
| Liens internes | **Toujours dans les phrases**, jamais en bloc. L'ancre reprend le mot-clé de la page cible (« taux de cendres », « ramonage d'un poêle à pellets »), pas « ici » ni un titre entier. La mère d'abord, dans le premier tiers. Puis 2-3 sœurs. 1-2 liens vers une autre verticale si le sujet l'appelle vraiment. **Ancres variées d'un article à l'autre** : vers `/bois-de-chauffage/`, « bois de chauffage », « bois de chauffage en Wallonie », « en Belgique », « acheter du bois de chauffage » ; vers `/pellets/`, « pellets en Belgique », « granulés de bois », « pellets de chauffage ». Jamais l'ancre propre à une autre page |
| Schema | FAQPage seulement si la FAQ se justifie (voir « La FAQ »). Jamais HowTo (abandonné par Google), jamais Product, Review ni LocalBusiness |
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
| `::prix-jour` + lignes `valeur \| texte` | Carte du prix du jour, juste sous le titre : la première ligne en grand, les suivantes en repères. Pages prix seulement |
| `entete: carte` (front-matter) | Titre de la page dans une carte compacte au lieu du bandeau, pour que le prix monte à l'écran |
| `> 💡 …` · `> ⚠️ …` · `> ℹ️ …` | Encadré astuce, alerte, à savoir |
| `> [À VÉRIFIER] …` | Bloque la publication |
| `{{prix:id}}` · `{{calc:expr}}` (`calc1`, `calc2` : décimales ; `min()`, `max()`) · `{{releve}}` · `{{releve:id}}` · `{{aujourdhui}}` | Prix relu chaque jour chez le fournisseur (`prix/releves.json`), calcul arrondi à l'unité, date du relevé. Voir la procédure, « Prix dynamiques » |
| `<!-- … -->` | Notes internes, jamais publiées |

**Pas de « À lire aussi », pas de ligne de renvoi `→`, pas de liste de liens en fin de section** : le pipeline les refuse (contrôle bloquant). Chaque lien interne est une expression de la phrase, ancrée sur le sujet de la page cible. Seul `::guides` reste, sur les pages mères : c'est leur sommaire.

**Liens internes** : on lie la mère et 2-3 sœurs selon la sitemap, même si ces pages n'existent pas encore. Au rendu, un lien vers une page absente devient du texte simple ; le maillage quotidien le réactive le jour où la page sort. Les formulaires n'apparaissent que si le plugin de réception est actif et la politique de confidentialité en ligne.

**FAQ** (facultative) : section `## Questions fréquentes`, chaque question en gras sur sa ligne, la réponse juste en dessous. Rendue en accordéon ; avec `schema: FAQPage`, le balisage JSON-LD est généré automatiquement.

**Généré par le rendu, à ne pas écrire** : fil d'Ariane, H1 affiché, cadre auteur avec les dates, sommaire (dès 4 H2), encadré auteur en fin d'article.
