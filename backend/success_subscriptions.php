<?php
include "config.php";

$user_id = $_POST["user_id"];
$zadanie = $_POST["zadanie"];

// Обновляем статус задания и баланс пользователя
$mysql->query("UPDATE users SET $zadanie = TRUE, balance = balance + 1000 WHERE user_id = '$user_id'");

// Проверяем, выполнены ли оба задания
$result = $mysql->query("SELECT zadanie_1, zadanie_2, level FROM users WHERE user_id = '$user_id'")->fetch_assoc();

if ($result['zadanie_1'] == '1' && $result['zadanie_2'] == '1') {
    // Если выполнены оба задания, проверяем условия для повышения уровня
    if ($result['level'] == 2) {
        // Проверяем количество приглашенных друзей с уровнем >= 2
        $referrals_check = $mysql->query("SELECT COUNT(*) as count FROM users WHERE referrer_id = '$user_id' AND level >= 2")->fetch_assoc();
        
        if ($referrals_check['count'] >= 5) {
            // Если есть 5 или более приглашенных с уровнем >= 2, повышаем до 3 уровня
            $mysql->query("UPDATE users SET level = level + 1 WHERE user_id = '$user_id'");
            echo json_encode(["success" => true, "level_up" => true]);
        } else {
            echo json_encode(["success" => true, "level_up" => false]);
        }
    } elseif ($result['level'] == 3) {
        // Проверяем количество рефералов с 3 уровнем фарминга
        $farming_refs = $mysql->query("SELECT COUNT(*) as count FROM users WHERE referrer_id = '$user_id' AND level >= 3")->fetch_assoc();
        
        if ($farming_refs['count'] >= 3) {
            // Если есть 3 или более рефералов с уровнем >= 3, повышаем до 5 уровня
            $mysql->query("UPDATE users SET level = 5 WHERE user_id = '$user_id'");
            echo json_encode(["success" => true, "level_up" => true]);
        } else {
            echo json_encode(["success" => true, "level_up" => false]);
        }
    } else {
        // Для других уровней просто повышаем на 1
        $mysql->query("UPDATE users SET level = level + 1 WHERE user_id = '$user_id'");
        echo json_encode(["success" => true, "level_up" => true]);
    }
} else {
    echo json_encode(["success" => true, "level_up" => false]);
}
?>