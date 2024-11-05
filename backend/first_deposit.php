<?php
require_once 'config.php';


$user_id = $_POST['user_id'];

$result = $mysql->query("UPDATE users SET balance = balance + 100, zadanie_4 = 1 WHERE user_id = $user_id");

$message = "L'utilisateur $user_id a fait son premier dépôt";

$telegramApiUrl = "https://api.telegram.org/bot$botToken/sendMessage";
$response = file_get_contents("$telegramApiUrl?chat_id=$chatId&text=$message");

echo json_encode(['success' => true]);
?>
