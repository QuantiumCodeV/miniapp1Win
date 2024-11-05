<?php

include "config.php";

$promo = $_POST["promo"];
$user_id = $_POST['user_id'];

$result = $mysql->query("SELECT * FROM promo_codes WHERE code = '$promo'")->fetch_assoc();

if (!$result) {
    echo json_encode(["error" => "Промокод не найден"]);
} else {
    // Проверяем использовал ли пользователь этот промокод
    $used_check = $mysql->query("SELECT * FROM promo_uses WHERE user_id = '$user_id' AND code = '$promo'")->fetch_assoc();
    
    if ($used_check) {
        echo json_encode(["error" => "Вы уже использовали этот промокод"]);
    }
    // Проверяем количество использований
    else if ($result['current_uses'] >= $result['max_uses']) {
        echo json_encode(["error" => "Промокод достиг максимального количества использований"]);
    } else {
        // Обновляем количество использований
        $mysql->query("UPDATE promo_codes SET current_uses = current_uses + 1 WHERE code = '$promo'");
        
        // Добавляем использование промокода
        $mysql->query("INSERT INTO promo_uses (user_id, code) VALUES ('$user_id', '$promo')");
        $mysql->query("UPDATE users SET balance = balance + {$result['amount']} WHERE user_id = '$user_id'");
        echo json_encode([
            "success" => "Промокод активирован. {$result['amount']} ₣ зачислено",
            "amount" => $result['amount']
        ]);
    }
}
?>