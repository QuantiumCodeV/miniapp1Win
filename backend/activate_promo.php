<?php

include "config.php";

$promo = $_POST["promo"];
$user_id = $_POST['user_id'];

$result = $mysql->query("SELECT * FROM promo_codes WHERE code = '$promo'")->fetch_assoc();

if (!$result) {
    echo json_encode(["error" => "Code promo introuvable"]);
} else {
    // Vérifions si l'utilisateur a déjà utilisé ce code promo
    $used_check = $mysql->query("SELECT * FROM promo_uses WHERE user_id = '$user_id' AND code = '$promo'")->fetch_assoc();
    
    if ($used_check) {
        echo json_encode(["error" => "Vous avez déjà utilisé ce code promo"]);
    }
    // Vérifions le nombre d'utilisations
    else if ($result['current_uses'] >= $result['max_uses']) {
        echo json_encode(["error" => "Le code promo a atteint le nombre maximum d'utilisations"]);
    } else {
        // Mettons à jour le nombre d'utilisations
        $mysql->query("UPDATE promo_codes SET current_uses = current_uses + 1 WHERE code = '$promo'");
        
        // Ajoutons l'utilisation du code promo
        $mysql->query("INSERT INTO promo_uses (user_id, code) VALUES ('$user_id', '$promo')");
        $mysql->query("UPDATE users SET balance = balance + {$result['amount']} WHERE user_id = '$user_id'");
        echo json_encode([
            "success" => "Code promo activé. {$result['amount']} ₣ crédités",
            "amount" => $result['amount']
        ]);
    }
}
?>