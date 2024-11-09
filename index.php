<?php
// Démarrer la session avant toute sortie
session_start();
error_reporting(E_ALL);
ini_set('display_errors', 1);
require_once "backend/config.php";
// Si user_id n'est pas encore enregistré dans les cookies
$user_id = $_GET['user_id'];
$user = $mysql->query("SELECT * FROM users WHERE user_id = '$user_id'")->fetch_assoc();

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
  <script
    type="text/javascript"
    src="//code.jquery.com/jquery-migrate-1.2.1.min.js"></script>
  <script src="https://telegram.org/js/telegram-web-app.js"></script>

  <title>Mini-application</title>
</head>

<body>

  <div class="modal_gift" id="modal_gift">
    <div class="modal_overlay"></div>
    <div class="modal_gift_rect">
      <img src="./assets/img/close.svg" alt="" class="modal_close" id="modal_close">
      <div class="modal_gift_rect_content">
        <p class="modal_gift_tittle">Bonus pour les invitations</p>
        <ul class="modal_gift_texts">
          <li class="modal_gift_text"><span>3000 ₣</span> pour <span>10</span> amis invités</li>
          <li class="modal_gift_text"><span>6000 ₣</span> pour <span>20</span> amis invités</li>
          <li class="modal_gift_text"><span>15000₣</span> pour <span>40</span> amis invités</li>
        </ul>
        <p class="modal_gift_subtittle">Publiez des vidéos avec notre bot et recevez des prix supplémentaires</p>
        <ul class="modal_gift_videos">
          <li class="modal_gift_video"><span>5000₣</span> si votre vidéo atteint 1000 vues</li>
          <li class="modal_gift_video"><span>20000₣</span> si votre vidéo atteint plus de 5 mille vues</li>
          <li class="modal_gift_video"><span>100 000₣</span> si votre vidéo atteint plus de 20 mille vues</li>
        </ul>
        <p class="modal_gift_video_text">Pour recevoir votre récompense, envoyez le lien de votre compte et une capture d'écran montrant le nombre de vues de votre vidéo"
        </p>
        <a class="modal_gift_button" href="<?= $support_link ?>">Support</a>
        <style>
          .modal_gift_button {
            color: #fff;
            text-align: center;
            font-family: "Manrope", sans-serif;
            outline: none;
            border: none;
            cursor: pointer;
            transition: all 0.5s;
            font-size: 25px;
            font-style: normal;
            font-weight: 600;
            line-height: normal;
            padding: 16px 50px;
            border-radius: 15px;
            background: #00c9ff;
            margin-top: 20px;
          }
        </style>
      </div>
    </div>
  </div>

  <div class="modal_help" id="modal_help">
    <div class="modal_overlay"></div>
    <div class="modal_help_rect">
      <img src="./assets/img/close.svg" alt="" class="modal_close" id="modal_close">
      <div class="modal_gift_rect_content">
        <p class="modal_help_rect_tittle">Ce bot est créé pour vous aider à gagner de l'argent en invitant vos amis. Les gains dans le système sont basés sur un modèle simple et compréhensible : plus vous invitez de personnes, plus vous pouvez gagner.
        </p>
        <p class="modal_help_rect_subtittle"><span>1</span> ami invité = <span><?php if($user['level'] == 1) echo "1000₣"; else if($user['level'] == 2) echo "2000₣"; else if($user['level'] == 3) echo "5000₣"; else if($user['level'] == 4) echo "6000₣"; else if($user['level'] == 5) echo "10000₣"; ?></span> (dépend du niveau de l'utilisateur)</p>
        <ul class="modal_help_rect_items">
          <li class="modal_help_rect_item_text"><span>1</span> niveau - niveau de base donné dès le début</li>
          <li class="modal_help_rect_item_text"><span>2</span> niveau pour <span>1</span> ami donne <span>2000₣</span></li>
          <li class="modal_help_rect_item_text"><span>3</span> niveau pour <span>1</span> ami donne <span>5000₣</span></li>
          <li class="modal_help_rect_item_text"><span>4</span> niveau pour <span>1</span> ami donne <span>6000₣</span></li>
          <li class="modal_help_rect_item_text"><span>5</span> niveau pour <span>1</span> ami donne <span>10000₣</span></li>
        </ul>
        <p class="modal_help_rect_bottom">Mais la question se pose, d'où vient l'argent ? Réponse : Tous les paiements sont effectués par nos partenaires qui sponsorisent le projet, ce qui le rend stable et fiable.</p>
      </div>
    </div>
  </div>

  <section class="main">
    <div class="container">
      <img src="./assets/img/help.svg" alt="" class="main_help" id="openhelp">
      <div class="main_center">
        <h2 class="main_tittle">VOTRE SOLDE</h2>
        <?php
        // Vérifier la présence du cookie
        if (isset($user_id)) {

          // Protection contre les injections SQL
          $user_id = $mysql->real_escape_string($user_id);

          // Vérifier l'existence de l'utilisateur
          $result = $mysql->query("SELECT balance FROM users WHERE user_id = '$user_id'")->fetch_assoc();

          if ($result) {
            echo '<h1 class="main_balance">' . htmlspecialchars($result['balance']) . '₣</h1>';
          } else {
            // Si l'utilisateur n'est pas trouvé, créer une entrée
            $mysql->query("INSERT INTO users (user_id) VALUES ('$user_id')");
            echo '<h1 class="main_balance">0₣</h1>';
          }
        } else {
          echo '<h1 class="main_balance">0₣</h1>';
        }
        ?>
        <h3 class="main_sutittle">Invitez des amis et recevez 1000₣ pour chaque ami</h3>
        <div class="main_buttons">
          <a class="main_button" id="inviteBtn" href="https://t.me/share/url?url=https://t.me/<?= $bot_username ?>?start=<?php echo $user_id; ?>&text=Rejoignez avec mon lien et obtenez un bonus de démarrage de 1000₣! 🔥">Inviter des amis</a>
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
          <li class="navigations_item navigations_item_active"><a href="index.php?user_id=<?php echo $user_id; ?>">Accueil</a></li>
          <li class="navigations_item"><a href="tasks.php?user_id=<?php echo $user_id; ?>">Tâches</a></li>
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

    // Obtenir les données de l'utilisateur de Telegram
    let user = tg.initDataUnsafe.user;
    console.log('ID utilisateur:', user.id);
    console.log('Nom utilisateur:', user.first_name);
    console.log('Nom d\'utilisateur:', user.username);
    localStorage.setItem('user_id', user.id);
    // Проверяем наличие user_id в URL
    let urlParams = new URLSearchParams(window.location.search);
    if (!urlParams.has('user_id')) {
        // Если user_id отсутствует, добавляем его из данных пользователя Telegram и перезагружаем страницу
        let newUrl = window.location.pathname + '?user_id=' + user.id;
        window.location.href = newUrl;
    }

    function copyLink() {
      let link = "https://t.me/<?= $bot_username ?>?start=" + localStorage.getItem('user_id');
      try {
        // Создаем временный элемент input
        const tempInput = document.createElement('input');
        tempInput.value = link;
        document.body.appendChild(tempInput);
        // Выделяем и копируем текст
        tempInput.select();
        document.execCommand('copy');
        // Удаляем временный элемент
        document.body.removeChild(tempInput);
      } catch(err) {
        console.error('Ошибка при копировании:', err);
      }
    }
  </script>

  <script src="assets/js/script.js"></script>
</body>

</html>