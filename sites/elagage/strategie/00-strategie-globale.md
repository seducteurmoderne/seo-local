# Site élagage — mots-clés et structure (version 2)
**Brouillon du 13/10/2026.** Il remplace la version 1 : on garde le français seul, on retire les pages sur les permis et la réglementation, et on se concentre sur les **services**, chacun avec son mot-clé principal décliné **en local**. Il rejoindra `sites/<nom>/strategie/` quand le domaine sera connu.

**Services couverts** : abattage · élagage · haubanage · dessouchage · plantation d'arbres, d'arbustes et de fruitiers · plantation de haies · plantes de façade.
**Zone** : le Grand-Duché d'abord, puis la province de Luxembourg.

## 1. Les 4 sites de référence
| Site | Ce que c'est | Structure | Pages locales | À reprendre / à éviter |
|---|---|---|---|---|
| elagage.net | Site de leads, comme le nôtre : guides et formulaire `/devis` | 15 URLs, guides de 1 200 à 1 500 mots (accueil, abattage, taille, droits, devis) | Aucune | **À reprendre** : de longs guides par service, qui répondent à tout (période, technique, prix, dessouchage, déchets). **Il lui manque** le local, que nous ajoutons |
| elagage-abattage-aquitaine.fr | Entreprise | Service × grande ville (`/abattage-arbre-bordeaux/`, `/dessouchage-bordeaux/`…), page combinée par commune (`/elagage-abattage-merignac-33700/`), page prix | 16 communes, environ 640 mots, gabarit identique | **À reprendre** : le motif *service + ville* et la page prix. **À éviter** : le même texte partout, les blocs de réassurance répétés, les émojis dans les titres |
| mselagage.fr | Entreprise | 3 pages services (de 190 mots seulement) + `/elagueur-<ville>/` | 23 communes, environ 950 mots | **À reprendre** : le mot-clé « élagueur + ville » dans l'URL et le H1. **À éviter** : un texte de remplissage où seul le nom change (les « doorway pages » que Google sanctionne) |
| lgb-paysage.fr | Paysagiste | `/nos-metiers/<service>` + `/zones-intervention/<commune>` | Environ 80 communes, **1 200 mots** | **Le meilleur modèle de page locale** : le terrain de la commune (sol, relief, eau, points de vigilance), une FAQ propre à la ville, la situation, les communes voisines. C'est notre règle « une page locale repose sur des données propres à sa ville » |

**Notre position** : la profondeur d'elagage.net sur les pages services, plus le maillage local d'Aquitaine, plus la qualité locale de LGB. Tout ça dans une zone où aucun des quatre n'est présent.

## 2. Les mots-clés principaux, service par service
D'après les suggestions Google relevées en Belgique et au Luxembourg (plus de 2 500, triées). Les volumes viendront d'un export Semrush.

| Service | Mot-clé principal | Variantes qui comptent | Pages guides tirées des variantes |
|---|---|---|---|
| **Abattage** | abattage arbre | abattage d'arbre · faire abattre un arbre · couper un arbre dans son jardin · abattage arbre prix · faire abattre un gros arbre prix · abattage arbre et évacuation prix · abattage d'arbre avec nacelle · abattage arbre dangereux · couper un arbre qui penche · couper un arbre mort · couper un arbre par le haut · abattage arbre autour de moi | prix, arbre dangereux, arbre qui penche, démontage d'un gros arbre |
| **Élagage** | élagage / élagueur | élagage arbre · élagueur grimpeur · élagage et abattage · entreprise élagage · élagage arbre prix · élagueur autour de moi · élagage arbre période · élaguer un arbre trop haut · élaguer un arbre en hauteur | prix, période, arbre trop haut, grimpeur ou nacelle, fruitiers |
| **Dessouchage** | dessouchage | dessouchage arbre (prix, entreprise) · rognage souche · rognage de souche · rognage souche tarif · dessouchage thuyas · rognage souche thuya | prix, thuyas |
| **Haubanage** | haubanage arbre | haubanage arbre prix · hauban arbre · haubanage branche arbre · câble. **Attention** : « haubanage » seul est un terme médical (rotule, fracture) : toujours écrire « haubanage d'arbre » | La page service suffit |
| **Plantation d'arbres** | plantation arbre / planter un arbre | plantation arbre fruitier · plantation arbre prix · plantation arbre période · planter un arbre adulte (déjà grand) · planter un arbre près de la maison | prix, arbre adulte, fruitier |
| **Plantation de haie** | plantation haie / planter une haie | prix · période · essences | quelle haie planter |
| **Plantes de façade** | plante grimpante façade | façade nord / sud / maison · végétalisation façade maison · plante grimpante qui n'abîme pas la façade · mur à l'ombre | façade nord |

