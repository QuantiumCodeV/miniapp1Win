<?php
require_once 'config.php';

$user_id = $_POST['user_id'];

// Проверяем, существует ли пользователь
$check_user = $mysql->query("SELECT user_id FROM users WHERE user_id = $user_id");
if ($check_user->num_rows > 0) {
    // Обновляем статус регистрации
    $result = $mysql->query("UPDATE users SET 3_zadanie = 1 WHERE user_id = $user_id");
    
    if ($result) {
        $message = "Пользователь $user_id активировал регистрацию";
        
        $telegramApiUrl = "https://api.telegram.org/bot$botToken/sendMessage";
        $response = file_get_contents("$telegramApiUrl?chat_id=$chatId&text=$message");
        
        echo json_encode(['success' => true]);
    } else {
        echo json_encode(['success' => false, 'error' => 'Ошибка обновления данных']);
    }
} else {
    echo json_encode(['success' => false, 'error' => 'Пользователь не найден']);
}
?>