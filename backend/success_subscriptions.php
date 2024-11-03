<?php
include "config.php";

$user_id = $_POST["user_id"];
$zadanie = $_POST["zadanie"];


$mysql->query("UPDATE users SET $zadanie = TRUE WHERE user_id = '$user_id'");

echo json_encode(["success" => true]);
?>