---
slug: politique-de-confidentialite
title_seo: "Politique de confidentialité"
meta_description: "Les données collectées par nos formulaires de devis, pourquoi, à qui nous les transmettons, combien de temps nous les gardons et comment exercer vos droits."
h1: "Politique de confidentialité"
type: page
requete_cible: "politique de confidentialité"
statut: brouillon
mis_a_jour: 2026-10-04
---

# Politique de confidentialité

Ce site met en relation des particuliers avec des professionnels du chauffage au bois en Wallonie : fournisseurs de bois et de pellets, ramoneurs, poêliers. Cette page explique ce que deviennent les informations que vous nous confiez quand vous demandez un devis, et ce que le site charge quand vous le consultez.

## Qui est responsable de vos données

Le responsable du traitement est l'éditeur du site bois-de-chauffage-et-pellets.be, la société **Indexio EOOD**.

Pour toute question sur vos données, écrivez à **contact@bois-de-chauffage-et-pellets.be**. Nous répondons à toute question sur vos données dans un délai d'un mois, comme le prévoit le RGPD.

## Les données collectées par le formulaire de devis

Quand vous remplissez un formulaire de demande de devis, nous recevons :

| Donnée | Obligatoire | À quoi elle sert |
|---|---|---|
| Nom | Oui | Permettre au professionnel de s'adresser à vous |
| Adresse e-mail | Oui | Vous envoyer le devis et vous répondre |
| Téléphone | Non | Vous rappeler, si vous préférez |
| Code postal | Oui | Trouver les professionnels qui interviennent chez vous |
| Besoin et détails (essence, quantité, appareil…) | Oui | Préparer un devis qui correspond à votre demande |
| Délai souhaité et précisions libres | Non | Préciser votre demande |
| Page d'où vous avez envoyé le formulaire | Automatique | Savoir quel article a suscité la demande |

N'écrivez dans le champ « précisions » que ce qui sert votre demande : inutile d'y mettre des informations sur votre santé, votre situation financière ou celle d'autres personnes.

Pour bloquer les envois automatiques, le site retient pendant une heure une empreinte chiffrée de votre adresse IP, qui ne permet pas de la retrouver. Elle sert seulement à limiter le nombre d'envois depuis une même connexion, puis s'efface.

## Pourquoi nous utilisons ces données, et sur quelle base

Nous les utilisons pour une seule chose : transmettre votre demande à des professionnels de votre zone, pour qu'ils vous proposent un devis. La base légale est votre **consentement**, donné en cochant la case du formulaire (article 6.1.a du RGPD). Sans cette case cochée, la demande n'est pas envoyée.

Vous pouvez retirer votre consentement à tout moment en nous écrivant. Nous cessons alors de transmettre votre demande et nous la supprimons. Le retrait ne remet pas en cause les transmissions déjà faites.

## À qui nous transmettons votre demande

Votre demande est transmise à **trois professionnels au plus**, choisis selon votre code postal et le besoin que vous avez coché. Ce sont des entreprises établies en Belgique ou dans un pays voisin de l'Union européenne, comme le Grand-Duché de Luxembourg pour certains fournisseurs qui livrent la province de Luxembourg.

Dès qu'un professionnel vous contacte, il devient lui-même responsable des données que vous échangez avec lui, pour établir son devis puis, si vous l'acceptez, pour exécuter la commande.

Nous ne vendons pas vos données, nous ne les louons pas et nous ne les utilisons pas pour vous envoyer de la publicité.

## Combien de temps nous les gardons

Nous conservons chaque demande **12 mois** après sa réception, pour pouvoir répondre si vous revenez vers nous ou si un professionnel ne vous a pas contacté. Elle est ensuite supprimée. Si vous retirez votre consentement ou demandez l'effacement avant ce délai, nous la supprimons dès réception de votre demande.

## Où sont hébergées vos données

Le site et les demandes de devis sont hébergés par **Infomaniak**, en Suisse. La Commission européenne reconnaît que la Suisse offre un niveau de protection des données adéquat, équivalent à celui de l'Union européenne. Les demandes ne sont accessibles qu'aux administrateurs du site.

## Ce que le site charge quand vous le consultez

Le site ne contient **aucun outil de mesure d'audience**, aucun pixel publicitaire, aucune vidéo ni carte intégrée. Il ne dépose pas de cookie de suivi.

Deux services extérieurs sont appelés à l'affichage des pages, et reçoivent à cette occasion votre adresse IP, comme tout serveur qui envoie un fichier à votre navigateur :

- **Google Fonts** (Google), qui fournit les polices de caractères du site ;
- **Gravatar** (Automattic), qui fournit la photo de l'auteur affichée dans les articles.

Ces deux services sont établis aux États-Unis. Ils ne reçoivent aucune donnée de vos demandes de devis.

## Vos droits

Vous pouvez à tout moment accéder à vos données, les faire rectifier ou effacer, en limiter l'usage, vous opposer à leur traitement, en recevoir une copie dans un format courant, ou retirer votre consentement. Écrivez à contact@bois-de-chauffage-et-pellets.be, en précisant l'adresse e-mail utilisée dans votre demande de devis.

Si vous estimez que vos droits ne sont pas respectés, vous pouvez introduire une plainte auprès de l'**Autorité de protection des données**, rue de la Presse 35, 1000 Bruxelles.

## Mises à jour de cette politique de confidentialité

Nous mettons cette page à jour quand le site change, par exemple si un nouvel outil y est ajouté. La date de dernière mise à jour figure en haut de la page.

<!--
NOTES DE PRODUCTION

CONSTATS TECHNIQUES (04/10/2026)
- Hébergement : DNS ns41/ns42.infomaniak.com, IP 83.166.138.108 (Infomaniak),
  MX mta-gw.infomaniak.ch. Centres de données Infomaniak en Suisse.
  Suisse : décision d'adéquation de la Commission européenne (2000/518/CE,
  confirmée par le rapport de janvier 2024).
- Pages d'accueil et /bois-de-chauffage-virton/ : aucun Google Analytics, GTM,
  Matomo, pixel Meta, Hotjar/Clarity, YouTube, Maps, reCAPTCHA. Présents :
  fonts.googleapis.com (Elementor) et gravatar.com (cadre auteur).
  → À REVOIR si un outil de mesure est ajouté (bannière de consentement alors
  nécessaire). Conseil au propriétaire : Elementor → Réglages → Performances →
  « Charger Google Fonts localement » supprime l'appel à Google ; remplacer
  l'avatar Gravatar par une photo de la médiathèque supprime l'appel à Gravatar.
  Retirer alors la liste correspondante de la page.
- Plugin bcp-leads : IP non stockée, seulement md5(IP + sel) en transient d'une
  heure (anti-spam, 5 envois/h). Champs : nom, email, tel (facultatif), cp,
  besoins + sous-champs, delai, message (facultatif), page/source.

IDENTITÉ : « Indexio EOOD » + contact@bois-de-chauffage-et-pellets.be, sans adresse
  ni numéro d'entreprise, à la demande du propriétaire (04/10/2026).
À COMPLÉTER PAR LE PROPRIÉTAIRE
- Valider la durée de 12 mois (proposition par défaut).
- Partenaires : la phrase « Belgique ou pays voisin de l'UE » couvre Wilwert
  énergie (Sanem, L). Si un partenaire hors UE est ajouté, revoir la page.

URL DES SOURCES (notes internes, jamais publiées)
- Autorité de protection des données : https://www.autoriteprotectiondonnees.be
- Décision d'adéquation Suisse : https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32000D0518
-->
