#
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, MessageHandler, ContextTypes, filters
import logging
import os
from datetime import datetime
import sqlite3
from telegram.ext import CallbackQueryHandler
from keyboards import language_selection_keyboard, generate_calendar_keyboard, generate_time_selection_keyboard, generate_person_selection_keyboard, generate_party_styles_keyboard
from abstract_functions import A, B, C_combined

import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def button_callback(update, context):
    query = update.callback_query
    query.answer()

    logger.info(f"Button clicked: {query.data}")

VIDEO_PATHS = [
    'media/video1.mp4',
    'media/video2.mp4'
]

BOT_TOKEN = '7407529729:AAErOT5NBpMSO-V-HPAW-MDu_1WQt0TtXng'

db_path = os.path.join(os.path.dirname(__file__), 'user_sessions.db')
print(f"Path to database: {db_path}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await update.message.reply_text(f"Привет, {user.first_name}!\nВыберите язык.", reply_markup=language_selection_keyboard())

async def handle_language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_data = context.user_data

    if query.data == 'lang_en':
        user_data['language'] = 'en'
        await query.message.reply_text("You selected English!")
    elif query.data == 'lang_ru':
        user_data['language'] = 'ru'
        await query.message.reply_text("Вы выбрали Русский!")

    await query.message.reply_text("Как вас зовут?")

async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_data = context.user_data
    user_data['name'] = update.message.text
    await update.message.reply_text(f"Привет, {user_data['name']}! Хочешь увидеть доступные даты?", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("Да", callback_data='yes')],
        [InlineKeyboardButton("Назад", callback_data='no')]
    ]))

async def handle_preferences(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    user_data['preferences'] = update.message.text
    await update.message.reply_text("Ваши предпочтения сохранены.")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    query.answer()
    user_data = context.user_data

    if query.data == 'yes':
        await query.message.reply_text("Пожалуйста, выберите дату.", reply_markup=generate_calendar_keyboard())
    elif query.data == 'no':
        await query.message.reply_text("Назад.", reply_markup=language_selection_keyboard())

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_preferences))

    application.run_polling()
