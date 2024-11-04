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
# Определите ID администратора
ADMIN_ID = 5685109533  # Замените на ваш фактический ID администратора
FIRST_CHANNEL_LINK = "https://t.me/+cdlYMb4VnbgzZDVi"
SECOND_CHANNEL_LINK = "https://t.me/+1uS2fYpUS4dmNWI6"
WIN_LINK = "https://1wwwl.com/?open=register"
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


@router.message()
async def handle_incoming_messages(message: Message):
    print(message)

    
    # Проверяем, что сообщение содержит текст
    if not message.text:
        return
        
    # Обрабатываем сообщения от бота и от пользователей в группах
    if message.chat.type in ['group', 'supergroup']:
        text = message.text
        
        try:
            # Проверка на регистрацию
            if text.startswith("1вин:регистрация:"):
                user_id = text.split(":")[2]
                await process_registration(user_id)
                await message.answer(f"Пользователь {user_id} успешно зарегистрирован!")
            
            # Проверка на первый депозит 
            elif text.startswith("1вин:") and ":первый_депозит:" in text:
                parts = text.split(":")
                user_id = parts[1]
                amount = parts[3]
                await process_first_deposit(user_id, amount)
                await message.answer(f"Пользователь {user_id} успешно внес первый депозит в размере {amount}!")
                
        except Exception as e:
            print(f"Ошибка при обработке сообщения: {e}")
            await message.answer("Произошла ошибка при обработке сообщения")
async def process_registration(user_id: str):
    print(f"Пользователь {user_id} зарегистрировался.")
async def process_first_deposit(user_id: str, amount: str):
    print(f"Пользователь {user_id} сделал первый депозит: {amount}.")


# Обработчик списка промокодов
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
    
    await message.answer("Промокоды:", reply_markup=kb.as_markup())

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
        await callback.answer("Промокод не найден")
        return
        
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="🗑 Удалить",
        callback_data=f"delete_promo_{code}"
    ))
    kb.add(InlineKeyboardButton(
        text="◀️ Назад",
        callback_data="back_to_promos"
    ))
    kb.adjust(1)
    
    info_text = f"""
Информация о промокоде:
Код: {promo[0]}
Сумма: {promo[1]}₣
Макс. использований: {promo[2]}
Использовано: {promo[3]}
Создан: {promo[4]}
"""
    
    await callback.message.edit_text(
        info_text,
        reply_markup=kb.as_markup()
    )
