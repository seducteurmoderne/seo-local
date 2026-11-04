<?php
/**
 * Plugin Name: Demandes de devis — Devis Élagage Lux
 * Version: 2
 * Généré par le moteur commun (python3 tools/autopilote.py plugin) depuis site.json : ne pas modifier à la main.
 * Description: Reçoit les formulaires de devis intégrés aux articles, les enregistre dans l'admin et les envoie par e-mail.
 *
 * À déposer dans wp-content/mu-plugins/.
 * Adresse de réception : ajouter  define('BCP_LEADS_EMAIL', 'vous@domaine.be');  dans wp-config.php,
 * sinon les demandes partent vers l'e-mail administrateur du site.
 */
if (!defined('ABSPATH')) {
    exit;
}

function bcp_leads_destinataire() {
    return defined('BCP_LEADS_EMAIL') ? BCP_LEADS_EMAIL : get_option('admin_email');
}

// Les demandes sont stockées comme contenus privés, lisibles par les administrateurs seulement
// (pas par le compte Éditeur de l'API, et jamais exposées par l'API REST).
add_action('init', function () {
    $cap = 'manage_options';
    register_post_type('bcp_lead', array(
        'labels'       => array('name' => 'Demandes de devis', 'singular_name' => 'Demande de devis', 'menu_name' => 'Demandes de devis'),
        'public'       => false,
        'show_ui'      => true,
        'show_in_rest' => false,
        'menu_icon'    => 'dashicons-email-alt',
        'supports'     => array('title', 'editor'),
        'map_meta_cap' => false,
        'capabilities' => array(
            'edit_post' => $cap, 'read_post' => $cap, 'delete_post' => $cap, 'read' => $cap,
            'edit_posts' => $cap, 'edit_others_posts' => $cap, 'edit_private_posts' => $cap, 'edit_published_posts' => $cap,
            'delete_posts' => $cap, 'delete_others_posts' => $cap, 'delete_private_posts' => $cap, 'delete_published_posts' => $cap,
            'publish_posts' => $cap, 'read_private_posts' => $cap, 'create_posts' => 'do_not_allow',
        ),
    ));
});

add_action('rest_api_init', function () {
    register_rest_route('leads/v1', '/lead', array(
        array('methods' => 'GET', 'permission_callback' => '__return_true',
              'callback' => function () { return array('actif' => true); }),
        array('methods' => 'POST', 'permission_callback' => '__return_true',
              'callback' => 'bcp_leads_recevoir'),
    ));
    // Suivi des demandes pour le panel du parc (version 2) : réservé aux comptes connectés qui peuvent écrire des articles.
    register_rest_route('leads/v1', '/lead/suivi', array(
        'methods' => 'GET',
        'permission_callback' => function () { return current_user_can('edit_posts'); },
        'callback' => 'bcp_leads_suivi',
    ));
});

// Date, page d'origine, besoins, code postal et délai de chaque demande. Ni nom, ni e-mail, ni téléphone, ni message :
// rien qui permette de contacter la personne ne sort par l'API.
function bcp_leads_suivi() {
    $ids = get_posts(array('post_type' => 'bcp_lead', 'post_status' => 'private', 'numberposts' => -1,
                           'fields' => 'ids', 'orderby' => 'date', 'order' => 'DESC', 'suppress_filters' => true));
    $demandes = array();
    foreach ($ids as $id) {
        $demandes[] = array(
            'id'      => $id,
            'date'    => get_post_time('c', true, $id),
            'source'  => (string) get_post_meta($id, 'bcp_source', true),
            'besoins' => array_values((array) get_post_meta($id, 'bcp_besoins', true)),
            'cp'      => (string) get_post_meta($id, 'bcp_cp', true),
            'delai'   => (string) get_post_meta($id, 'bcp_delai', true),
        );
    }
    return array('version' => 2, 'demandes' => $demandes);
}

function bcp_leads_erreur($message, $code = 400) {
    return new WP_REST_Response(array('ok' => false, 'message' => $message), $code);
}

