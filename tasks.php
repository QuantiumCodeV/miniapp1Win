<?php
session_start();
error_reporting(E_ALL);
ini_set('display_errors', 1);
require_once "backend/config.php";

// Получаем ссылки из БД
$links_result = $mysql->query("SELECT * FROM links");
$links = $links_result->fetch_assoc();

// Получаем статус заданий пользователя
$user_id = $_COOKIE['user_id'];
$tasks_result = $mysql->query("SELECT * FROM users WHERE user_id = '$user_id'");
$tasks = $tasks_result->fetch_assoc();
?>

<!DOCTYPE html>
<html lang="ru" class="">
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
        <h1 class="tasks_tittle">ВЫПОЛНЕНИЕ ЗАДАНИЙ</h1>
        <div class="tasks_items">
          <div class="tasks_item" id="channel1" onclick="successSubscription('zadanie_1')">
            <div class="tasks_item_content">
              <p class="tasks_item_tittle">Подписаться на первый канал</p>
              <p class="tasks_item_price" <?php if($tasks['zadanie_1'] == '1') echo 'style="display:none"'; ?>>1000₣</p>
              <img src="./assets/img/tasks_accept.svg" alt="" class="tasks_item_accept" 
                <?php if($tasks['zadanie_1'] != '1') echo 'style="display:none"'; ?>
                data-link="<?php echo $links['first_channel']; ?>" />
            </div>
          </div>

          <div class="tasks_item" id="channel2" onclick="successSubscription('zadanie_2')">
            <div class="tasks_item_content">
              <p class="tasks_item_tittle">Подписаться на второй канал</p>
              <p class="tasks_item_price" <?php if($tasks['zadanie_2'] == '1') echo 'style="display:none"'; ?>>1000₣</p>
              <img src="./assets/img/tasks_accept.svg" alt="" class="tasks_item_accept"
                <?php if($tasks['zadanie_2'] != '1') echo 'style="display:none"'; ?>
                data-link="<?php echo $links['second_channel']; ?>" />
            </div>
          </div>

          <div class="tasks_item" id="1win" onclick="window.location.href='<?php echo $links['win_link']; ?>'">
            <div class="tasks_item_content">
              <p class="tasks_item_tittle">Регистрация на сайте</p>
              <p class="tasks_item_price" <?php if($tasks['zadanie_3'] == '1') echo 'style="display:none"'; ?>>1000₣</p>
              <img src="./assets/img/tasks_accept.svg" alt="" class="tasks_item_accept"
                <?php if($tasks['zadanie_3'] != '1') echo 'style="display:none"'; ?> />
            </div>
          </div>

          <div class="tasks_item" id="deposit">
            <div class="tasks_item_content">
              <p class="tasks_item_tittle">Сделать депозит</p>
              <p class="tasks_item_price" <?php if($tasks['zadanie_4'] == '1') echo 'style="display:none"'; ?>>3000₣</p>
              <img src="./assets/img/tasks_accept.svg" alt="" class="tasks_item_accept"
                <?php if($tasks['zadanie_4'] != '1') echo 'style="display:none"'; ?> />
            </div>
          </div>

          <div class="tasks_item" id="invite">
            <div class="tasks_item_content">
              <p class="tasks_item_tittle">Пригласить друга</p>
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
                    if(zadanie == "zadanie_2") {
                      window.location.href = $("#channel2").find(".tasks_item_accept").attr("data-link");
                    }
                  }
                }
              });
            }
          </script>
        </div>

        <div class="tasks_promocode">
          <p class="tasks_promocode_tittle">Promocode</p>
          <input type="text" placeholder="Enter poromocode" class="tasks_promocode_input"/>
          <p class="tasks_promocode_error" style="display: none"></p>
          <p class="tasks_promocode_success" style="display: none"></p>

          <button class="tasks_promocode_button" onclick="activatePromo()">Применить</button>

          <script>
            async function activatePromo() {
              let promoCode = document.querySelector(".tasks_promocode_input").value;

              if(promoCode == "") {
                $(".tasks_promocode_error").text("Введите промокод").show();
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
            <li class="navigations_item"><a href="index.php">Главная</a></li>
            <li class="navigations_item navigations_item_active">
              <a href="tasks.php">Задания</a>
            </li>
            <li class="navigations_item"><a href="friends.php">Друзья</a></li>
            <li class="navigations_item"><a href="wallet.php">Кошелек</a></li>
          </ul>
        </div>
      </div>
    </section>

    <script>
      // Инициализация Telegram WebApp
      let tg = window.Telegram.WebApp;
      tg.expand();

      // Получаем данные пользователя из Telegram
      let user = tg.initDataUnsafe.user;
      console.log("ID пользователя:", user.id);
      console.log("Имя пользователя:", user.first_name);
      console.log("Юзернейм:", user.username);
    </script>

    <script src="assets/js/script.js"></script>
  </body>
</html>
