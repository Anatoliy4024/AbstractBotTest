from telegram import Update
from telegram.ext import ContextTypes
from keyboards import yes_no_keyboard, generate_calendar_keyboard, generate_time_selection_keyboard, generate_person_selection_keyboard, generate_party_styles_keyboard

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    step = user_data.get('step', '')

    if step == 'greeting':
        await handle_name(update, context)
    elif step == 'preferences_request':
        await handle_preferences(update, context)
    else:
        await update.message.reply_text(
            "Выбор только кнопками",
            reply_markup=get_current_step_keyboard(step, user_data)
        )

# Функция для обработки имени
async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
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

    await update.message.reply_text(
        greeting_texts.get(language_code, f'Hello {user_data["name"]}! Do you want to see available dates?'),
        reply_markup=yes_no_keyboard(language_code)
    )

# Функция для обработки предпочтений
async def handle_preferences(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    user_data['preferences'] = update.message.text

    user_data['step'] = 'preferences_received'

    language_code = user_data.get('language', 'en')

    confirmation_texts = {
        'en': 'Your preferences have been saved.',
        'ru': 'Ваши предпочтения сохранены.',
        'es': 'Tus preferencias han sido guardadas.',
        'fr': 'Vos préférences ont été enregistrées.',
        'uk': 'Ваші уподобання збережено.',
        'pl': 'Twoje preferencje zostały zapisane.',
        'de': 'Ihre Vorlieben wurden gespeichert.',
        'it': 'Le tue preferenze sono state salvate.'
    }

    await update.message.reply_text(
        confirmation_texts.get(language_code, 'Your preferences have been saved.')
    )

# Функция для получения текущей клавиатуры для шага
def get_current_step_keyboard(step, user_data):
    language = user_data.get('language', 'en')
    if step == 'calendar':
        month_offset = user_data.get('month_offset', 0)
        return generate_calendar_keyboard(month_offset, language)
    elif step == 'time_selection':
        return generate_time_selection_keyboard(language, 'start')
    elif step == 'people_selection':
        return generate_person_selection_keyboard(language)
    elif step == 'style_selection':
        return generate_party_styles_keyboard(language)
    else:
        return None
