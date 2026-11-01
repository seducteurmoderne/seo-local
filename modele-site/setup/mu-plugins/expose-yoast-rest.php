<?php
// wp-content/mu-plugins/expose-yoast-rest.php — rend title, meta description et mot-clé Yoast modifiables par l'API.
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
