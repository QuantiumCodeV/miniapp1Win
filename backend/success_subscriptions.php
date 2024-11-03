<?php
include "config.php";

$user_id = $_POST["user_id"];
$zadanie = $_POST["zadanie"];


$mysql->query("UPDATE users SET $zadanie = TRUE, balance = balance + 1000 WHERE user_id = '$user_id'");


echo json_encode(["success" => true]);
?>