<?php
include "config.php";

$user_id = $_POST["user_id"];

$result = $mysql->query("SELECT * FROM users WHERE referrer_id = '$user_id'");
$friends = array();
while($row = $result->fetch_assoc()) {
    $friends[] = array(
        'user_id' => $row['user_id'],
        'username' => $row['username'],
        'level' => $row['level'],
        'join_date' => $row['join_date']
    );
}
echo json_encode($friends);
?>