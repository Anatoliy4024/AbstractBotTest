from telegram import Update
from telegram.ext import ContextTypes
from keyboards import yes_no_keyboard, generate_calendar_keyboard, generate_time_selection_keyboard, generate_person_selection_keyboard, generate_party_styles_keyboard
from constants import UserData


# Обработчик текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data.get('user_data', UserData())
    context.user_data['user_data'] = user_data
    step = user_data.get_step()

    if step == 'greeting':
        await handle_name(update, context)
    elif step == 'preferences_request':
        await handle_preferences(update, context)
    elif step == 'city_request':
        await handle_city(update, context)
    else:
        await update.message.reply_text(
            get_translation(user_data, 'buttons_only'),  # Используем функцию для получения перевода
            reply_markup=get_current_step_keyboard(step, user_data)
        )

# Функция для обработки имени
async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data.get('user_data', UserData())
    user_data.set_name(update.message.text)
    user_data.set_step('name_received')
    context.user_data['user_data'] = user_data

    language_code = user_data.get_language()

    greeting_texts = {
        'en': f'Hello {user_data.get_name()}! Do you want to see available dates?',
        'ru': f'Привет {user_data.get_name()}! Хочешь увидеть доступные даты?',
        'es': f'¡Hola {user_data.get_name()}! ¿Quieres ver las fechas disponibles?',
        'fr': f'Bonjour {user_data.get_name()}! Voulez-vous voir les dates disponibles?',
        'uk': f'Привіт {user_data.get_name()}! Хочеш подивитися доступні дати?',
        'pl': f'Cześć {user_data.get_name()}! Chcesz zobaczyć dostępne daty?',
        'de': f'Hallo {user_data.get_name()}! Möchten Sie verfügbare Daten sehen?',
        'it': f'Ciao {user_data.get_name()}! Vuoi vedere le date disponibili?'
    }

    await update.message.reply_text(
        greeting_texts.get(language_code, f'Hello {user_data.get_name()}! Do you want to see available dates?'),
        reply_markup=yes_no_keyboard(language_code)
    )


# Функция для обработки предпочтений
async def handle_preferences(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data.get('user_data', UserData())
    user_data.set_preferences(update.message.text)
    user_data.set_step('preferences_received')
    context.user_data['user_data'] = user_data

    language_code = user_data.get_language()

    city_request_texts = {
        'en': 'Please specify the city for the event.',
        'ru': 'Пожалуйста укажите город проведения ивента.',
        'es': 'Por favor, especifique la ciudad para el evento.',
        'fr': 'Veuillez indiquer la ville pour l\'événement.',
        'uk': 'Будь ласка, вкажіть місто проведення івенту.',
        'pl': 'Proszę podać miasto, w którym odbędzie się wydarzenie.',
        'de': 'Bitte geben Sie die Stadt für die Veranstaltung an.',
        'it': 'Si prega di specificare la città per l\'evento.'
    }

    await update.message.reply_text(
        city_request_texts.get(language_code, 'Please specify the city for the event.')
    )
    user_data.set_step('city_request')


# Функция для обработки города
async def handle_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data.get('user_data', UserData())
    user_data.set_city(update.message.text)
    context.user_data['user_data'] = user_data

    language_code = user_data.get_language()

    confirmation_texts = {
        'en': f'City: {user_data.get_city()}, correct?',
        'ru': f'Город: {user_data.get_city()}, правильно?',
        'es': f'Ciudad: {user_data.get_city()}, ¿correcto?',
        'fr': f'Ville: {user_data.get_city()}, correct ?',
        'uk': f'Місто: {user_data.get_city()}, правильно?',
        'pl': f'Miasto: {user_data.get_city()}, poprawne?',
        'de': f'Stadt: {user_data.get_city()}, richtig?',
        'it': f'Città: {user_data.get_city()}, corretto?'
    }

    await update.message.reply_text(
        confirmation_texts.get(language_code, f'City: {user_data.get_city()}, correct?'),
        reply_markup=yes_no_keyboard(language_code)
    )
    user_data.set_step('city_confirmation')


async def handle_city_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data.get('user_data', UserData())
    if user_data.get_step() == 'city_confirmation':
        language_code = user_data.get_language()

        confirmation_texts = {
            'en': f'{user_data.get_name()}, your data has been saved. Calculating the cost for the proforma invoice.',
            'ru': f'{user_data.get_name()}, ваши данные сохранены. Рассчитываем стоимость для выдачи вам проформы.',
            'es': f'{user_data.get_name()}, sus datos han sido guardados. Calculando el costo para emitir la proforma.',
            'fr': f'{user_data.get_name()}, vos données ont été sauvegardées. Calcul du coût pour l\'émission de la facture proforma.',
            'uk': f'{user_data.get_name()}, ваші дані збережено. Розраховуємо вартість для видачі вам проформи.',
            'pl': f'{user_data.get_name()}, twoje dane zostały zapisane. Obliczanie kosztu wystawienia proformy.',
            'de': f'{user_data.get_name()}, Ihre Daten wurden gespeichert. Berechnung der Kosten für die Proformarechnung.',
            'it': f'{user_data.get_name()}, i tuoi dati sono stati salvati. Calcolo del costo per l\'emissione della fattura proforma.'
        }

        await update.message.reply_text(
            confirmation_texts.get(language_code,
                                   f'{user_data.get_name()}, your data has been saved. Calculating the cost for the proforma invoice.')
        )
        user_data.set_step('data_saved')


# Функция для получения текущей клавиатуры для шага
def get_current_step_keyboard(step, user_data):
    language = user_data.get_language()
    if step == 'calendar':
        month_offset = user_data.get_month_offset() if hasattr(user_data, 'get_month_offset') else 0
        return generate_calendar_keyboard(month_offset, language)
    elif step == 'time_selection':
        return generate_time_selection_keyboard(language, 'start')
    elif step == 'people_selection':
        return generate_person_selection_keyboard(language)
    elif step == 'style_selection':
        return generate_party_styles_keyboard(language)
    else:
        return None


# Словарь с переводами сообщения "Выбор только кнопками" на разные языки
translations = {
    'en': "Please use the buttons",
    'ru': "Выбор только кнопками",
    'es': "Por favor, usa los botones",
    'fr': "Veuillez utiliser les boutons",
    'de': "Bitte verwenden Sie die Tasten",
    'it': "Si prega di utilizzare i pulsanti",
    'uk': "Будь ласка, використовуйте кнопки",
    'pl': "Proszę użyć przycisków"
}

# Функция для получения перевода на основе языка пользователя
def get_translation(user_data, key):
    language_code = user_data.get_language()  # Получаем код языка пользователя
    return translations.get(language_code, translations['en'])  # Возвращаем перевод или английский по умолчанию
