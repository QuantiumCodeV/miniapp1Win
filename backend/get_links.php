<?php
include "config.php";

$result = $mysql->query("SELECT * FROM links");

echo json_encode($result->fetch_assoc());
?>