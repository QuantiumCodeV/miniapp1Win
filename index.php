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

  <div class="modal_gift" id="modal_gift">
    <div class="modal_overlay"></div>
    <div class="modal_gift_rect">
      <img src="./assets/img/close.svg" alt="" class="modal_close" id="modal_close">
      <div class="modal_gift_rect_content">
        <p class="modal_gift_tittle">Бонус за приглашения</p>
        <ul class="modal_gift_texts">
          <li class="modal_gift_text"><span>3000 ₣</span> за <span>10</span> приглашенных друзей</li>
          <li class="modal_gift_text"><span>6000 ₣</span> за <span>20</span> приглашенных друзей</li>
          <li class="modal_gift_text"><span>15000₣</span> за <span>40</span> приглашенных друзей</li>
        </ul>
        <p class="modal_gift_subtittle">Выпускайте видеоролики с нашим ботом и получайте дополнительные призы</p>
        <ul class="modal_gift_videos">
          <li class="modal_gift_video"><span>5000₣</span> если ваше видео набрало 1000 просмотров</li>
          <li class="modal_gift_video"><span>20000₣</span> если ваше видео набрало более 5 тысяч просмотров</li>
          <li class="modal_gift_video"><span>100 000₣</span> если ваше видео набрало более 20 тысяч просмотров</li>
        </ul>
        <p class="modal_gift_video_text">Для получения вознаграждения, пришлите ссылку вашего аккаунта и скриншот где видно сколько ваше видео набрало просмотров"
        </p>
      </div>
    </div>
  </div>

  <div class="modal_help" id="modal_help">
    <div class="modal_overlay"></div>
    <div class="modal_help_rect">
      <img src="./assets/img/close.svg" alt="" class="modal_close" id="modal_close">
      <div class="modal_gift_rect_content">
        <p class="modal_help_rect_tittle">Этот бот создан для того, чтобы помочь вам зарабатывать, приглашая своих друзей. Заработок в системе основан на простой и понятной модели: чем больше людей вы пригласите, тем больше вы сможете заработать.
        </p>
        <p class="modal_help_rect_subtittle"><span>1</span> приглашенный друг = <span>N сумма</span> (зависит от уровня пользователя)</p>
        <ul class="modal_help_rect_items">
          <li class="modal_help_rect_item_text"><span>1</span> уровень - базовый уровень дается с самого начала</li>
          <li class="modal_help_rect_item_text"><span>2</span> уровень за <span>1</span> друга дается <span>2000₣</span></li>
          <li class="modal_help_rect_item_text"><span>3</span> уровень за <span>1</span> друга дается <span>5000₣</span></li>
          <li class="modal_help_rect_item_text"><span>4</span> уровень за <span>1</span> друга дается <span>6000₣</span></li>
          <li class="modal_help_rect_item_text"><span>5</span> уровень за <span>1</span> друга дается <span>10000₣</span></li>
        </ul>
        <p class="modal_help_rect_bottom">Но создается вопрос, откуда берутся деньги? Ответ: Все выплаты происходят за счет наших партнеров, которые спонсируют проект, что делает его устойчивым и надежным.</p>
      </div>
    </div>
  </div>

  <section class="main">
    <div class="container">
      <img src="./assets/img/help.svg" alt="" class="main_help" id="openhelp">
      <div class="main_center">
        <h2 class="main_tittle">ВАШ БАЛАНС</h2>
        <?php
        // Start session before any output
        error_reporting(E_ALL);
        ini_set('display_errors', 1);
        include "backend/config.php";

        // Если user_id еще не сохранен в сессии 
        if (!isset($_COOKIE['user_id'])) {
            $user_id = isset($_GET['user_id']) ? $_GET['user_id'] : null;
            if ($user_id) {
                setcookie('user_id', $user_id, time() + (86400 * 30), "/"); // Cookie на 30 дней
            }
        }

        if (isset($_COOKIE['user_id'])) {
            $user_id = $_COOKIE['user_id'];
            
            // Защита от SQL-инъекций
            $user_id = $mysql->real_escape_string($user_id);

            // Проверяем существование пользователя
            $result = $mysql->query("SELECT balance FROM users WHERE user_id = '$user_id'")->fetch_assoc();

            if ($result) {
                echo '<h1 class="main_balance">' . htmlspecialchars($result['balance']) . '₣</h1>';
            } else {
                // Если пользователь не найден, создаем запись
                $mysql->query("INSERT INTO users (user_id) VALUES ('$user_id')");
                echo '<h1 class="main_balance">0₣</h1>';
            }
        } else {
            echo '<h1 class="main_balance">0₣</h1>';
        }
        ?>
        <h3 class="main_sutittle">Приглашайте друзей и получайте 1000₣ за каждого друга</h3>
        <div class="main_buttons">
          <a class="main_button" id="inviteBtn" href="https://t.me/share/url?url=https://t.me/fasdfadf_bot?start=<?php echo $user_id; ?>&text=Присоединяйся по моей ссылке и получи бонус 1000₣ на старте! 🔥">Пригласить друзей</a>
          <img src="./assets/img/copy.svg" alt="" class="main_copy" id="copyBtn" onclick="copyLink()">
        </div>
      </div>
    </div>
  </section>

  <section class="navs">
    <img src="./assets/img/present.png" alt="" class="navs_image" id="opengift">
    <div class="navigations">
      <div class="navigations_content">
        <ul class="navigations_items">
          <li class="navigations_item navigations_item_active"><a href="index.php">Главная</a></li>
          <li class="navigations_item"><a href="tasks.html">Задания</a></li>
          <li class="navigations_item"><a href="friends.html">Друзья</a></li>
          <li class="navigations_item"><a href="wallet.html">Кошелек</a></li>
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
    localStorage.setItem('user_id', user.id);

    function copyLink() {
      let link = "https://t.me/fasdfadf_bot?start=" + localStorage.getItem('user_id');
      navigator.clipboard.writeText(link);
    }
  </script>

  <script src="assets/js/script.js"></script>
</body>

</html>