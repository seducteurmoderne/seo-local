# Accès WordPress

## Ce que je te demande de créer

**Un utilisateur dédié**, pas ton compte admin :

1. `Utilisateurs → Ajouter` → identifiant `claude`, rôle **Éditeur**
2. Te connecter comme cet utilisateur (ou éditer son profil) → section **Mots de passe d'application** → en créer un nommé `Claude Code`
3. WordPress affiche une chaîne du type `abcd EFGH ijkl MNOP qrst UVWX` — **elle n'est affichée qu'une fois**

### ⚠️ Ne colle pas ce mot de passe dans le chat
Il se retrouverait dans l'historique de conversation. À la place :

```bash
cat > "/Users/thomasdufour/Documents/CLAUDE.nosync/SITES/sites/bois-chauffage/setup/.env" <<'ENV'
WP_URL=https://bois-de-chauffage-et-pellets.be
WP_USER=claude
WP_APP_PASSWORD=colle-le-mot-de-passe-ici
ENV
```

Je lirai le fichier au moment de faire les appels, sans jamais l'afficher. Tu révoques le mot de passe en un clic quand on a fini, sans toucher à ton compte.

**Pourquoi Éditeur et pas Administrateur** : le rôle Éditeur permet de créer et modifier pages, articles et catégories — tout ce dont j'ai besoin pour produire. Il ne permet ni d'installer de plugin, ni de modifier les réglages, ni de toucher au thème. Les tâches d'administration de la Phase 0 restent chez toi, ce qui limite ce qu'un accès automatisé peut casser.

## Deux blocages possibles

**Sécurité** : Wordfence, iThemes Security ou certains hébergeurs bloquent l'API REST ou les mots de passe d'application. Si ça coince, il faut autoriser `/wp-json/` pour cet utilisateur.

**Yoast n'expose pas ses champs à l'API REST par défaut.** Sans ça je peux écrire le contenu mais pas les balises title et meta description — ce qui vide l'intérêt de l'accès. Le correctif est un fichier à déposer dans `wp-content/mu-plugins/` (à créer si le dossier n'existe pas) :

```php
<?php
// wp-content/mu-plugins/expose-yoast-rest.php
add_action('init', function () {
    $keys = ['_yoast_wpseo_title', '_yoast_wpseo_metadesc', '_yoast_wpseo_focuskw'];
    foreach (['post', 'page'] as $type) {
        foreach ($keys as $key) {
            register_post_meta($type, $key, [
                'show_in_rest'  => true,
                'single'        => true,
                'type'          => 'string',
                'auth_callback' => function () { return current_user_can('edit_posts'); },
            ]);
        }
    }
});
```

## Ce que je ferai, et ce que je ne ferai pas

| Je fais | Je ne fais pas |
|---|---|
| Créer les pages **en brouillon** | Publier — c'est toi qui valides |
| Rédiger contenu, titres, métas | Toucher aux réglages ou aux plugins |
| Poser le maillage interne | Supprimer quoi que ce soit d'existant |
| Assigner catégories et étiquettes | Modifier le thème |

**Tout part en brouillon.** Tu relis, tu publies. Aucune page ne sort sans ton accord.
