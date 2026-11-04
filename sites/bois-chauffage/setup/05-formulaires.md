# Formulaires de devis : mise en service

Les articles embarquent un formulaire de devis : une ligne « code postal → Continuer » après l'intro, et le formulaire complet en fin d'article. Les quatre besoins (bois, pellets, ramonage, poêlier) y sont proposés en cases à cocher, celui de l'article déjà coché : une visite peut produire plusieurs leads.

**Tant que les étapes 1 et 4 ne sont pas faites, aucun formulaire ne s'affiche.** Dès qu'elles le sont, la passe de maillage du lendemain matin installe les formulaires sur tous les articles publiés.

## 1. Déposer le plugin
`setup/mu-plugins/bcp-leads.php` → dans `wp-content/mu-plugins/`, à côté de `expose-yoast-rest.php`.

## 2. Choisir l'adresse de réception
Dans `wp-config.php`, avant la ligne « C'est tout, ne touchez pas à ce qui suit » :
```php
define('BCP_LEADS_EMAIL', 'votre@adresse.be');
```
Sans cette ligne, les demandes partent vers l'e-mail administrateur du site.

## 3. Fiabiliser l'envoi des e-mails
L'envoi natif de WordPress finit souvent en spam. Installer **WP Mail SMTP** (gratuit) et le brancher sur une vraie boîte. De toute façon, **aucune demande n'est perdue** : elles sont toutes enregistrées dans le menu **Demandes de devis** de l'admin.

## 4. Compléter la politique de confidentialité
`articles/politique-de-confidentialite.md` : identité de l'entreprise, contact, durée de conservation, hébergeur, outils de mesure. Je la publie ensuite. Transmettre des coordonnées à des professionnels tiers impose d'informer la personne (RGPD, article 13) : sans cette page, le formulaire ne serait pas conforme.

## 5. Test
J'envoie une demande marquée « TEST », tu vérifies qu'elle arrive dans l'admin et dans ta boîte.

## Ce que fait le plugin
- Reçoit les envois sur `/wp-json/bcp/v1/lead`, contrôle chaque champ, enregistre la demande en contenu privé et l'envoie par e-mail, avec la page d'origine.
- Anti-spam : champ piège invisible, délai minimal de 3 secondes avant l'envoi, 5 demandes par heure au plus depuis une même connexion.
- Les demandes ne sont visibles que des administrateurs. Le compte `claude` (Éditeur) n'y a pas accès, et elles ne sont jamais exposées par l'API.
