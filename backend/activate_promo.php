<?php

include "config.php";

$promo = $_POST["promo"];

$result = $mysql->query("SELECT * FROM promo_codes WHERE code = '$promo'")->fetch_assoc();

if (!$result) {
    echo json_encode(["error" => "Промокод не найден"]);
} else {
    // Проверяем количество использований
    if ($result['current_uses'] >= $result['max_uses']) {
        echo json_encode(["error" => "Промокод уже использован максимальное количество раз"]);
    } else {
        // Обновляем количество использований
        $mysql->query("UPDATE promo_codes SET current_uses = current_uses + 1 WHERE code = '$promo'");
        
        // Добавляем запись об использовании промокода
        $user_id = $_POST['user_id']; // Получаем ID пользователя
        $mysql->query("INSERT INTO promo_uses (user_id, code) VALUES ('$user_id', '$promo')");
        $mysql->query("UPDATE users SET balance = balance + {$result['amount']} WHERE user_id = '$user_id'");
        echo json_encode([
            "success" => "Промокод активирован. Начислено {$result['amount']} ₣",
            "amount" => $result['amount']
        ]);
    }
}
?>