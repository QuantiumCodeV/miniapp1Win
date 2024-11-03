<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

include "config.php";

$result = $mysql->query("SELECT * FROM links");

echo json_encode($result->fetch_assoc());
?>