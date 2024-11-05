from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import asyncio
from typing import Dict, List, Union
from datetime import datetime
import mysql.connector
import json

# États pour FSM
class BroadcastStates(StatesGroup):
    choosing_recipients = State()
    entering_text = State()
    adding_media = State()
    adding_button = State()
    confirming = State()

class PromoStates(StatesGroup):
    entering_code = State()
    entering_amount = State()
    entering_uses = State()
    confirming = State()

# Initialisation du bot et du dispatcher
bot = Bot(token="7666407425:AAF623qqMheTU-SD_zTbFqmy8w2i_WHGAFw")
dp = Dispatcher()
router = Router()
# Définir l'ID de l'administrateur
ADMIN_ID = 5685109533  # Remplacez par votre ID d'administrateur réel
FIRST_CHANNEL_LINK = "https://t.me/+cdlYMb4VnbgzZDVi"
SECOND_CHANNEL_LINK = "https://t.me/+1uS2fYpUS4dmNWI6"
WIN_LINK = "https://1wwwl.com/?open=register"

# Création de la base de données
def init_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="miniapp",
        password="72Merasardtfy_",
        database="miniapp"
    )
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id BIGINT PRIMARY KEY,
                  username VARCHAR(255),
                  level INT DEFAULT 1,
                  balance INT DEFAULT 0,
                  invited_users INT DEFAULT 0,
                  referrer_id BIGINT,
                  join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  zadanie_1 BOOLEAN DEFAULT FALSE,
                  zadanie_2 BOOLEAN DEFAULT FALSE,
                  zadanie_3 BOOLEAN DEFAULT FALSE,
                  zadanie_4 BOOLEAN DEFAULT FALSE,
                  zadanie_5 BOOLEAN DEFAULT FALSE)''')
                  
    cursor.execute('''CREATE TABLE IF NOT EXISTS promo_codes
                 (code VARCHAR(255) PRIMARY KEY,
                  amount INT,
                  max_uses INT,
                  current_uses INT DEFAULT 0,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
                  
    cursor.execute('''CREATE TABLE IF NOT EXISTS promo_uses
                 (user_id BIGINT,
                  code VARCHAR(255),
                  used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY(user_id) REFERENCES users(user_id),
                  FOREIGN KEY(code) REFERENCES promo_codes(code),
                  PRIMARY KEY(user_id, code))''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS links
                 (id INT PRIMARY KEY AUTO_INCREMENT,
                  first_channel VARCHAR(255) DEFAULT %s,
                  second_channel VARCHAR(255) DEFAULT %s,
                  win_link VARCHAR(255) DEFAULT %s)''', (FIRST_CHANNEL_LINK, SECOND_CHANNEL_LINK, WIN_LINK))
    
    cursor.execute('INSERT IGNORE INTO links (id, first_channel, second_channel, win_link) VALUES (1, %s, %s, %s)',
                  (FIRST_CHANNEL_LINK, SECOND_CHANNEL_LINK, WIN_LINK))
    
    conn.commit()
    cursor.close()
    conn.close()


# Обработчик постов в канале
@router.channel_post()
async def channel_post(message: Message):
    conn = mysql.connector.connect(
        host="localhost",
        user="miniapp",
        password="72Merasardtfy_", 
        database="miniapp"
    )
    cursor = conn.cursor()
    
    # Проверяем формат сообщения "1вин:регистрация:код"
    text = message.text
    if text and ":" in text:
        parts = text.split(":")
        if len(parts) == 3 and parts[0].lower() == "1вин" and parts[1].lower() == "регистрация":
            reg_code = parts[2].strip()
            
            # Отправляем ответное сообщение
            response = f"✅ Регистрация подтверждена\nВаш код: {reg_code}"
           
            # Публикуем пост в канал
            await message.bot.send_message(
                chat_id=message.chat.id,
                text=f"🎉 Новая регистрация!\nКод: {reg_code}\n\nПрисоединяйтесь к нам!"
            )
            
    cursor.close()
    conn.close()


# Gestionnaire de liste des codes promo
@router.message(Command("promos"))
async def list_promos(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
        
    conn = mysql.connector.connect(
        host="localhost",
        user="miniapp",
        password="72Merasardtfy_",
        database="miniapp"
    )
    c = conn.cursor()
    c.execute('SELECT code FROM promo_codes')
    promos = c.fetchall()
    conn.close()
    
    kb = InlineKeyboardBuilder()
    for promo in promos:
        kb.add(InlineKeyboardButton(
            text=promo[0],
            callback_data=f"promo_info_{promo[0]}"
        ))
    kb.adjust(1)
    
    await message.answer("Codes promo:", reply_markup=kb.as_markup())

@router.callback_query(lambda c: c.data.startswith("promo_info_"))
async def show_promo_info(callback: CallbackQuery):
    code = callback.data.split("_")[2]
    
    conn = mysql.connector.connect(
        host="localhost",
        user="miniapp",
        password="72Merasardtfy_",
        database="miniapp"
    )
    c = conn.cursor()
    c.execute('''SELECT code, amount, max_uses, current_uses, created_at 
                 FROM promo_codes WHERE code = %s''', (code,))
    promo = c.fetchone()
    conn.close()
    
    if not promo:
        await callback.answer("Code promo non trouvé")
        return
        
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="🗑 Supprimer",
        callback_data=f"delete_promo_{code}"
    ))
    kb.add(InlineKeyboardButton(
        text="◀️ Retour",
        callback_data="back_to_promos"
    ))
    kb.adjust(1)
    
    info_text = f"""
Informations sur le code promo:
Code: {promo[0]}
Montant: {promo[1]}₣
Utilisations max: {promo[2]}
Utilisé: {promo[3]}
Créé le: {promo[4]}
"""
    
    await callback.message.edit_text(
        info_text,
        reply_markup=kb.as_markup()
    )