**Ce qui reste hors périmètre** (le prochain site, ou plus tard) :
- la taille de haie : forte demande, mais pas dans votre liste ;
- « paysagiste + ville » : la requête locale la plus fréquente, présente dans presque toutes les communes, mais elle vise la création de jardin, pas votre acheteur.

## 3. Ce que montre le local
Nombre de suggestions locales par commune, sur 12 formulations (élagage, élagueur, abattage arbre, dessouchage, paysagiste…) :

| Commune | Élagage / élagueur / abattage | Autres (paysagiste, jardinier) |
|---|---|---|
| **Luxembourg** (pays) | **15** (élagage luxembourg, élagueur luxembourg, abattage arbre luxembourg prix, entreprise élagage luxembourg…) | 15 |
| **Arlon** | 6 | 8 |
| **Marche-en-Famenne** | 4 | 17 |
| Bouillon | 3 | 5 |
| Mamer, Neufchâteau | 2 | 5 à 8 |
| Bastogne, Libramont, Virton | 1 | 4 |
| Esch-sur-Alzette, Mersch, Bertrange, Mondorf, Dudelange… | 0 | 5 à 13 |
| Clervaux, Martelange, Vielsalm, Houffalize | 0 | 0 à 1 |

**Ce qu'on en tire.**
- **Les mots-clés locaux sont « élagueur <ville> », « élagage <ville> » et « abattage arbre <ville> ».** Ce sont aussi ceux des concurrents français.
- **« Luxembourg » seul porte la demande du Grand-Duché.** Les communes grand-ducales, elles, n'ont presque aucune suggestion : la page pays est la page la plus importante du site.
- Les petites communes se font quand même, comme sur le site bois : peu de volume, mais peu de concurrence, et elles convertissent.

## 4. La structure
**3 catégories WordPress, 7 pages services, 16 guides, 90 pages locales** : 116 URLs dans `sitemap-urls.csv`, toutes de premier niveau.

| Catégorie | Pages services (mères) |
|---|---|
| Abattage | `/abattage-arbre/` · `/dessouchage/` |
| Élagage | `/elagage/` · `/haubanage-arbre/` |
| Plantation | `/plantation-arbres/` · `/plantation-haie/` · `/plantes-facade/` |

**La déclinaison locale** (le cœur du site, au rythme de 4 pages locales pour 1 guide) :

| Niveau | Communes | Pages par commune |
|---|---|---|
| Pays | Grand-Duché, province de Luxembourg | `/elagage-luxembourg/`, `/abattage-arbre-luxembourg/` (et de même pour la province) |
| Grandes villes | Luxembourg-Ville, Arlon, Marche-en-Famenne, Esch-sur-Alzette, Bastogne | `/elagage-<ville>/`, `/abattage-arbre-<ville>/`, `/dessouchage-<ville>/`, `/plantation-arbres-<ville>/` |
| Autres communes | 33 communes (16 au Grand-Duché, 17 en province) | `/elagage-<ville>/`, `/abattage-arbre-<ville>/` |

