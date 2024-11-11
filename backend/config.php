<?php

$botToken = "8094002698:AAEmA01XnMzEwmn5rlhZVj8uWr6gKNxQlN4";
$chatId = "5685109533";
$support_link = "https://t.me/support_bot";
$bot_username = "fasdfadf_bot";
$mysql = new mysqli('localhost', 'admin', '72Merasardtfy_', 'miniapp');

if ($mysql->connect_error) {
    die('Ошибка подключения к базе данных: ' . $mysql->connect_error);
}
?>