@router.callback_query(lambda c: c.data.startswith("delete_promo_"))
async def delete_promo(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Vous n'avez pas les droits pour supprimer les codes promo")
        return
        
    code = callback.data.split("_")[2]
    
    conn = mysql.connector.connect(
        host="localhost",
        user="miniapp",
        password="72Merasardtfy_",
        database="miniapp"
    )
    c = conn.cursor()
    
    # Vérifier l'existence du code promo
    c.execute('SELECT code FROM promo_codes WHERE code = %s', (code,))
    if not c.fetchone():
        await callback.answer("Code promo non trouvé")
        conn.close()
        return
        
    # Supprimer le code promo
    c.execute('DELETE FROM promo_codes WHERE code = %s', (code,))
    conn.commit()
    conn.close()
    
    await callback.answer("✅ Code promo supprimé avec succès")
    
    # Obtenir la liste mise à jour des codes promo
    conn = mysql.connector.connect(
        host="localhost",
        user="miniapp",
        password="72Merasardtfy_",
        database="miniapp"
    )
    c = conn.cursor()
    c.execute('SELECT code FROM promo_codes')
    promos = c.fetchall()
    conn.close()
    
    kb = InlineKeyboardBuilder()
    for promo in promos:
        kb.add(InlineKeyboardButton(
            text=promo[0],
            callback_data=f"promo_info_{promo[0]}"
        ))
    kb.adjust(1)
    
    await callback.message.edit_text("Codes promo:", reply_markup=kb.as_markup())

@router.callback_query(lambda c: c.data == "back_to_promos")
async def back_to_promos(callback: CallbackQuery):
    conn = mysql.connector.connect(
        host="localhost",
        user="miniapp",
        password="72Merasardtfy_",
        database="miniapp"
    )
    c = conn.cursor()
    c.execute('SELECT code FROM promo_codes')
    promos = c.fetchall()
    conn.close()
    
    kb = InlineKeyboardBuilder()
    for promo in promos:
        kb.add(InlineKeyboardButton(
            text=promo[0],
            callback_data=f"promo_info_{promo[0]}"
        ))
    kb.adjust(1)
    
    await callback.message.edit_text("Codes promo:", reply_markup=kb.as_markup())

# Gestionnaire de création de code promo
@router.message(Command("createpromo"))
async def create_promo(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
        
    await message.answer("Entrez le code promo:")
    await state.set_state(PromoStates.entering_code)

@router.message(PromoStates.entering_code)
async def process_promo_code(message: Message, state: FSMContext):
    await state.update_data(code=message.text)
    await message.answer("Entrez le montant du crédit:")
    await state.set_state(PromoStates.entering_amount)

@router.message(PromoStates.entering_amount)
async def process_promo_amount(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Veuillez entrer un nombre")
        return
        
    await state.update_data(amount=int(message.text))
    await message.answer("Entrez le nombre maximum d'utilisations:")
    await state.set_state(PromoStates.entering_uses)

@router.message(PromoStates.entering_uses)
async def process_promo_uses(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Veuillez entrer un nombre")
        return
        
    data = await state.get_data()
    code = data['code']
    amount = data['amount']
    max_uses = int(message.text)
    
    conn = mysql.connector.connect(
        host="localhost",
        user="miniapp",
        password="72Merasardtfy_",
        database="miniapp"
    )
    c = conn.cursor()
    try:
        c.execute('INSERT INTO promo_codes (code, amount, max_uses) VALUES (%s, %s, %s)',
                 (code, amount, max_uses))
        conn.commit()
        await message.answer(f"""
Code promo créé:
Code: {code}
Montant: {amount}₣
Utilisations max: {max_uses}
""")
    except mysql.connector.IntegrityError:
        await message.answer("Ce code promo existe déjà!")
    finally:
        conn.close()
        await state.clear()

# Gestionnaire d'activation de code promo
@router.message(Command("promo"))
async def activate_promo(message: Message):
    if len(message.text.split()) != 2:
        await message.answer("Utilisation: /promo CODE")
        return
        
    code = message.text.split()[1]
    user_id = message.from_user.id
    
    conn = mysql.connector.connect(
        host="localhost",
        user="miniapp",
        password="72Merasardtfy_",
        database="miniapp"
    )
    c = conn.cursor()
    
    # Vérifier l'existence du code promo
    c.execute('SELECT amount, max_uses, current_uses FROM promo_codes WHERE code = %s', (code,))
    promo = c.fetchone()
    
    if not promo:
        await message.answer("❌ Code promo non trouvé")
        conn.close()
        return
        
    amount, max_uses, current_uses = promo
    
    # Vérifier si l'utilisateur a déjà utilisé ce code
    c.execute('SELECT 1 FROM promo_uses WHERE user_id = %s AND code = %s', (user_id, code))
    if c.fetchone():
        await message.answer("❌ Vous avez déjà utilisé ce code promo")
        conn.close()
        return
        
    # Vérifier le nombre d'utilisations
    if current_uses >= max_uses:
        await message.answer("❌ Ce code promo n'est plus valide")
        conn.close()
        return
        
    try:
        # Créditer le solde et mettre à jour les statistiques
        c.execute('UPDATE users SET balance = balance + %s WHERE user_id = %s', (amount, user_id))
        c.execute('UPDATE promo_codes SET current_uses = current_uses + 1 WHERE code = %s', (code,))
        c.execute('INSERT INTO promo_uses (user_id, code) VALUES (%s, %s)', (user_id, code))
        conn.commit()
        
        await message.answer(f"✅ Code promo activé! {amount}₣ crédités")
    except Exception as e:
        print(f"Erreur lors de l'activation du code promo: {e}")
        await message.answer("❌ Une erreur s'est produite lors de l'activation du code promo")
    finally:
        conn.close()

# Gestionnaire de commande de diffusion
@router.message(Command("broadcast"))
async def start_broadcast(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
        
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Tous les utilisateurs", callback_data="recipients_all"))
    kb.add(InlineKeyboardButton(text="Niveau 1", callback_data="recipients_level_1"))
    kb.add(InlineKeyboardButton(text="Niveau 2", callback_data="recipients_level_2"))
    kb.add(InlineKeyboardButton(text="Niveau 3", callback_data="recipients_level_3"))
    kb.add(InlineKeyboardButton(text="Niveau 4", callback_data="recipients_level_4"))
    kb.add(InlineKeyboardButton(text="Niveau 5", callback_data="recipients_level_5"))
    
    await message.answer(
        "👥 Choisissez les destinataires de la diffusion:",
        reply_markup=kb.as_markup()
    )
    await state.set_state(BroadcastStates.choosing_recipients)

@router.callback_query(lambda c: c.data.startswith("recipients_"))
async def process_recipients(callback: CallbackQuery, state: FSMContext):
    recipient_type = callback.data.split("_")[1]
    
    await state.update_data(recipients=recipient_type)
    
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Passer", callback_data="skip_media"))
    
    await callback.message.edit_text(
        "📝 Entrez le texte du message à diffuser\n"
        "Vous pouvez aussi répondre avec un média (photo/vidéo)",
        reply_markup=kb.as_markup()
    )
    await state.set_state(BroadcastStates.entering_text)

@router.message(BroadcastStates.entering_text)
async def process_broadcast_text(message: Message, state: FSMContext):
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Oui", callback_data="add_button_yes"))
    kb.add(InlineKeyboardButton(text="Non", callback_data="add_button_no"))
    
    text = message.caption if message.photo else message.text
    entities = message.caption_entities if message.photo else message.entities
    
    await state.update_data(
        text=text,
        entities=entities,
        media=message.photo[-1].file_id if message.photo else None
    )
    
    await message.answer(
        "🔘 Voulez-vous ajouter un bouton au message?",
        reply_markup=kb.as_markup()
    )
    await state.set_state(BroadcastStates.adding_button)

@router.callback_query(lambda c: c.data.startswith("add_button_"))
async def process_button_choice(callback: CallbackQuery, state: FSMContext):
    choice = callback.data.split("_")[2]
    
    if choice == "yes":
        await callback.message.edit_text(
            "Entrez le texte et le lien du bouton au format:\n"
            "texte|lien"
        )
    else:
        data = await state.get_data()
        preview = f"""
📨 Aperçu de la diffusion:

📝 Texte: {data['text']}
👥 Destinataires: {data['recipients']}
🔘 Bouton: Non
        """
        
        kb = InlineKeyboardBuilder()
        kb.add(InlineKeyboardButton(text="✅ Confirmer", callback_data="confirm_broadcast"))
        kb.add(InlineKeyboardButton(text="❌ Annuler", callback_data="cancel_broadcast"))
        
        await callback.message.edit_text(
            preview,
            reply_markup=kb.as_markup()
        )
        await state.set_state(BroadcastStates.confirming)

@router.message(BroadcastStates.adding_button)
async def process_button_data(message: Message, state: FSMContext):
    if message.text is None:
        await message.answer("❌ Le texte du bouton ne peut pas être vide.")
        return

    if "|" not in message.text:
        await message.answer("❌ Format invalide. Utilisez: texte|lien")
        return

    try:
        button_text, button_url = message.text.split("|")
        await state.update_data(button_text=button_text.strip(), button_url=button_url.strip())
        
        data = await state.get_data()
        preview = f"""
📨 Aperçu de la diffusion:

📝 Texte: {data['text']}
👥 Destinataires: {data['recipients']}
🔘 Bouton: {data['button_text']} -> {data['button_url']}
        """
        
        kb = InlineKeyboardBuilder()
        kb.add(InlineKeyboardButton(text="✅ Confirmer", callback_data="confirm_broadcast"))
        kb.add(InlineKeyboardButton(text="❌ Annuler", callback_data="cancel_broadcast"))
        
        await message.answer(
            preview,
            reply_markup=kb.as_markup()
        )
        await state.set_state(BroadcastStates.confirming)
        
    except ValueError:
        await message.answer("❌ Format invalide. Utilisez: texte|lien")

@router.callback_query(lambda c: c.data in ["confirm_broadcast", "cancel_broadcast"])
async def process_confirmation(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    
    if callback.data == "cancel_broadcast":
        await state.clear()
        await callback.message.edit_text("❌ Diffusion annulée")
        return

    # Information de débogage
    print(f"Données reçues: {data}")  # Ajoutez cette ligne pour le débogage

    # Vérifier que 'recipients' a le bon format
    if 'recipients' in data:
        if data['recipients'] == "all":
            level = None  # Si tous les destinataires, pas besoin de niveau
        elif "_" in data['recipients']:
            level = int(data['recipients'].split("_")[1])
        else:
            await callback.message.edit_text("❌ Format de destinataires invalide.")
            return
    else:
        await callback.message.edit_text("❌ Format de destinataires invalide.")
        return

    # Obtenir les utilisateurs selon les critères choisis
    conn = mysql.connector.connect(
        host="localhost",
        user="miniapp",
        password="72Merasardtfy_",
        database="miniapp"
    )
    c = conn.cursor()
    
    if data['recipients'] == "all":
        c.execute('SELECT user_id FROM users')
    else:
        c.execute('SELECT user_id FROM users WHERE level = %s', (level,))
    
    users = c.fetchall()
    conn.close()
    
    # Créer le clavier s'il y a un bouton
    kb = None
    if 'button_text' in data:
        kb = InlineKeyboardBuilder()
        kb.add(InlineKeyboardButton(text=data['button_text'], url=data['button_url']))
    
    success = 0
    failed = 0
    
    await callback.message.edit_text("📤 Début de la diffusion...")
    
    for user_id in users:
        try:
            if data.get('media'):
                await bot.send_photo(
                    user_id[0],
                    data['media'],
                    caption=data['text'],
                    reply_markup=kb.as_markup() if kb else None,
                    caption_entities=data.get('entities')
                )
            else:
                await bot.send_message(
                    user_id[0],
                    data['text'],
                    reply_markup=kb.as_markup() if kb else None,
                    entities=data.get('entities')
                )
            success += 1
            await asyncio.sleep(0.1)
        except Exception as e:
            failed += 1
            print(f"Erreur d'envoi à l'utilisateur {user_id[0]}: {e}")
    
    stats = f"""
Diffusion terminée:
✅ Réussis: {success}
❌ Échoués: {failed}
📝 Total: {success + failed}
    """
    await callback.message.edit_text(stats)
    await state.clear()

# Gestionnaire de commande /start
@router.message(Command("start"))
async def start_command(message: Message):
    # Vérifier le code de parrainage
    args = message.text.split()
    referrer_id = int(args[1]) if len(args) > 1 else None
    
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Ouvrir l'application",
        web_app=WebAppInfo(url=f"https://miniapp.quantiumcode.online?user_id={message.from_user.id}")
    ))

    # Créer le lien de parrainage
    ref_link = f"https://t.me/fasdfadf_bot?start={message.from_user.id}"
    
    # Enregistrer l'utilisateur
    register_user(message.from_user.id, message.from_user.username, referrer_id)

    
    user_data = get_user_data(message.from_user.id)
    
    welcome_text = f"""
    👋 *Bienvenue dans le bot!*
    
💰 Invitez des amis et gagnez:
• 10% des gains de vos amis
• 1000₣ par ami invité
    
📊 Vos statistiques:
Niveau: {user_data['level']}
Solde: {user_data['balance']}₣
Amis invités: {user_data['invited_users']}
    """
    
    await message.answer(
        welcome_text,
        reply_markup=kb.as_markup(),
        parse_mode=ParseMode.MARKDOWN
    )

def register_user(user_id: int, username: str, referrer_id: int = None):
    conn = mysql.connector.connect(
        host="localhost",
        user="miniapp",
        password="72Merasardtfy_",
        database="miniapp"
    )
    c = conn.cursor()
    
    # Vérifier si l'utilisateur existe
    c.execute('SELECT user_id FROM users WHERE user_id = %s', (user_id,))
    if not c.fetchone():
        c.execute('''INSERT INTO users (user_id, username, referrer_id)
                    VALUES (%s, %s, %s)''', (user_id, username, referrer_id))
        
        # Si parrain, mettre à jour ses statistiques et créditer le bonus selon son niveau
        if referrer_id:
            c.execute('SELECT level FROM users WHERE user_id = %s', (referrer_id,))
            level = c.fetchone()[0]
            
            bonus = {
                1: 2000,
                2: 2000,
                3: 5000,
                4: 6000, 
                5: 10000
            }.get(level, 2000)  # 2000 par défaut si niveau inconnu
            
            c.execute('''UPDATE users 
                        SET invited_users = invited_users + 1,
                            balance = balance + %s,
                            zadanie_5 = 1
                        WHERE user_id = %s''', (bonus, referrer_id))
            bot.send_message(
                referrer_id,
                f"🎉 Vous avez un nouvel utilisateur invité!\n"
                f"💰 Vous avez reçu un bonus de {bonus}₣"
            )
    
    conn.commit()
    conn.close()

# Fonction pour obtenir les données utilisateur
def get_user_data(user_id: int) -> Dict:
    conn = mysql.connector.connect(
        host="localhost",
        user="miniapp",
        password="72Merasardtfy_",
        database="miniapp"
    )
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE user_id = %s', (user_id,))
    user = c.fetchone()
    conn.close()
    
    if not user:
        return {'level': 1, 'balance': 0, 'invited_users': 0}
    return {
        'level': user[2],
        'balance': user[3],
        'invited_users': user[4],
        'referrer_id': user[5]
    }

# Fonction pour vérifier le niveau
async def check_level_requirements(user_id: int):
    conn = mysql.connector.connect(
        host="localhost",
        user="miniapp",
        password="72Merasardtfy_",
        database="miniapp"
    )
    c = conn.cursor()
    
    user_data = get_user_data(user_id)
    current_level = user_data['level']
    
    # Logique de vérification des exigences pour chaque niveau
    if current_level == 1:
        # Vérifier l'accomplissement de la tâche d'abonnement
        c.execute('SELECT zadanie_1 FROM users WHERE user_id = %s', (user_id,))
        if c.fetchone()[0]:
            c.execute('UPDATE users SET level = 2 WHERE user_id = %s', (user_id,))
            
    elif current_level == 2:
        # Vérifier l'accomplissement de la tâche d'inscription
        c.execute('SELECT zadanie_2 FROM users WHERE user_id = %s', (user_id,))
        if c.fetchone()[0]:
            c.execute('UPDATE users SET level = 3 WHERE user_id = %s', (user_id,))
            
    elif current_level == 3:
        # Vérifier la présence de 5 amis invités de niveau 2
        c.execute('''SELECT COUNT(*) FROM users 
                    WHERE referrer_id = %s AND level >= 2''', (user_id,))
        if c.fetchone()[0] >= 5:
            c.execute('UPDATE users SET level = 4 WHERE user_id = %s', (user_id,))
            
    elif current_level == 4:
        # Vérifier la présence de 15 amis invités
        c.execute('''SELECT COUNT(*) FROM users 
                    WHERE referrer_id = %s''', (user_id,))
        if c.fetchone()[0] >= 15:
            c.execute('UPDATE users SET level = 5 WHERE user_id = %s', (user_id,))
            
    elif current_level == 5:
        # Vérifier la présence de 3 amis de niveau 3
        c.execute('''SELECT COUNT(*) FROM users 
                    WHERE referrer_id = %s AND level >= 3''', (user_id,))
        if c.fetchone()[0] >= 3:
            c.execute('UPDATE users SET level = 5 WHERE user_id = %s', (user_id,))
    
    conn.commit()
    conn.close()

# Commandes pour obtenir les statistiques
@router.message(Command("stats"))
async def get_full_statistics(message: Message):
    stats = get_statistics()
    stats_text = f"""
📊 *Statistiques globales du bot:*

👥 Total utilisateurs: {stats['total_users']}
🆕 Nouveaux aujourd'hui: {stats['new_today']}
📈 Par niveau:
• Niveau 1: {stats['level_1']}
• Niveau 2: {stats['level_2']}
• Niveau 3: {stats['level_3']}
• Niveau 4: {stats['level_4']}
• Niveau 5: {stats['level_5']}

🤝 Sans parrainages: {stats['no_referrals']}
💰 Solde total: {stats['total_balance']}₣
    """
    await message.answer(stats_text, parse_mode=ParseMode.MARKDOWN)

@router.message(Command("level_stats"))
async def get_level_statistics(message: Message):
    
    level = int(message.text.split()[1]) if len(message.text.split()) > 1 else 1
    stats = get_level_stats(level)
    stats_text = f"""
📊 *Statistiques niveau {level}:*

👥 Utilisateurs au niveau: {stats['users_count']}
💰 Solde moyen: {stats['avg_balance']}₣
👨‍👦‍👦 Nombre moyen de parrainages: {stats['avg_referrals']}
    """
    await message.answer(stats_text, parse_mode=ParseMode.MARKDOWN)

# Fonction pour obtenir les statistiques
def get_statistics() -> Dict:
    conn = mysql.connector.connect(
        host="localhost",
        user="miniapp",
        password="72Merasardtfy_",
        database="miniapp"
    )
    c = conn.cursor()
    
    stats = {
        'total_users': 0,
        'new_today': 0,
        'no_referrals': 0,
        'level_1': 0,
        'level_2': 0,
        'level_3': 0,
        'level_4': 0,
        'level_5': 0,
        'total_balance': 0
    }
    
    # Nombre total d'utilisateurs
    c.execute('SELECT COUNT(*) FROM users')
    stats['total_users'] = c.fetchone()[0]
    
    # Nouveaux utilisateurs aujourd'hui
    c.execute('''SELECT COUNT(*) FROM users 
                WHERE DATE(join_date) = CURDATE()''')
    stats['new_today'] = c.fetchone()[0]
    
    # Utilisateurs sans parrainages
    c.execute('SELECT COUNT(*) FROM users WHERE invited_users = 0')
    stats['no_referrals'] = c.fetchone()[0]
    
    # Statistiques par niveau
    for level in range(1, 6):
        c.execute('SELECT COUNT(*) FROM users WHERE level = %s', (level,))
        stats[f'level_{level}'] = c.fetchone()[0]
    
    # Solde total
    c.execute('SELECT SUM(balance) FROM users')
    stats['total_balance'] = c.fetchone()[0] or 0
    
    conn.close()
    return stats

def get_level_stats(level: int) -> Dict:
    conn = mysql.connector.connect(
        host="localhost",
        user="miniapp",
        password="72Merasardtfy_",
        database="miniapp"
    )
    c = conn.cursor()
    
    stats = {
        'users_count': 0,
        'avg_balance': 0,
        'avg_referrals': 0
    }
    
    c.execute('''SELECT COUNT(*), AVG(balance), AVG(invited_users)
                FROM users WHERE level = %s''', (level,))
    result = c.fetchone()
    
    stats['users_count'] = result[0]
    stats['avg_balance'] = round(result[1] or 0, 2)
    stats['avg_referrals'] = round(result[2] or 0, 2)
    
    conn.close()
    return stats

dp.include_router(router)

async def main():
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