@router.callback_query(lambda c: c.data.startswith("delete_promo_"))
async def delete_promo(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("У вас нет прав для удаления промокодов")
        return
        
    code = callback.data.split("_")[2]
    
    conn = mysql.connector.connect(
        host="localhost",
        user="miniapp",
        password="72Merasardtfy_",
        database="miniapp"
    )
    c = conn.cursor()
    
    # Проверяем существование промокода
    c.execute('SELECT code FROM promo_codes WHERE code = %s', (code,))
    if not c.fetchone():
        await callback.answer("Промокод не найден")
        conn.close()
        return
        
    # Удаляем промокод
    c.execute('DELETE FROM promo_codes WHERE code = %s', (code,))
    conn.commit()
    conn.close()
    
    await callback.answer("✅ Промокод успешно удален")
    
    # Получаем обновленный список промокодов
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
    
    await callback.message.edit_text("Промокоды:", reply_markup=kb.as_markup())
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
    
    await callback.message.edit_text("Промокоды:", reply_markup=kb.as_markup())

# Обработчик создания промокода
@router.message(Command("createpromo"))
async def create_promo(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
        
    await message.answer("Введите код промокода:")
    await state.set_state(PromoStates.entering_code)

@router.message(PromoStates.entering_code)
async def process_promo_code(message: Message, state: FSMContext):
    await state.update_data(code=message.text)
    await message.answer("Введите сумму начисления:")
    await state.set_state(PromoStates.entering_amount)

@router.message(PromoStates.entering_amount)
async def process_promo_amount(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите число")
        return
        
    await state.update_data(amount=int(message.text))
    await message.answer("Введите максимальное количество использований:")
    await state.set_state(PromoStates.entering_uses)

@router.message(PromoStates.entering_uses)
async def process_promo_uses(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите число")
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
Промокод создан:
Код: {code}
Сумма: {amount}₣
Макс. использований: {max_uses}
""")
    except mysql.connector.IntegrityError:
        await message.answer("Такой промокод уже существует!")
    finally:
        conn.close()
        await state.clear()

# Обработчик активации промокода
@router.message(Command("promo"))
async def activate_promo(message: Message):
    if len(message.text.split()) != 2:
        await message.answer("Использование: /promo КОД")
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
    
    # Проверяем существование промокода
    c.execute('SELECT amount, max_uses, current_uses FROM promo_codes WHERE code = %s', (code,))
    promo = c.fetchone()
    
    if not promo:
        await message.answer("❌ Промокод не найден")
        conn.close()
        return
        
    amount, max_uses, current_uses = promo
    
    # Проверяем, не использовал ли пользователь этот промокод
    c.execute('SELECT 1 FROM promo_uses WHERE user_id = %s AND code = %s', (user_id, code))
    if c.fetchone():
        await message.answer("❌ Вы уже использовали этот промокод")
        conn.close()
        return
        
    # Проверяем количество использований
    if current_uses >= max_uses:
        await message.answer("❌ Промокод больше не действителен")
        conn.close()
        return
        
    try:
        # Начисляем баланс и обновляем статистику
        c.execute('UPDATE users SET balance = balance + %s WHERE user_id = %s', (amount, user_id))
        c.execute('UPDATE promo_codes SET current_uses = current_uses + 1 WHERE code = %s', (code,))
        c.execute('INSERT INTO promo_uses (user_id, code) VALUES (%s, %s)', (user_id, code))
        conn.commit()
        
        await message.answer(f"✅ Промокод активирован! Начислено {amount}₣")
    except Exception as e:
        print(f"Ошибка при активации промокода: {e}")
        await message.answer("❌ Произошла ошибка при активации промокода")
    finally:
        conn.close()

# Обработчик команды рассылки
@router.message(Command("broadcast"))
async def start_broadcast(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
        
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Всем пользователям", callback_data="recipients_all"))
    kb.add(InlineKeyboardButton(text="Уровень 1", callback_data="recipients_level_1"))
    kb.add(InlineKeyboardButton(text="Уровень 2", callback_data="recipients_level_2"))
    kb.add(InlineKeyboardButton(text="Уровень 3", callback_data="recipients_level_3"))
    kb.add(InlineKeyboardButton(text="Уровень 4", callback_data="recipients_level_4"))
    kb.add(InlineKeyboardButton(text="Уровень 5", callback_data="recipients_level_5"))
    
    await message.answer(
        "👥 Выберите получателей рассылки:",
        reply_markup=kb.as_markup()
    )
    await state.set_state(BroadcastStates.choosing_recipients)

@router.callback_query(lambda c: c.data.startswith("recipients_"))
async def process_recipients(callback: CallbackQuery, state: FSMContext):
    recipient_type = callback.data.split("_")[1]
    
    await state.update_data(recipients=recipient_type)
    
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Пропустить", callback_data="skip_media"))
    
    await callback.message.edit_text(
        "📝 Введите текст сообщения для рассылки\n"
        "Можете также ответить на сообщение с медиа (фото/видео)",
        reply_markup=kb.as_markup()
    )
    await state.set_state(BroadcastStates.entering_text)

@router.message(BroadcastStates.entering_text)
async def process_broadcast_text(message: Message, state: FSMContext):
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Да", callback_data="add_button_yes"))
    kb.add(InlineKeyboardButton(text="Нет", callback_data="add_button_no"))
    
    text = message.caption if message.photo else message.text
    entities = message.caption_entities if message.photo else message.entities
    
    await state.update_data(
        text=text,
        entities=entities,
        media=message.photo[-1].file_id if message.photo else None
    )
    
    await message.answer(
        "🔘 Хотите добавить кнопку к сообщению?",
        reply_markup=kb.as_markup()
    )
    await state.set_state(BroadcastStates.adding_button)

@router.callback_query(lambda c: c.data.startswith("add_button_"))
async def process_button_choice(callback: CallbackQuery, state: FSMContext):
    choice = callback.data.split("_")[2]
    
    if choice == "yes":
        await callback.message.edit_text(
            "Введите текст и ссылку для кнопки в формате:\n"
            "текст|ссылка"
        )
    else:
        data = await state.get_data()
        preview = f"""
📨 Предпросмотр рассылки:

📝 Текст: {data['text']}
👥 Получатели: {data['recipients']}
🔘 Кнопка: Нет
        """
        
        kb = InlineKeyboardBuilder()
        kb.add(InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_broadcast"))
        kb.add(InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_broadcast"))
        
        await callback.message.edit_text(
            preview,
            reply_markup=kb.as_markup()
        )
        await state.set_state(BroadcastStates.confirming)

@router.message(BroadcastStates.adding_button)
async def process_button_data(message: Message, state: FSMContext):
    if message.text is None:
        await message.answer("❌ Текст кнопки не может быть пустым.")
        return

    if "|" not in message.text:
        await message.answer("❌ Неверный формат. Используйте: текст|ссылка")
        return

    try:
        button_text, button_url = message.text.split("|")
        await state.update_data(button_text=button_text.strip(), button_url=button_url.strip())
        
        data = await state.get_data()
        preview = f"""
📨 Предпросмотр рассылки:

📝 Текст: {data['text']}
👥 Получатели: {data['recipients']}
🔘 Кнопка: {data['button_text']} -> {data['button_url']}
        """
        
        kb = InlineKeyboardBuilder()
        kb.add(InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_broadcast"))
        kb.add(InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_broadcast"))
        
        await message.answer(
            preview,
            reply_markup=kb.as_markup()
        )
        await state.set_state(BroadcastStates.confirming)
        
    except ValueError:
        await message.answer("❌ Неверный формат. Используйте: текст|ссылка")

@router.callback_query(lambda c: c.data in ["confirm_broadcast", "cancel_broadcast"])
async def process_confirmation(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    
    if callback.data == "cancel_broadcast":
        await state.clear()
        await callback.message.edit_text("❌ Рассылка отменена")
        return

    # Отладочная информация
    print(f"Полученные данные: {data}")  # Добавьте эту строку для отладки

    # Проверяем, что 'recipients' имеет правильный формат
    if 'recipients' in data:
        if data['recipients'] == "all":
            level = None  # Если получатели все, уровень не нужен
        elif "_" in data['recipients']:
            level = int(data['recipients'].split("_")[1])
        else:
            await callback.message.edit_text("❌ Неверный формат получателей.")
            return
    else:
        await callback.message.edit_text("❌ Неверный формат получателей.")
        return

    # Получаем пользователей согласно выбранным критериям
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
    
    # Создаем клавиатуру если есть кнопка
    kb = None
    if 'button_text' in data:
        kb = InlineKeyboardBuilder()
        kb.add(InlineKeyboardButton(text=data['button_text'], url=data['button_url']))
    
    success = 0
    failed = 0
    
    await callback.message.edit_text("📤 Начинаю рассылку...")
    
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
            print(f"Ошибка отправки пользователю {user_id[0]}: {e}")
    
    stats = f"""
Рассылка завершена:
✅ Успешно: {success}
❌ Не удалось: {failed}
📝 Всего: {success + failed}
    """
    await callback.message.edit_text(stats)
    await state.clear()

# Обработчик команды /start
@router.message(Command("start"))
async def start_command(message: Message):
    # Проверяем реферальный код
    args = message.text.split()
    referrer_id = int(args[1]) if len(args) > 1 else None
    
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(
        text="Открыть приложение",
        web_app=WebAppInfo(url="https://miniapp.quantiumcode.online?user_id={message.from_user.id}")
    ))
    
    # Создаем реферальную ссылку
    ref_link = f"https://t.me/fasdfadf_bot?start={message.from_user.id}"
    
    # Регистрируем пользователя
    register_user(message.from_user.id, message.from_user.username, referrer_id)
    
    user_data = get_user_data(message.from_user.id)
    
    welcome_text = f"""
    👋 *Добро пожаловать в бота!*
    
💰 Приглашайте друзей и зарабатывайте:
• 10% от дохода друга
• 1000₣ за каждого приглашенного
    
📊 Ваша статистика:
Уровень: {user_data['level']}
Баланс: {user_data['balance']}₣
Приглашено друзей: {user_data['invited_users']}
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
    
    # Проверяем существует ли пользователь
    c.execute('SELECT user_id FROM users WHERE user_id = %s', (user_id,))
    if not c.fetchone():
        c.execute('''INSERT INTO users (user_id, username, referrer_id)
                    VALUES (%s, %s, %s)''', (user_id, username, referrer_id))
        
        # Если есть реферер, обновляем его статистику и начисляем бонус в зависимости от уровня
        if referrer_id:
            c.execute('SELECT level FROM users WHERE user_id = %s', (referrer_id,))
            level = c.fetchone()[0]
            
            bonus = {
                1: 2000,
                2: 2000,
                3: 5000, 
                4: 6000,
                5: 10000
            }.get(level, 2000)  # По умолчанию 2000 если уровень неизвестен
            
            c.execute('''UPDATE users 
                        SET invited_users = invited_users + 1,
                            balance = balance + %s,
                            zadanie_5 = 1
                        WHERE user_id = %s''', (bonus, referrer_id))
    
    conn.commit()
    conn.close()

# Функция получения данных пользователя
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

# Функция проверки уровня
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
    
    # Логика проверки требований для каждого уровня
    if current_level == 1:
        # Проверка выполнения задания с подпиской
        c.execute('SELECT zadanie_1 FROM users WHERE user_id = %s', (user_id,))
        if c.fetchone()[0]:
            c.execute('UPDATE users SET level = 2 WHERE user_id = %s', (user_id,))
            
    elif current_level == 2:
        # Проверка выполнения задания с регистрацией
        c.execute('SELECT zadanie_2 FROM users WHERE user_id = %s', (user_id,))
        if c.fetchone()[0]:
            c.execute('UPDATE users SET level = 3 WHERE user_id = %s', (user_id,))
            
    elif current_level == 3:
        # Проверка наличия 5 приглашенных друзей 2 уровня
        c.execute('''SELECT COUNT(*) FROM users 
                    WHERE referrer_id = %s AND level >= 2''', (user_id,))
        if c.fetchone()[0] >= 5:
            c.execute('UPDATE users SET level = 4 WHERE user_id = %s', (user_id,))
            
    elif current_level == 4:
        # Проверка наличия 15 приглашенных друзей
        c.execute('''SELECT COUNT(*) FROM users 
                    WHERE referrer_id = %s''', (user_id,))
        if c.fetchone()[0] >= 15:
            c.execute('UPDATE users SET level = 5 WHERE user_id = %s', (user_id,))
            
    elif current_level == 5:
        # Проверка наличия 3 друзей 3 уровня
        c.execute('''SELECT COUNT(*) FROM users 
                    WHERE referrer_id = %s AND level >= 3''', (user_id,))
        if c.fetchone()[0] >= 3:
            c.execute('UPDATE users SET level = 5 WHERE user_id = %s', (user_id,))
    
    conn.commit()
    conn.close()

# Команды для получения статистики
@router.message(Command("stats"))
async def get_full_statistics(message: Message):
    stats = get_statistics()
    stats_text = f"""
📊 *Общая статистика бота:*

👥 Всего пользователей: {stats['total_users']}
🆕 Новых за сегодня: {stats['new_today']}
📈 По уровням:
• Уровень 1: {stats['level_1']}
• Уровень 2: {stats['level_2']}
• Уровень 3: {stats['level_3']}
• Уровень 4: {stats['level_4']}
• Уровень 5: {stats['level_5']}

🤝 Без рефералов: {stats['no_referrals']}
💰 Общий баланс: {stats['total_balance']}₣
    """
    await message.answer(stats_text, parse_mode=ParseMode.MARKDOWN)

@router.message(Command("level_stats"))
async def get_level_statistics(message: Message):
    level = int(message.text.split()[1]) if len(message.text.split()) > 1 else 1
    stats = get_level_stats(level)
    stats_text = f"""
📊 *Статистика уровня {level}:*

👥 Пользователей на уровне: {stats['users_count']}
💰 Средний баланс: {stats['avg_balance']}₣
👨‍👦‍👦 Среднее количество рефералов: {stats['avg_referrals']}
    """
    await message.answer(stats_text, parse_mode=ParseMode.MARKDOWN)

# Функция получения статистики
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
    
    # Общее количество пользователей
    c.execute('SELECT COUNT(*) FROM users')
    stats['total_users'] = c.fetchone()[0]
    
    # Новые пользователи за сегодня
    c.execute('''SELECT COUNT(*) FROM users 
                WHERE DATE(join_date) = CURDATE()''')
    stats['new_today'] = c.fetchone()[0]
    
    # Пользователи без рефералов
    c.execute('SELECT COUNT(*) FROM users WHERE invited_users = 0')
    stats['no_referrals'] = c.fetchone()[0]
    
    # Статистика по уровням
    for level in range(1, 6):
        c.execute('SELECT COUNT(*) FROM users WHERE level = ?', (level,))
        stats[f'level_{level}'] = c.fetchone()[0]
    
    # Общий баланс
    c.execute('SELECT SUM(balance) FROM users')
    stats['total_balance'] = c.fetchone()[0] or 0
    
    conn.close()
    return stats

def get_level_stats(level: int) -> Dict:
    conn = sqlite3.connect('bot_database.db')
    c = conn.cursor()
    
    stats = {
        'users_count': 0,
        'avg_balance': 0,
        'avg_referrals': 0
    }
    
    c.execute('''SELECT COUNT(*), AVG(balance), AVG(invited_users)
                FROM users WHERE level = ?''', (level,))
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