function bcp_leads_recevoir(WP_REST_Request $req) {
    $p = $req->get_json_params();
    if (!is_array($p)) {
        $p = $req->get_body_params();
    }

    // Pièges à robots : champ caché rempli, ou formulaire envoyé trop vite / trop tard.
    if (!empty($p['site_web'])) {
        return new WP_REST_Response(array('ok' => true), 200);
    }
    $t0 = isset($p['t0']) ? (int) floor(((float) $p['t0']) / 1000) : 0;
    $duree = time() - $t0;
    if ($t0 <= 0 || $duree < 3 || $duree > 7200) {
        return bcp_leads_erreur('Le formulaire a expiré. Rechargez la page, puis recommencez.');
    }

    // Cinq demandes par heure au plus depuis une même adresse.
    $ip = isset($_SERVER['REMOTE_ADDR']) ? $_SERVER['REMOTE_ADDR'] : '';
    $cle = 'bcp_lead_' . md5($ip . wp_salt());
    $nombre = (int) get_transient($cle);
    if ($nombre >= 5) {
        return bcp_leads_erreur('Trop de demandes envoyées depuis votre connexion. Réessayez dans une heure.', 429);
    }

    $texte = function ($cle_champ, $max = 200) use ($p) {
        if (!isset($p[$cle_champ]) || is_array($p[$cle_champ])) {
            return '';
        }
        return mb_substr(sanitize_text_field(wp_unslash($p[$cle_champ])), 0, $max);
    };

    $cp      = $texte('cp', 6);
    $nom     = $texte('nom', 120);
    $email   = isset($p['email']) && !is_array($p['email']) ? sanitize_email($p['email']) : '';
    $tel     = $texte('tel', 40);
    $delai   = $texte('delai', 60);
    $message = isset($p['message']) && !is_array($p['message']) ? mb_substr(sanitize_textarea_field(wp_unslash($p['message'])), 0, 2000) : '';
    $source  = isset($p['source']) && !is_array($p['source']) ? esc_url_raw($p['source']) : '';
    $page    = $texte('page', 200);
    $prenom  = $texte('prenom', 80);
    if ($prenom === '') {
        return bcp_leads_erreur('Indiquez votre prénom.');
    }
    if ($nom === '') {
        return bcp_leads_erreur('Indiquez votre nom.');
    }
    if (!preg_match('/^[+0-9 ().\/-]{8,}$/', $tel)) {
        return bcp_leads_erreur('Indiquez un numéro de téléphone pour être rappelé.');
    }
    $nom = trim($prenom . ' ' . $nom);
    $cp = $cp !== '' ? $cp : '—';
    if ($nom === '') {
        return bcp_leads_erreur('Indiquez votre nom.');
    }
    if (!is_email($email)) {
        return bcp_leads_erreur('Vérifiez votre adresse e-mail.');
    }
    if (empty($p['consentement'])) {
        return bcp_leads_erreur('Sans votre accord, nous ne pouvons pas transmettre votre demande.');
    }

    $libelles = array('elagage' => 'Élagage', 'abattage' => 'Abattage', 'dessouchage' => 'Dessouchage', 'haubanage' => 'Haubanage', 'plantation' => 'Plantation');
    $recus = isset($p['besoins']) ? (array) $p['besoins'] : array();
    $besoins = array_values(array_intersect(array_keys($libelles), $recus));
    if (!$besoins) {
        return bcp_leads_erreur('Cochez au moins un besoin.');
    }

    $details = array(
        'elagage' => array(),
        'abattage' => array(),
        'dessouchage' => array(),
        'haubanage' => array(),
        'plantation' => array(),
    );
    $lignes = array();
    foreach ($besoins as $b) {
        $lignes[] = '— ' . $libelles[$b];
        foreach ($details[$b] as $champ => $libelle) {
            $v = $texte($champ);
            if ($v !== '') {
                $lignes[] = "   $libelle : $v";
            }
        }
    }

    $corps = implode("\n", array_merge(
        array("Nom : $nom", "E-mail : $email", 'Téléphone : ' . ($tel !== '' ? $tel : '—'), "Code postal : $cp",
              'Délai : ' . ($delai !== '' ? $delai : '—'), '', 'Besoins :'),
        $lignes,
        array('', 'Précisions : ' . ($message !== '' ? $message : '—'), '', "Page : $page", "Adresse : $source",
              'Reçue le ' . wp_date('d/m/Y à H:i'))
    ));
    $resume = implode(' + ', array_map(function ($b) use ($libelles) { return $libelles[$b]; }, $besoins));

    $id = wp_insert_post(array(
        'post_type'    => 'bcp_lead',
        'post_status'  => 'private',
        'post_title'   => "$resume — $cp — $nom",
        'post_content' => $corps,
    ), true);
    if (is_wp_error($id)) {
        return bcp_leads_erreur("L'enregistrement a échoué. Réessayez dans un instant.", 500);
    }
    foreach (array('cp' => $cp, 'nom' => $nom, 'email' => $email, 'tel' => $tel, 'delai' => $delai, 'source' => $source) as $k => $v) {
        update_post_meta($id, "bcp_$k", $v);
    }
    update_post_meta($id, 'bcp_besoins', $besoins);
    set_transient($cle, $nombre + 1, HOUR_IN_SECONDS);

    wp_mail(bcp_leads_destinataire(), "[Devis] $resume — $cp — $nom", $corps, array('Reply-To: ' . $email));

    return new WP_REST_Response(array('ok' => true), 200);
}
