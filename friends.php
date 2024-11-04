<?php
session_start();
error_reporting(E_ALL);
ini_set('display_errors', 1);
require_once "backend/config.php";

// Получаем статус заданий пользователя
$user_id = $_COOKIE['user_id'];

// Получаем друзей из базы данных
$result = $mysql->query("SELECT * FROM users WHERE referrer_id = '$user_id'");
$friends = array();
$level2 = 0;
$level3 = 0; 
$level4 = 0;
$level5 = 0;
$total = 0;

while ($row = $result->fetch_assoc()) {
    $friends[] = $row;
    $total++;
    
    switch($row['level']) {
        case "2":
            $level2++;
            break;
        case "3":
            $level3++;
            break;
        case "4":
            $level4++;
            break;
        case "5":
            $level5++;
            break;
    }
}
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
        <p class="friends_info">ВСЕГО ВЫ ПРИГЛАСИЛИ: <br> <span id="friendsTotal"><?php echo $total; ?> ДРУЗЕЙ</span> </p>
        <div class="friends_items">
          <p class="friends_item">ДРУЗЬЯ <span>2</span> УРОВНЯ: <span id="friends2"><?php echo $level2; ?></span></p>
          <p class="friends_item">ДРУЗЬЯ <span>3</span> УРОВНЯ: <span id="friends3"><?php echo $level3; ?></span></p>
          <p class="friends_item">ДРУЗЬЯ <span>4</span> УРОВНЯ: <span id="friends4"><?php echo $level4; ?></span></p>
          <p class="friends_item">ДРУЗЬЯ <span>5</span> УРОВНЯ: <span id="friends5"><?php echo $level5; ?></span></p>
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
    let tg = window.Telegram.WebApp;
    tg.expand();

    function copyLink() {
      let link = "https://t.me/fasdfadf_bot?start=<?php echo $user_id; ?>";
      navigator.clipboard.writeText(link);
    }
  </script>

  <script src="assets/js/script.js"></script>
</body>

</html>