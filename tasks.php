<?php
session_start();
error_reporting(E_ALL);
ini_set('display_errors', 1);
require_once "backend/config.php";

// Obtenir les liens de la base de données
$links_result = $mysql->query("SELECT * FROM links");
$links = $links_result->fetch_assoc();

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
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@200..800&display=swap" rel="stylesheet"/>
    
    <script src="assets/js/jquery-3.6.3.js"></script>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>

    <title>Miniapp</title>
  </head>
  <body>
    <section class="main">
      <div class="container">
        <img src="./assets/img/tasks_image.svg" alt="" class="tasks_image" />
        <h1 class="tasks_tittle">RÉALISATION DES TÂCHES</h1>
        <div class="tasks_items">
          <div class="tasks_item" id="channel1" onclick="successSubscription('zadanie_1')">
            <div class="tasks_item_content">
              <p class="tasks_item_tittle">S'abonner à la première chaîne</p>
              <p class="tasks_item_price" <?php if($tasks['zadanie_1'] == '1') echo 'style="display:none"'; ?>>1000₣</p>
              <img src="./assets/img/tasks_accept.svg" alt="" class="tasks_item_accept" 
                <?php if($tasks['zadanie_1'] != '1') echo 'style="display:none"'; ?>
                data-link="<?php echo $links['first_channel']; ?>" />
            </div>
          </div>

          <div class="tasks_item" id="channel2" onclick="successSubscription('zadanie_2')">
            <div class="tasks_item_content">
              <p class="tasks_item_tittle">S'abonner à la deuxième chaîne</p>
              <p class="tasks_item_price" <?php if($tasks['zadanie_2'] == '1') echo 'style="display:none"'; ?>>1000₣</p>
              <img src="./assets/img/tasks_accept.svg" alt="" class="tasks_item_accept"
                <?php if($tasks['zadanie_2'] != '1') echo 'style="display:none"'; ?>
                data-link="<?php echo $links['second_channel']; ?>" />
            </div>
          </div>

          <div class="tasks_item" id="1win" onclick="window.location.href='<?php echo $links['win_link']; ?><?php echo $user_id; ?>'">
            <div class="tasks_item_content">
              <p class="tasks_item_tittle">Inscription sur le site</p>
              <p class="tasks_item_price" <?php if($tasks['zadanie_3'] == '1') echo 'style="display:none"'; ?>>1000₣</p>
              <img src="./assets/img/tasks_accept.svg" alt="" class="tasks_item_accept"
                <?php if($tasks['zadanie_3'] != '1') echo 'style="display:none"'; ?> />
            </div>
          </div>

          <div class="tasks_item" id="deposit">
            <div class="tasks_item_content">
              <p class="tasks_item_tittle">Faire un dépôt</p>
              <p class="tasks_item_price" <?php if($tasks['zadanie_4'] == '1') echo 'style="display:none"'; ?>>3000₣</p>
              <img src="./assets/img/tasks_accept.svg" alt="" class="tasks_item_accept"
                <?php if($tasks['zadanie_4'] != '1') echo 'style="display:none"'; ?> />
            </div>
          </div>

          <div class="tasks_item" id="invite">
            <div class="tasks_item_content">
              <p class="tasks_item_tittle">Inviter un ami</p>
              <p class="tasks_item_price" <?php if($tasks['zadanie_5'] == '1') echo 'style="display:none"'; ?>>1000₣</p>
              <img src="./assets/img/tasks_accept.svg" alt="" class="tasks_item_accept"
                <?php if($tasks['zadanie_5'] != '1') echo 'style="display:none"'; ?> />
            </div>
          </div>

          <script>
            function successSubscription(zadanie) {
              $.ajax({
                url: "/backend/success_subscriptions.php",
                method: "POST", 
                data: {
                  user_id: localStorage.getItem("user_id"),
                  zadanie: zadanie
                },
                success: function(response) {
                  var responseJSON = JSON.parse(response);
                  if(responseJSON.success) {
                    if(zadanie == "zadanie_1") {
                      window.location.href = $("#channel1").find(".tasks_item_accept").attr("data-link");
                    }
                    if(zadanie == "zadanie_2") {ы
                      window.location.href = $("#channel2").find(".tasks_item_accept").attr("data-link");
                    }
                  }
                }
              });
            }
          </script>
        </div>

        <div class="tasks_promocode">
          <p class="tasks_promocode_tittle">Code promo</p>
          <input type="text" placeholder="Entrez le code promo" class="tasks_promocode_input"/>
          <p class="tasks_promocode_error" style="display: none"></p>
          <p class="tasks_promocode_success" style="display: none"></p>

          <button class="tasks_promocode_button" onclick="activatePromo()">Appliquer</button>

          <script>
            async function activatePromo() {
              let promoCode = document.querySelector(".tasks_promocode_input").value;

              if(promoCode == "") {
                $(".tasks_promocode_error").text("Entrez le code promo").show();
                $(".tasks_promocode_success").hide();
                setTimeout(() => {
                  $(".tasks_promocode_error").hide();
                }, 3000);
                return;
              }

              $.ajax({
                url: "/backend/activate_promo.php",
                method: "POST",
                data: {
                  promo: promoCode,
                  user_id: localStorage.getItem("user_id")
                },
                success: function(response) {
                  var responseJSON = JSON.parse(response);
                  if(responseJSON.error) {
                    $(".tasks_promocode_error").text(responseJSON.error).show();
                    $(".tasks_promocode_success").hide();
                    setTimeout(() => {
                      $(".tasks_promocode_error").hide();
                    }, 3000);
                  } else {
                    $(".tasks_promocode_success").text(responseJSON.success).show();
                    $(".tasks_promocode_error").hide();
                    setTimeout(() => {
                      $(".tasks_promocode_success").hide();
                    }, 3000);
                  }
                }
              });
            }
          </script>
        </div>
      </div>
    </section>

    <section class="navs">
      <div class="navigations">
        <div class="navigations_content">
          <ul class="navigations_items">
            <li class="navigations_item"><a href="index.php?user_id=<?php echo $user_id; ?>">Accueil</a></li>
            <li class="navigations_item navigations_item_active">
              <a href="tasks.php?user_id=<?php echo $user_id; ?>">Tâches</a>
            </li>
            <li class="navigations_item"><a href="friends.php?user_id=<?php echo $user_id; ?>">Amis</a></li>
            <li class="navigations_item"><a href="wallet.php?user_id=<?php echo $user_id; ?>">Portefeuille</a></li>
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
      console.log("ID utilisateur:", user.id);
      console.log("Prénom:", user.first_name);
      console.log("Nom d'utilisateur:", user.username);
    </script>

    <script src="assets/js/script.js"></script>
  </body>
</html>
