<?php
include "config.php";

$user_id = $_POST["user_id"];

$result = $mysql->query("SELECT * FROM users WHERE referrer_id = '$user_id'");
$friends = array();
while ($row = $result->fetch_assoc()) {
    $friends[] = array(
        'user_id' => $row['user_id'],
        'username' => $row['username'], 
        'level' => $row['level'],
        'balance' => $row['balance'],
        'invited_users' => $row['invited_users'],
        'join_date' => $row['join_date'],
        'zadanie_1' => $row['zadanie_1'],
        'zadanie_2' => $row['zadanie_2'], 
        'zadanie_3' => $row['zadanie_3'],
        'zadanie_4' => $row['zadanie_4'],
        'zadanie_5' => $row['zadanie_5']
    );
}
echo json_encode($friends);
