<?php

include "config.php";

$promo = $_POST["promo"];

$result = $mysql->query("SELECT * FROM promo_codes WHERE code = '$promo'")->fetch_assoc();

if (!$result) {
    echo json_encode(["error" => "Code promo introuvable"]);
} else {
    // Vérifier le nombre d'utilisations
    if ($result['current_uses'] >= $result['max_uses']) {
        echo json_encode(["error" => "Le code promo a déjà été utilisé le nombre maximum de fois"]);
    } else {
        // Mettre à jour le nombre d'utilisations
        $mysql->query("UPDATE promo_codes SET current_uses = current_uses + 1 WHERE code = '$promo'");
        
        // Ajouter l'utilisation du code promo
        $user_id = $_POST['user_id']; // Obtenir l'ID utilisateur
        $mysql->query("INSERT INTO promo_uses (user_id, code) VALUES ('$user_id', '$promo')");
        $mysql->query("UPDATE users SET balance = balance + {$result['amount']} WHERE user_id = '$user_id'");
        echo json_encode([
            "success" => "Code promo activé. {$result['amount']} ₣ crédités",
            "amount" => $result['amount']
        ]);
    }
}
?>