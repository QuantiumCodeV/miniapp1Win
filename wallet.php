<?php
session_start();
error_reporting(E_ALL);
ini_set('display_errors', 1);
require_once "backend/config.php";

// Obtenir le statut des tâches de l'utilisateur
$user_id = $_GET['user_id'];
$tasks_result = $mysql->query("SELECT * FROM users WHERE user_id = '$user_id'");
$tasks = $tasks_result->fetch_assoc();
?>

<!DOCTYPE html>
<html lang="fr" class="">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="Description" content="" />

    <link rel="icon" href="favicon.ico" />
    <link rel="stylesheet" href="assets/css/style.css" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@200..800&display=swap" rel="stylesheet">

    <script src="assets/js/jquery-3.6.3.js"></script>
    <script src="assets/js/jquery-ui.min.js"></script>
    <script type="text/javascript" src="//code.jquery.com/jquery-migrate-1.2.1.min.js"></script>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>

    <title>Miniapp</title>
  </head>
  <body>

<section class="main">
  <div class="container">
    <div class="wallet_main">
      <img src="./assets/img/withdraw_image.svg" alt="" class="wallet_image">
      <h1 class="wallet_tittle">RETRAIT DES FONDS</h1>
      <p class="wallet_info">
        <?php
        if ($tasks['zadanie_1'] != '1' || $tasks['zadanie_2'] != '1') {
          echo 'Pour retirer, vous devez compléter <span>2 tâches</span> avec abonnement';
        } else if ($tasks['zadanie_3'] == '0') {
          echo 'Pour retirer, vous devez vous inscrire sur le site';
        } else if ($tasks['zadanie_4'] == '0') {
          echo 'Pour retirer, vous devez faire votre premier dépôt';
        } else if ($tasks['zadanie_5'] == '0') {
          echo 'Pour retirer, vous devez inviter 1 ami';
        }
        ?>
      </p>
      <div class="main_buttons">
        <button class="main_button" onclick="window.location.href='tasks.php'">Aller aux tâches</button>
      </div>
    </div>
  </div>
</section>

<section class="navs">
  <div class="navigations">
    <div class="navigations_content">
      <ul class="navigations_items">
        <li class="navigations_item"><a href="index.php?user_id=<?php echo $user_id; ?>">Accueil</a></li>
        <li class="navigations_item"><a href="tasks.php?user_id=<?php echo $user_id; ?>">Tâches</a></li>
        <li class="navigations_item"><a href="friends.php?user_id=<?php echo $user_id; ?>">Amis</a></li>
        <li class="navigations_item navigations_item_active"><a href="wallet.php?user_id=<?php echo $user_id; ?>">Portefeuille</a></li>
      </ul>
    </div>
  </div>
</section>

    <script>
      // Initialisation de Telegram WebApp
      let tg = window.Telegram.WebApp;
      tg.expand();
      
      // Obtenir les données utilisateur de Telegram
      let user = tg.initDataUnsafe.user;
      console.log('ID utilisateur:', user.id);
      console.log('Prénom:', user.first_name);
      console.log('Nom d\'utilisateur:', user.username);
    </script>
    
    <script src="assets/js/script.js"></script>
  </body>
</html>
