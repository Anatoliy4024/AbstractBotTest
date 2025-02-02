import os
import logging
import random
from datetime import datetime
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, MessageHandler, ContextTypes, filters
from abstract_functions import create_connection, execute_query
from keyboards import language_selection_keyboard, yes_no_keyboard, generate_calendar_keyboard, generate_time_selection_keyboard, generate_person_selection_keyboard, generate_party_styles_keyboard

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'user_sessions.db')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

VIDEO_PATHS = [
    'media/IMG_5981 (online-video-cutter.com).mp4',
    'media/IMG_6156 (online-video-cutter.com).mp4',
    'media/IMG_4077_1 (online-video-cutter.com).mp4',
    'media/IMG_6412 (online-video-cutter.com).mp4'
]

BOT_TOKEN = '7407529729:AAErOT5NBpMSO-V-HPAW-MDu_1WQt0TtXng'

conn = create_connection(DATABASE_PATH)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    user_data['step'] = 'start'
    logger.info("Starting conversation with user: %s", update.effective_user.id)
    if update.message:
        await update.message.reply_text(
            "Choose your language / Выберите язык / Elige tu idioma",
            reply_markup=language_selection_keyboard()
        )
    elif update.callback_query:
        await update.callback_query.message.reply_text(
            "Choose your language / Выберите язык / Elige tu idioma",
            reply_markup=language_selection_keyboard()
        )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_data = context.user_data
    logger.info("User %s pressed button: %s", update.effective_user.id, query.data)

    if query.data.startswith('lang_'):
        language_code = query.data.split('_')[1]
        user_data['language'] = language_code
        user_data['step'] = 'greeting'

        loading_texts = {
            'en': 'Loading...',
            'ru': 'Ожидай...',
            'es': 'Cargando...',
            'fr': 'Chargement...',
            'uk': 'Завантаження...',
            'pl': 'Ładowanie...',
            'de': 'Laden...',
            'it': 'Caricamento...'
        }
        loading_message = await query.message.reply_text(
            loading_texts.get(language_code, 'Loading...'),
        )

        video_path = random.choice(VIDEO_PATHS)

        if os.path.exists(video_path):
            with open(video_path, 'rb') as video_file:
                await context.bot.send_document(
                    chat_id=update.effective_chat.id,
                    document=video_file,
                    disable_notification=True
                )
                await loading_message.delete()
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Video file not found.")
            await loading_message.delete()

        greeting_texts = {
            'en': 'Hello! What is your name?',
            'ru': 'Привет! Как вас зовут?',
            'es': '¡Hola! ¿Cómo te llamas?',
            'fr': 'Salut! Quel est votre nom ?',
            'uk': 'Привіт! Як вас звати?',
            'pl': 'Cześć! Jak masz na imię?',
            'de': 'Hallo! Wie heißt du?',
            'it': 'Ciao! Come ti chiami?'
        }
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=greeting_texts.get(language_code, 'Hello! What is your name?')
        )

    elif query.data == 'yes':
        if user_data['step'] == 'name_received':
            user_data['step'] = 'calendar'
            await show_calendar(query, user_data.get('month_offset', 0), user_data.get('language', 'en'))
        elif user_data['step'] == 'date_confirmation':
            user_data['step'] = 'time_selection'
            await query.message.reply_text(
                time_selection_headers['start'].get(user_data['language'], "Select start and end time (minimum duration 2 hours)"),
                reply_markup=generate_time_selection_keyboard(user_data['language'], 'start')
            )
        elif user_data['step'] == 'time_confirmation':
            user_data['step'] = 'people_selection'
            await query.message.reply_text(
                people_selection_headers.get(user_data['language'], 'How many people are attending?'),
                reply_markup=generate_person_selection_keyboard(user_data['language'])
            )
        elif user_data['step'] == 'people_confirmation':
            user_data['step'] = 'style_selection'
            await query.message.reply_text(
                party_styles_headers.get(user_data['language'], 'What style do you choose?'),
                reply_markup=generate_party_styles_keyboard(user_data['language'])
            )
        elif user_data['step'] == 'style_confirmation':
            user_data['step'] = 'preferences_request'
            preferences_request_texts = {
                'en': 'Please write your preferences for table setting colors, food items (or exclusions), and desired table accessories (candles, glasses, etc.) - no more than 1000 characters.',
                'ru': 'Напишите свои предпочтения по цвету сервировки и продуктам (или исключения по ним) и желаемые аксессуары сервировки (свечи, бокалы и прочее) - не более 1000 знаков.',
                'es': 'Escriba sus preferencias de colores para la mesa, artículos de comida (o exclusiones), y accesorios de mesa deseados (velas, copas, etc.) - no más de 1000 caracteres.',
                'fr': 'Veuillez écrire vos préférences pour les couleurs de la table, les aliments (ou exclusions), et les accessoires de table désirés (bougies, verres, etc.) - pas plus de 1000 caractères.',
                'uk': 'Напишіть свої уподобання щодо кольору сервіровки та продуктів (або винятки з них) і бажані аксесуары для сервіровки (свічки, келихи тощо) - не більше 1000 знаків.',
                'pl': 'Napisz swoje preferencje dotyczące kolorów nakrycia stołu, produktów spożywczych (lub wyłączeń) i pożądanych akcesoriów stołowych (świece, szklanki itp.) - nie więcej niż 1000 znaków.',
                'de': 'Bitte schreiben Sie Ihre Vorlieben für Tischdeckfarben, Lebensmittel (oder Ausschlüsse) und gewünschte Tischaccessoires (Kerzen, Gläser usw.) - nicht mehr als 1000 Zeichen.',
                'it': 'Scrivi le tue preferenze per i colori della tavola, gli articoli alimentari (o le esclusioni) e gli accessori per la tavola desiderati (candele, bicchieri, ecc.) - non più di 1000 caratteri.'
            }
            await query.message.reply_text(
                preferences_request_texts.get(user_data['language'], "Please write your preferences for table setting colors, food items (or exclusions), and desired table accessories (candles, glasses, etc.) - no more than 1000 characters.")
            )

        await query.edit_message_reply_markup(reply_markup=disable_yes_no_buttons(query.message.reply_markup))

    elif query.data == 'no':
        if user_data['step'] == 'calendar':
            user_data['step'] = 'name_received'
            await handle_name(query, context)
        elif user_data['step'] == 'date_confirmation':
            user_data['step'] = 'calendar'
            await show_calendar(query, user_data.get('month_offset', 0), user_data.get('language', 'en'))
        elif user_data['step'] == 'name_received':
            user_data['step'] = 'greeting'
            await start(update, context)
        elif user_data['step'] == 'time_selection':
            user_data.pop('start_time', None)
            user_data.pop('end_time', None)
            await query.message.reply_text(
                time_selection_headers['start'].get(user_data['language'], "Select start and end time (minimum duration 2 hours)"),
                reply_markup=generate_time_selection_keyboard(user_data['language'], 'start')
            )
        elif user_data['step'] == 'time_confirmation':
            user_data.pop('start_time', None)
            user_data.pop('end_time', None)
            await query.message.reply_text(
                time_selection_headers['start'].get(user_data['language'], "Select start and end time (minimum duration 2 hours)"),
                reply_markup=generate_time_selection_keyboard(user_data['language'], 'start')
            )
        elif user_data['step'] == 'people_selection':
            await query.message.reply_text(
                people_selection_headers.get(user_data['language'], 'How many people are attending?'),
                reply_markup=generate_person_selection_keyboard(user_data['language'])
            )
        elif user_data['step'] == 'people_confirmation':
            user_data['step'] = 'people_selection'
            await query.message.reply_text(
                people_selection_headers.get(user_data['language'], 'How many people are attending?'),
                reply_markup=generate_person_selection_keyboard(user_data['language'])
            )
        elif user_data['step'] == 'style_selection':
            await query.message.reply_text(
                party_styles_headers.get(user_data['language'], 'What style do you choose?'),
                reply_markup=generate_party_styles_keyboard(user_data['language'])
            )
        elif user_data['step'] == 'style_confirmation':
            user_data['step'] = 'style_selection'
            await query.message.reply_text(
                party_styles_headers.get(user_data['language'], 'What style do you choose?'),
                reply_markup=generate_party_styles_keyboard(user_data['language'])
            )

    elif query.data.startswith('date_'):
        selected_date = query.data.split('_')[1]
        user_data['step'] = 'date_confirmation'
        user_data['selected_date'] = selected_date

        await query.edit_message_reply_markup(reply_markup=disable_calendar_buttons(query.message.reply_markup, selected_date))

        confirmation_texts = {
            'en': f'You selected {selected_date}, correct?',
            'ru': f'Вы выбрали {selected_date}, правильно?',
            'es': f'Seleccionaste {selected_date}, ¿correcto?',
            'fr': f'Vous avez sélectionné {selected_date}, correct ?',
            'uk': f'Ви вибрали {selected_date}, правильно?',
            'pl': f'Wybrałeś {selected_date}, poprawne?',
            'de': f'Sie haben {selected_date} gewählt, richtig?',
            'it': f'Hai selezionato {selected_date}, corretto?'
        }
        await query.message.reply_text(
            confirmation_texts.get(user_data['language'], f'You selected {selected_date}, correct?'),
            reply_markup=yes_no_keyboard(user_data['language'])
        )

    elif query.data.startswith('time_'):
        selected_time = query.data.split('_')[1]
        if 'start_time' not in user_data:
            user_data['start_time'] = selected_time
            await query.message.reply_text(
                time_set_texts['start_time'].get(user_data['language'], 'Start time set to {}. Now select end time.').format(selected_time),
                reply_markup=generate_time_selection_keyboard(user_data['language'], 'end', user_data['start_time'])
            )
        else:
            user_data['end_time'] = selected_time
            start_time = datetime.strptime(user_data['start_time'], '%H:%M')
            end_time = datetime.strptime(user_data['end_time'], '%H:%M')
            if (end_time - start_time).seconds >= 7200:
                user_data['step'] = 'time_confirmation'
                await query.message.reply_text(
                    time_set_texts['end_time'].get(user_data['language'], 'End time set to {}. Confirm your selection.').format(selected_time),
                    reply_markup=yes_no_keyboard(user_data.get('language', 'en'))
                )
            else:
                await query.message.reply_text(
                    f"Minimum duration is 2 hours. Please select an end time at least 2 hours after the start time.",
                    reply_markup=generate_time_selection_keyboard(user_data['language'], 'end', user_data['start_time'])
                )
        await query.edit_message_reply_markup(reply_markup=disable_time_buttons(query.message.reply_markup, selected_time))

    elif query.data.startswith('person_'):
        selected_person = query.data.split('_')[1]
        user_data['step'] = 'people_confirmation'
        user_data['selected_person'] = selected_person

        await query.edit_message_reply_markup(reply_markup=disable_person_buttons(query.message.reply_markup, selected_person))

        confirmation_texts = {
            'en': f'You selected {selected_person} people, correct?',
            'ru': f'Вы выбрали {selected_person} человек, правильно?',
            'es': f'Seleccionaste {selected_person} personas, ¿correcto?',
            'fr': f'Vous avez sélectionné {selected_person} personnes, correct ?',
            'uk': f'Ви вибрали {selected_person} людей, правильно?',
            'pl': f'Wybrałeś {selected_person} osób, poprawne?',
            'de': f'Sie haben {selected_person} Personen gewählt, richtig?',
            'it': f'Hai selezionato {selected_person}, corretto?'
        }
        await query.message.reply_text(
            confirmation_texts.get(user_data['language'], f'You selected {selected_person} people, correct?'),
            reply_markup=yes_no_keyboard(user_data['language'])
        )

    elif query.data.startswith('style_'):
        selected_style = query.data.split('_')[1]
        user_data['step'] = 'style_confirmation'
        user_data['selected_style'] = selected_style

        await query.edit_message_reply_markup(reply_markup=disable_style_buttons(query.message.reply_markup, selected_style))

        confirmation_texts = {
            'en': f'You selected {selected_style} style, correct?',
            'ru': f'Вы выбрали стиль {selected_style}, правильно?',
            'es': f'Seleccionaste el estilo {selected_style}, ¿correcto?',
            'fr': f'Vous avez sélectionné le style {selected_style}, correct ?',
            'uk': f'Ви вибрали стиль {selected_style}, правильно?',
            'pl': f'Wybrałeś styl {selected_style}, poprawne?',
            'de': f'Sie haben den Stil {selected_style} gewählt, richtig?',
            'it': f'Hai selezionato lo stile {selected_style}, corretto?'
        }
        await query.message.reply_text(
            confirmation_texts.get(user_data['language'], f'You selected {selected_style} style, correct?'),
            reply_markup=yes_no_keyboard(user_data['language'])
        )

    elif query.data.startswith('prev_month_') or query.data.startswith('next_month_'):
        month_offset = int(query.data.split('_')[2])
        user_data['month_offset'] = month_offset
        await show_calendar(query, month_offset, user_data.get('language', 'en'))

