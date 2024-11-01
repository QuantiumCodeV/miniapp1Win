<?php
include "config.php";

$user_id = $_POST["user_id"];

$result = $mysql->query("SELECT balance FROM users WHERE user_id = '$user_id'")->fetch_assoc();
echo json_encode($result);
?>