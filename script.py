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

# Состояния для FSM
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

# Инициализация бота и диспетчера
bot = Bot(token="7666407425:AAF623qqMheTU-SD_zTbFqmy8w2i_WHGAFw")
dp = Dispatcher()
router = Router()
# Установка ID администратора
ADMIN_ID = 612475751

FIRST_CHANNEL_LINK = "https://t.me/+cdlYMb4VnbgzZDVi"
SECOND_CHANNEL_LINK = "https://t.me/+1uS2fYpUS4dmNWI6"
WIN_LINK = "https://1wwwl.com/?open=register&sub1="

# Создание базы данных
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

# Админ-панель
@router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
        
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats"))
    kb.add(InlineKeyboardButton(text="📨 Рассылка", callback_data="admin_broadcast"))
    kb.add(InlineKeyboardButton(text="🎟 Промокоды", callback_data="admin_promos"))
    kb.adjust(1)
    
    await message.answer(
        "🎛 *Админ-панель*\nВыберите действие:",
        reply_markup=kb.as_markup(),
        parse_mode=ParseMode.MARKDOWN
    )

@router.callback_query(lambda c: c.data.startswith("admin_"))
async def admin_panel_handler(callback: CallbackQuery, state: FSMContext):
    action = callback.data.split("_")[1]
    
    if action == "stats":
        stats = get_statistics()
        stats_text = f"""
📊 *Статистика бота:*

👥 Всего пользователей: {stats['total_users']}
🆕 Новых сегодня: {stats['new_today']}
📈 По уровням:
• Уровень 1: {stats['level_1']}
• Уровень 2: {stats['level_2']}
• Уровень 3: {stats['level_3']}
• Уровень 4: {stats['level_4']}
• Уровень 5: {stats['level_5']}

🤝 Без рефералов: {stats['no_referrals']}
💰 Общий баланс: {stats['total_balance']}₣
        """
        kb = InlineKeyboardBuilder()
        kb.add(InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_admin"))
        await callback.message.edit_text(stats_text, reply_markup=kb.as_markup(), parse_mode=ParseMode.MARKDOWN)
        
    elif action == "broadcast":
        kb = InlineKeyboardBuilder()
        kb.row(InlineKeyboardButton(text="Все пользователи", callback_data="recipients_all"))
        kb.row(InlineKeyboardButton(text="Уровень 1", callback_data="recipients_level_1"))
        kb.row(InlineKeyboardButton(text="Уровень 2", callback_data="recipients_level_2"))
        kb.row(InlineKeyboardButton(text="Уровень 3", callback_data="recipients_level_3"))
        kb.row(InlineKeyboardButton(text="Уровень 4", callback_data="recipients_level_4"))
        kb.row(InlineKeyboardButton(text="Уровень 5", callback_data="recipients_level_5"))
        kb.row(InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_admin"))
        
        await callback.message.edit_text(
            "👥 Выберите получателей рассылки:",
            reply_markup=kb.as_markup()
        )
        await state.set_state(BroadcastStates.choosing_recipients)
        
    elif action == "promos":
        kb = InlineKeyboardBuilder()
        kb.add(InlineKeyboardButton(text="📝 Создать промокод", callback_data="create_promo"))
        kb.add(InlineKeyboardButton(text="📋 Список промокодов", callback_data="list_promos"))
        kb.add(InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_admin"))
        kb.adjust(1)
        
        await callback.message.edit_text(
            "🎟 *Управление промокодами*\nВыберите действие:",
            reply_markup=kb.as_markup(),
            parse_mode=ParseMode.MARKDOWN
        )

@router.callback_query(lambda c: c.data == "back_to_admin")
async def back_to_admin(callback: CallbackQuery):
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats"))
    kb.add(InlineKeyboardButton(text="📨 Рассылка", callback_data="admin_broadcast"))
    kb.add(InlineKeyboardButton(text="🎟 Промокоды", callback_data="admin_promos"))
    kb.adjust(1)
    
    await callback.message.edit_text(
        "🎛 *Админ-панель*\nВыберите действие:",
        reply_markup=kb.as_markup(),
        parse_mode=ParseMode.MARKDOWN
    )

# Обработчик команды /start
@router.message(Command("start"))
async def start_command(message: Message):
    # Проверяем реферальный код
    args = message.text.split()
    referrer_id = int(args[1]) if len(args) > 1 else None
    
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Ouvrir l'application",
        web_app=WebAppInfo(url=f"https://miniapp.quantiumcode.online?user_id={message.from_user.id}")
    ))

    # Создаем реферальную ссылку
    ref_link = f"https://t.me/fasdfadf_bot?start={message.from_user.id}"
    
    # Регистрируем пользователя
    await register_user(message.from_user.id, message.from_user.username, referrer_id)
    
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

# Вспомогательные функции
async def register_user(user_id: int, username: str, referrer_id: int = None):
    conn = mysql.connector.connect(
        host="localhost",
        user="miniapp",
        password="72Merasardtfy_",
        database="miniapp"
    )
    c = conn.cursor()
    
    c.execute('SELECT user_id FROM users WHERE user_id = %s', (user_id,))
    if not c.fetchone():
        c.execute('''INSERT INTO users (user_id, username, referrer_id)
                    VALUES (%s, %s, %s)''', (user_id, username, referrer_id))
        
        if referrer_id:
            c.execute('SELECT level, invited_users FROM users WHERE user_id = %s', (referrer_id,))
            result = c.fetchone()
            level = result[0]
            invited_users = result[1]
            
            bonus = {1: 2000, 2: 2000, 3: 5000, 4: 6000, 5: 10000}.get(level, 2000)
            
            new_level = level
            if invited_users + 1 >= 15:
                new_level = level + 1
            
            c.execute('''UPDATE users 
                        SET invited_users = invited_users + 1,
                            balance = balance + %s,
                            zadanie_5 = 1,
                            level = %s
                        WHERE user_id = %s''', (bonus, new_level, referrer_id))
                 
            await bot.send_message(
                referrer_id,
                f"🎉 Vous avez un nouvel utilisateur invité!\n"
                f"💰 Vous avez reçu un bonus de {bonus}₣"
            )
    
    conn.commit()
    conn.close()

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
    
    c.execute('SELECT COUNT(*) FROM users')
    stats['total_users'] = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM users WHERE DATE(join_date) = CURDATE()')
    stats['new_today'] = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM users WHERE invited_users = 0')
    stats['no_referrals'] = c.fetchone()[0]
    
    for level in range(1, 6):
        c.execute('SELECT COUNT(*) FROM users WHERE level = %s', (level,))
        stats[f'level_{level}'] = c.fetchone()[0]
    
    c.execute('SELECT SUM(balance) FROM users')
    stats['total_balance'] = c.fetchone()[0] or 0
    
    conn.close()
    return stats

dp.include_router(router)

async def main():
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