async def show_calendar(query, month_offset, language):
    if month_offset < -1:
        month_offset = -1
    elif month_offset > 2:
        month_offset = 2

    calendar_keyboard = generate_calendar_keyboard(month_offset, language)

    select_date_text = {
        'en': "Select a date:",
        'ru': "Выберите дату:",
        'es': "Seleccione una fecha:",
        'fr': "Sélectionnez une date:",
        'uk': "Виберіть дату:",
        'pl': "Wybierz datę:",
        'de': "Wählen Sie ein Datum:",
        'it': "Seleziona una data:"
    }

    await query.message.reply_text(
        select_date_text.get(language, 'Select a date:'),
        reply_markup=calendar_keyboard
    )

async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    if update.callback_query:
        user_data['name'] = "Имя пользователя"
    else:
        user_data['name'] = update.message.text

    user_data['step'] = 'name_received'

    language_code = user_data.get('language', 'en')

    greeting_texts = {
        'en': f'Hello {user_data["name"]}! Do you want to see available dates?',
        'ru': f'Привет {user_data["name"]}! Хочешь увидеть доступные даты?',
        'es': f'Hola {user_data["name"]}! ¿Quieres ver las fechas disponibles?',
        'fr': f'Bonjour {user_data["name"]}! Voulez-vous voir les dates disponibles?',
        'uk': f'Привіт {user_data["name"]}! Хочеш подивитися які дати доступні?',
        'pl': f'Cześć {user_data["name"]}! Chcesz zobaczyć dostępne daty?',
        'de': f'Hallo {user_data["name"]}! Möchten Sie verfügbare Daten sehen?',
        'it': f'Ciao {user_data["name"]}! Vuoi vedere le date disponibili?'
    }

    if update.message:
        await update.message.reply_text(
            greeting_texts.get(language_code, f'Hello {user_data["name"]}! Do you want to see available dates?'),
            reply_markup=yes_no_keyboard(language_code)
        )
    elif update.callback_query:
        await update.callback_query.message.reply_text(
            greeting_texts.get(language_code, f'Hello {user_data["name"]}! Do you want to see available dates?'),
            reply_markup=yes_no_keyboard(language_code)
        )

