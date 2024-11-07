<?php
session_start();
error_reporting(E_ALL);
ini_set('display_errors', 1);
require_once "backend/config.php";

// Obtenir le statut des tâches de l'utilisateur
$user_id = $_GET['user_id'];

// Obtenir les amis de la base de données
$result = $mysql->prepare("SELECT * FROM users WHERE referrer_id = ? AND level >= 2");
$result->bind_param("s", $user_id);
$result->execute();
$result = $result->get_result();
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

  <title>Miniapp</title>
</head>

<body>

  <section class="main">
    <div class="container">
      <div class="friends_main">
        <img src="./assets/img/friends_image.svg" alt="" class="friends_image">
        <h1 class="friends_tittle">INVITEZ VOS AMIS</h1>
        <p class="friends_info">TOTAL DES INVITATIONS: <br> <span id="friendsTotal"><?php echo $total; ?> AMIS</span> </p>
        <div class="friends_items">
          <p class="friends_item">AMIS NIVEAU <span>2</span>: <span id="friends2"><?php echo $level2; ?></span></p>
          <p class="friends_item">AMIS NIVEAU <span>3</span>: <span id="friends3"><?php echo $level3; ?></span></p>
          <p class="friends_item">AMIS NIVEAU <span>4</span>: <span id="friends4"><?php echo $level4; ?></span></p>
          <p class="friends_item">AMIS NIVEAU <span>5</span>: <span id="friends5"><?php echo $level5; ?></span></p>
        </div>
        <div class="main_buttons">
          <a class="main_button" href="https://t.me/share/url?url=https://t.me/fasdfadf_bot?start=<?php echo $user_id; ?>&text=Rejoignez avec mon lien et obtenez un bonus de 1000₣ au départ! 🔥">Inviter des amis</a>
          <img src="./assets/img/copy.svg" alt="" class="main_copy" onclick="copyLink()">
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
          <li class="navigations_item navigations_item_active"><a href="friends.php?user_id=<?php echo $user_id; ?>">Amis</a></li>
          <li class="navigations_item"><a href="wallet.php?user_id=<?php echo $user_id; ?>">Portefeuille</a></li>
        </ul>
      </div>
    </div>
  </section>

  <script>
    let tg = window.Telegram.WebApp;
    tg.expand();

    function copyLink() {
      let link = "https://t.me/fasdfadf_bot?start=<?php echo $user_id; ?>";
      
      // Create temporary textarea element
      const textarea = document.createElement('textarea');
      textarea.value = link;
      document.body.appendChild(textarea);
      
      // Select and copy text
      textarea.select();
      document.execCommand('copy');
      
      // Remove temporary element
      document.body.removeChild(textarea);
    }
  </script>

  <script src="assets/js/script.js"></script>
</body>

</html>