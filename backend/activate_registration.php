<?php
require_once 'config.php';

$user_id = $_GET['user_id'];

// Vérifier si l'utilisateur existe
$check_user = $mysql->query("SELECT user_id FROM users WHERE user_id = $user_id");
if ($check_user->num_rows > 0) {
    // Mettre à jour le statut d'inscription
    $result = $mysql->query("UPDATE users SET zadanie_3 = 1 WHERE user_id = $user_id");
    
    if ($result) {
        $message = "L'utilisateur $user_id a activé son inscription";
        
        $telegramApiUrl = "https://api.telegram.org/bot$botToken/sendMessage";
        $response = file_get_contents("$telegramApiUrl?chat_id=$chatId&text=$message");
        
        echo json_encode(['success' => true]);
    } else {
        echo json_encode(['success' => false, 'error' => 'Erreur lors de la mise à jour des données']);
    }
} else {
    echo json_encode(['success' => false, 'error' => 'Utilisateur non trouvé']);
}
?>