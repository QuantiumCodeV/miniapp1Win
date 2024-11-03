<?php
require_once 'config.php';

$user_id = $_POST['user_id'];

$result = $mysql->query("SELECT * FROM links WHERE user_id = $user_id");

echo json_encode($result->fetch_assoc());
?>