- **Haubanage** : aucune suggestion « haubanage arbre + lieu » (Luxembourg, Belgique, Wallonie, Arlon : 0 le 14/10/2026). Pas une page par commune : une seule page test `/haubanage-arbre-luxembourg/` (Grand-Duché et province), plus un paragraphe sur le haubanage dans chaque page `/elagage-<ville>/` (« sauver l'arbre plutôt que l'abattre »), qui capte la recherche locale sans page vide. **Façade** : page nationale seule.
- **Ordre de sortie.** Vague 1 : les pages pays, la zone de l'acheteur (Beckerich, Redange, Steinfort, Mersch, Mamer, Luxembourg-Ville) et Arlon. Puis les grandes villes, puis le reste.
- **Mots-clés de chaque page locale.** `/elagage-<ville>/` : H1 « Élagueur à <ville> : élagage d'arbres », title « Élagage <ville> : élagueur, prix et devis ». `/abattage-arbre-<ville>/` : H1 « Abattage d'arbre à <ville> », avec « couper un arbre » et « dessouchage » dans le texte.

**Ce qui distingue les deux pages d'une même ville** (pour ne pas faire deux fois le même texte) :
- *Élagage* : les essences courantes de la commune (vergers du Gutland, hêtres et chênes d'Ardenne, alignements urbains), la période de taille, l'arbre trop haut près de la maison, l'élagueur grimpeur dans les jardins sans accès.
- *Abattage* : les arbres à risque du coin (épicéas scolytés en Ardenne, arbres morts après la sécheresse), le démontage en ville, l'évacuation du bois et des branches (parc à conteneurs ou recyparc de la commune), le dessouchage.

**Ce qui rend chaque page locale propre** (pas de règlement, pas de permis) :
- les entreprises qui nomment la commune sur leur propre site ;
- les villages et quartiers desservis, et les communes voisines ;
- le terrain : jardins en pente, accès étroits, centre ancien ;
- les arbres typiques du coin ;
- où déposer les branches ;
- les prix publiés, s'il y en a ;
- une FAQ seulement si des questions propres à la ville existent.

C'est le modèle de LGB, adapté à l'élagage.

## 5. Le formulaire de devis
- **Besoins (cases)** : abattage · élagage · dessouchage · haubanage · plantation (arbres, arbustes, fruitiers, haies, façade).
- **Champs** : nombre d'arbres · hauteur (moins de 5 m, 5 à 10 m, 10 à 20 m, plus de 20 m) · proche d'une maison, d'une route ou d'une ligne · accès d'un camion ou d'une nacelle · évacuation des déchets oui ou non · délai (urgent, sous un mois, à la bonne saison).
- **Code postal** : le formulaire doit accepter les codes belges (6600 à 6999) et luxembourgeois (L-xxxx). C'est une modification du moteur, à faire en session et à tester sur le site bois.

## 6. Reste à décider
1. **Le domaine** : .lu ou .be ? Un mot-clé dans le domaine (`elagage-…`) aide un peu, comme pour elagage.net.
2. **Les volumes** : un export Semrush (Belgique et Luxembourg) des mots-clés de la section 2 et des combinaisons « élagueur / élagage / abattage arbre + ville » de la section 3. Il dira combien de communes méritent leurs pages.
3. **La taille de haie et « paysagiste + ville »** : à garder pour plus tard, ou à inclure si l'acheteur prend aussi ces chantiers.

## 7. Structure type d'une page `/elagage-<ville>/` (14/10/2026)
Aucune entreprise citée : la page envoie vers le formulaire, qui transmet la demande à l'élagueur partenaire. Même structure partout, texte nourri par des faits propres à la commune (villages, relief et accès, essences typiques, recyparc ou parc à conteneurs, arbres remarquables, communes voisines, photos de chantiers de l'acheteur s'il en fournit).

```
H1  Élagueur à <ville> : élagage d'arbres, prix et devis
[En bref] prix repère selon la hauteur · période · villages couverts · devis gratuit
Intro + ::cta-fort
H2  Comment trouver un bon élagueur à <ville> ?        ← cible « élagueur <ville> » et « comment trouver un élagueur »
    réponse directe 40-60 mots, puis : assurance RC, devis écrit détaillé (hauteur,
    méthode, évacuation comprise ou non), méthode adaptée (grimpeur ou nacelle),
    démarcheurs au porte-à-porte et acompte en liquide (alerte à sourcer).
    Fin : « nous transmettons votre demande à un élagueur qui intervient à <ville> »
H2  Prix d'un élagage à <ville> en 2026                 tableau par hauteur, sourcé ou facteurs seuls
H2  Quand élaguer un arbre à <ville>
H2  Arbre trop haut ou dangereux à <ville> : élagage, haubanage ou abattage ?   → /abattage-arbre-<ville>/
H2  Évacuation des branches à <ville> : broyage ou recyparc
H2  Élagage autour de <ville> : villages et communes voisines
H2  Questions fréquentes (seulement si 3 questions propres à la ville)
::cta-fort
```
Pour `/abattage-arbre-<ville>/`, même logique : « Trouver une entreprise d'abattage d'arbres à <ville> », prix avec ou sans évacuation, démontage près d'une maison, dessouchage, que faire du bois.

## 8. Réglage du moteur pour ce site (14/10/2026)
Le site élagage pose dans `site.json` : `"seo": {"brief_locales_facultatif": true}`. Ses pages de ville n'exigent plus l'analyse des 10 résultats Google ni le brief : elles partent du modèle local et des données de la commune. Le contrôle continue de refuser une page locale dont plus de 50 % du texte se retrouve dans une autre (avertissement dès 35 %). Les pages services et les guides gardent le brief complet.

## 9. Décisions du 15/10/2026 (remplacent les sections 4 et 5 là où elles diffèrent)

**Ordre de production** (colonnes `etape` et `ordre` de `sitemap-urls.csv`, 177 URLs) :
0. **Jour du lancement** : les 5 pages services, mises au menu : `/elagage/`, `/abattage-arbre/`, `/dessouchage/`, `/haubanage-arbre/`, `/plantation/`. `/plantation/` regroupe arbres, arbustes, fruitiers, haies et plantes de façade ; `/plantation-haie/` et `/plantes-facade/` deviennent des guides.
1. **Mères locales** : `/elagage-luxembourg/`, `/abattage-arbre-luxembourg/` (Grand-Duché), `/elagage-province-de-luxembourg/`, `/abattage-arbre-province-de-luxembourg/`.
2. **Villes**, deux pages chacune (élagage, abattage). Beckerich d'abord, puis par anneaux de distance autour de Beckerich (0-15, 15-30, 30-45, plus de 45 km), les communes les plus peuplées en premier dans chaque anneau. 68 communes : 42 au Grand-Duché, 26 en province.
3. Dessouchage et plantation dans les 5 grandes villes, et la page test haubanage.
4. Les 18 guides.

**Maillage en cascade** : page ville → mère locale de son pays (`/elagage-luxembourg/` ou `/elagage-province-de-luxembourg/`) → page service (`/elagage/`). Chaque mère locale cite et relie ses villes, comme `::guides` sur les pages mères du site bois.

**Formulaire sur chaque page**, plus simple que celui du site bois :
- Titre adapté à la page : « Un élagage à faire ? Faites appel à un professionnel » (« Un abattage… », « Un dessouchage… », « Un haubanage… », « Une plantation… »).
- Sous-titre : « Renseignez vos coordonnées pour être recontacté rapidement par un professionnel de votre région ».
- Champs : Prénom · Nom · E-mail · Téléphone · Informations (facultatif, placeholder « Décrivez votre demande »).
- Le besoin est déduit de la page, sans case à cocher. La page d'origine part avec la demande : sur une page de ville, l'élagueur sait où intervenir.
- À garder : la case de consentement avec le lien vers la politique de confidentialité (RGPD) et le piège anti-robots.
- **Moteur** : le formulaire actuel impose les cases de besoin, le code postal et le délai. Il faut un mode `"formulaire": {"mode": "simple", …}` dans `site.json` et l'adaptation du plugin de réception. C'est à faire à la création du site, testé sur les deux sites, et le site bois reste inchangé.

## 10. Design (15/10/2026)
**Direction A, éditorial** (`designs/a-editorial.html`), choisie par le propriétaire : le B fait trop moderne, trop « SaaS », pour l'élagage. Ce qui est gardé : Source Serif 4 et Familjen Grotesk, le fond papier, les filets fins, l'accent brun-rouille et le vert. À adapter : le formulaire simple de la section 9 en encadré sobre, sur chaque page, et des photos de chantiers réels dès que l'acheteur en fournit.
