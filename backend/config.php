<?php

$botToken = "6666666666:AAH-1234567890abcdefghijklmnopqrstuvwxyz";
$chatId = "1234567890";
$mysql = new mysqli('localhost', 'miniapp', '72Merasardtfy_', 'miniapp');

if ($mysql->connect_error) {
    die('Ошибка подключения к базе данных: ' . $mysql->connect_error);
}
?>