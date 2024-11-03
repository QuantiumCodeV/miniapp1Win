<?php
require_once 'config.php';
$result = $mysql->query("SELECT * FROM links WHERE");

echo json_encode($result->fetch_assoc());
?>