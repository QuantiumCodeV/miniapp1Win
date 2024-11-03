<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

include "config.php";

$result = $mysql->query("SELECT * FROM links");

if ($result && $result->num_rows > 0) {
    echo json_encode($result->fetch_assoc());
} else {
    echo json_encode($result);
}
?>