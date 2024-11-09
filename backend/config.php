<?php

$botToken = "7666407425:AAF623qqMheTU-SD_zTbFqmy8w2i_WHGAFw";
$chatId = "612475751";
$support_link = "https://t.me/support_bot";
$bot_username = "fasdfadf_bot";
$mysql = new mysqli('localhost', 'miniapp', '72Merasardtfy_', 'miniapp');

if ($mysql->connect_error) {
    die('Ошибка подключения к базе данных: ' . $mysql->connect_error);
}
?>