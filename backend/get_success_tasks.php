<?php

include "config.php";

$user_id = $_POST["user_id"];

$result = $mysql->query("SELECT * FROM users WHERE user_id = '$user_id'");

echo json_encode($result->fetch_assoc());
?>