<?php

$mysql = new mysqli('localhost', 'root', '', 'miniapp');

if ($mysql->connect_error) {
    die('Ошибка подключения к базе данных: ' . $mysql->connect_error);
}
?>