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
    elif step == 'city_request':
        await handle_city(update, context)
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

    city_request_texts = {
        'en': 'Please specify the city for the event.',
        'ru': 'Пожалуйста укажите город проведение Ивента.',
        'es': 'Por favor especifique la ciudad para el evento.',
        'fr': 'Veuillez indiquer la ville pour l\'événement.',
        'uk': 'Будь ласка, вкажіть місто проведення івенту.',
        'pl': 'Proszę podać miasto na wydarzenie.',
        'de': 'Bitte geben Sie die Stadt für die Veranstaltung an.',
        'it': 'Si prega di specificare la città per l\'evento.'
    }

    await update.message.reply_text(
        city_request_texts.get(language_code, 'Please specify the city for the event.')
    )
    user_data['step'] = 'city_request'

# Функция для обработки города
async def handle_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    user_data['city'] = update.message.text

    language_code = user_data.get('language', 'en')

    confirmation_texts = {
        'en': f'City: {user_data["city"]}, correct?',
        'ru': f'Город: {user_data["city"]}, правильно?',
        'es': f'Ciudad: {user_data["city"]}, ¿correcto?',
        'fr': f'Ville: {user_data["city"]}, correct?',
        'uk': f'Місто: {user_data["city"]}, правильно?',
        'pl': f'Miasto: {user_data["city"]}, poprawne?',
        'de': f'Stadt: {user_data["city"]}, richtig?',
        'it': f'Città: {user_data["city"]}, corretto?'
    }

    await update.message.reply_text(
        confirmation_texts.get(language_code, f'City: {user_data["city"]}, correct?'),
        reply_markup=yes_no_keyboard(language_code)
    )
    user_data['step'] = 'city_confirmation'

async def handle_city_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    if user_data.get('step') == 'city_confirmation':
        language_code = user_data.get('language', 'en')

        confirmation_texts = {
            'en': f'{user_data["name"]}, your data has been saved. Calculating the cost for the proforma invoice.',
            'ru': f'{user_data["name"]}, ваши данные сохранены. Рассчитываем стоимость для выдачи вам проформы.',
            'es': f'{user_data["name"]}, sus datos han sido guardados. Calculando el costo para emitir la proforma.',
            'fr': f'{user_data["name"]}, vos données ont été sauvegardées. Calcul du coût pour l\'émission de la facture proforma.',
            'uk': f'{user_data["name"]}, ваші дані збережено. Розраховуємо вартість для видачі вам проформи.',
            'pl': f'{user_data["name"]}, twoje dane zostały zapisane. Obliczanie kosztu wystawienia proformy.',
            'de': f'{user_data["name"]}, Ihre Daten wurden gespeichert. Berechnung der Kosten für die Proformarechnung.',
            'it': f'{user_data["name"]}, i tuoi dati sono stati salvati. Calcolo del costo per l\'emissione della fattura proforma.'
        }

        await update.message.reply_text(
            confirmation_texts.get(language_code, f'{user_data["name"]}, your data has been saved. Calculating the cost for the proforma invoice.')
        )
        user_data['step'] = 'data_saved'

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
