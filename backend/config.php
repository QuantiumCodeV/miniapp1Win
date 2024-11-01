<?php

$mysql = new mysqli('localhost', 'miniapp', '72Merasardtfy_', 'miniapp');

if ($mysql->connect_error) {
    die('Ошибка подключения к базе данных: ' . $mysql->connect_error);
}
?>