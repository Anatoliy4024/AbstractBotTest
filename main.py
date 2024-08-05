import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
import sqlite3
import keyboards
import os
import time

# Устанавливаем уровень логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Устанавливаем путь к базе данных
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "user_sessions.db")
print(f"Path to database: {db_path}")

# Создаем таблицу user_sessions, если она не существует
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    language TEXT,
    user_name TEXT,
    event_date TEXT,
    start_time TEXT,
    end_time TEXT,
    number_of_people INTEGER,
    party_style TEXT,
    preferences TEXT,
    city TEXT,
    duration TEXT
)
''')
conn.commit()
conn.close()


# Обработчик команды /start
async def start(update: Update, context):
    user_id = update.message.from_user.id
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO user_sessions (user_id) VALUES (?)
    ''', (user_id,))
    conn.commit()
    conn.close()
    keyboard = [[InlineKeyboardButton("English", callback_data='lang_en'),
                 InlineKeyboardButton("Русский", callback_data='lang_ru')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please choose your language / Пожалуйста, выберите язык",
                                    reply_markup=reply_markup)


# Обработчик нажатия на кнопки
async def button_callback(update: Update, context):
    query = update.callback_query
    user_id = query.from_user.id
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if query.data == 'lang_en':
        cursor.execute('''
        UPDATE user_sessions SET language = 'en' WHERE user_id = ?
        ''', (user_id,))
        await query.message.reply_text("Please wait...")
        time.sleep(3)
        await query.message.reply_photo(open('media/IMG_4077_1 (online-video-cutter.com).mp4', 'rb'))
        await query.message.reply_text("Hi! What's your name?")

    elif query.data == 'lang_ru':
        cursor.execute('''
        UPDATE user_sessions SET language = 'ru' WHERE user_id = ?
        ''', (user_id,))
        await query.message.reply_text("Пожалуйста, подождите...")
        time.sleep(3)
        await query.message.reply_photo(open('media/IMG_4077_1 (online-video-cutter.com).mp4', 'rb'))
        await query.message.reply_text("Привет! Как вас зовут?")

    conn.commit()
    conn.close()
    await query.answer()


# Обработчик ввода имени
async def name_handler(update: Update, context):
    user_id = update.message.from_user.id
    user_name = update.message.text
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE user_sessions SET user_name = ? WHERE user_id = ?
    ''', (user_name, user_id))
    conn.commit()
    conn.close()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT language, user_name FROM user_sessions WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()
    language = user_data[0]
    user_name = user_data[1]
    if language == 'en':
        greeting = f"Hello, {user_name}! Do you want to see available dates?"
        keyboard = [[InlineKeyboardButton("Yes", callback_data='confirm_date'),
                     InlineKeyboardButton("No", callback_data='reject_date')]]
    else:
        greeting = f"Привет, {user_name}! Хочешь увидеть доступные даты?"
        keyboard = [[InlineKeyboardButton("Да", callback_data='confirm_date'),
                     InlineKeyboardButton("Нет", callback_data='reject_date')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(greeting, reply_markup=reply_markup)


# Обработчик текстовых сообщений
async def handle_text(update: Update, context):
    user_id = update.message.from_user.id
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT user_name FROM user_sessions WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()
    if user_data is None or user_data[0] is None:
        await name_handler(update, context)


# Создаем приложение и добавляем обработчики
application = Application.builder().token("7407529729:AAErOT5NBpMSO-V-HPAW-MDu_1WQt0TtXng").build()

application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button_callback))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

# Запуск приложения
application.run_polling()
