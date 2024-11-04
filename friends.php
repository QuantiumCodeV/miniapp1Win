<?php
session_start();
error_reporting(E_ALL);
ini_set('display_errors', 1);
require_once "backend/config.php";

// Получаем статус заданий пользователя
$user_id = $_COOKIE['user_id'];
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

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@200..800&display=swap" rel="stylesheet">

  <script src="assets/js/jquery-3.6.3.js"></script>
  <script src="assets/js/jquery-ui.min.js"></script>
  <script
    type="text/javascript"
    src="//code.jquery.com/jquery-migrate-1.2.1.min.js"></script>
  <script src="https://telegram.org/js/telegram-web-app.js"></script>

  <title>Miniapp</title>
</head>

<body>


  <section class="main">
    <div class="container">
      <div class="friends_main">
        <img src="./assets/img/friends_image.svg" alt="" class="friends_image">
        <h1 class="friends_tittle">ПРИГЛАСИТЕ ДРУЗЕЙ</h1>
        <p class="friends_info">ВСЕГО ВЫ ПРИГЛАСИЛИ: <br> <span id="friendsTotal">0 ДРУЗЕЙ</span> </p>
        <div class="friends_items">
          <p class="friends_item">ДРУЗЬЯ <span>2</span> УРОВНЯ: <span id="friends2">0</span></p>
          <p class="friends_item">ДРУЗЬЯ <span>3</span> УРОВНЯ: <span id="friends3">0</span></p>
          <p class="friends_item">ДРУЗЬЯ <span>4</span> УРОВНЯ: <span id="friends4">0</span></p>
          <p class="friends_item">ДРУЗЬЯ <span>5</span> УРОВНЯ: <span id="friends5">5</span></p>
        </div>
        <div class="main_buttons">
          <a class="main_button" href="https://t.me/share/url?url=https://t.me/fasdfadf_bot?start=<?php echo $user_id; ?>&text=Присоединяйся по моей ссылке и получи бонус 1000₣ на старте! 🔥">Пригласить друзей</a>
          <img src="./assets/img/copy.svg" alt="" class="main_copy" onclick="copyLink()">
        </div>
      </div>
    </div>
  </section>

  <section class="navs">
    <div class="navigations">
      <div class="navigations_content">
        <ul class="navigations_items">
          <li class="navigations_item"><a href="index.php">Главная</a></li>
          <li class="navigations_item"><a href="tasks.php">Задания</a></li>
          <li class="navigations_item navigations_item_active"><a href="friends.php">Друзья</a></li>
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
    console.log('ID пользователя:', user.id);
    console.log('Имя пользователя:', user.first_name);
    console.log('Юзернейм:', user.username);

    function getFriends() {
      // Проверяем наличие user_id в localStorage
      const userId = localStorage.getItem('user_id');
      if (!userId) {
        console.error('ID пользователя не найден');
        return;
      }

      $.ajax({
        url: "/backend/get_friends.php",
        method: "POST",
        data: {
          user_id: userId
        },
        success: function(response) {
          try {
            if (!response) {
              throw new Error('Пустой ответ от сервера');
            }

            let friends = JSON.parse(response);

            // Подсчет друзей по уровням
            let level2 = 0,
              level3 = 0,
              level4 = 0,
              level5 = 0;

            friends.forEach(friend => {
              if (friend.level == "2") level2++;
              if (friend.level == "3") level3++;
              if (friend.level == "4") level4++;
              if (friend.level == "5") level5++;
            });

            // Обновляем DOM
            $("#friendsTotal").text(friends.length + " ДРУЗЕЙ");
            $("#friends2").text(level2);
            $("#friends3").text(level3);
            $("#friends4").text(level4);
            $("#friends5").text(level5);

          } catch (error) {
            console.error('Ошибка при обработке данных:', error);
          }
        },
        error: function(xhr, status, error) {
          console.error('Ошибка запроса:', error);
        }
      });
    }

    getFriends();


    function copyLink() {
      let link = "https://t.me/fasdfadf_bot?start=" + localStorage.getItem('user_id');
      navigator.clipboard.writeText(link);
    }
  </script>

  <script src="assets/js/script.js"></script>
</body>

</html>