def disable_calendar_buttons(reply_markup, selected_date):
    new_keyboard = []
    for row in reply_markup.inline_keyboard:
        new_row = []
        for button in row:
            if button.callback_data and button.callback_data.endswith(selected_date):
                new_row.append(InlineKeyboardButton(f"🔴 {selected_date.split('-')[2]}", callback_data='none'))
            else:
                new_row.append(InlineKeyboardButton(button.text, callback_data='none'))
        new_keyboard.append(new_row)
    return InlineKeyboardMarkup(new_keyboard)

def disable_time_buttons(reply_markup, selected_time):
    new_keyboard = []
    for row in reply_markup.inline_keyboard:
        new_row = []
        for button in row:
            if button.callback_data and button.callback_data.endswith(selected_time):
                new_row.append(InlineKeyboardButton(f"🔴 {selected_time}", callback_data='none'))
            else:
                new_row.append(InlineKeyboardButton(button.text, callback_data='none'))
        new_keyboard.append(new_row)
    return InlineKeyboardMarkup(new_keyboard)

def disable_person_buttons(reply_markup, selected_person):
    new_keyboard = []
    for row in reply_markup.inline_keyboard:
        new_row = []
        for button in row:
            if button.callback_data and button.callback_data.endswith(f'person_{selected_person}'):
                new_row.append(InlineKeyboardButton(f"🔴 {selected_person}", callback_data='none'))
            else:
                new_row.append(InlineKeyboardButton(button.text, callback_data='none'))
        new_keyboard.append(new_row)
    return InlineKeyboardMarkup(new_keyboard)

def disable_style_buttons(reply_markup, selected_style):
    new_keyboard = []
    for row in reply_markup.inline_keyboard:
        new_row = []
        for button in row:
            if button.callback_data and button.callback_data.endswith(f'style_{selected_style}'):
                new_row.append(InlineKeyboardButton(f"🔴 {selected_style}", callback_data='none'))
            else:
                new_row.append(InlineKeyboardButton(button.text, callback_data='none'))
        new_keyboard.append(new_row)
    return InlineKeyboardMarkup(new_keyboard)

def disable_yes_no_buttons(reply_markup):
    new_keyboard = []
    for row in reply_markup.inline_keyboard:
        new_row = []
        for button in row:
            new_row.append(InlineKeyboardButton(button.text, callback_data='none'))
        new_keyboard.append(new_row)
    return InlineKeyboardMarkup(new_keyboard)

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name))

    application.run_polling()
