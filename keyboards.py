from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def language_selection_keyboard():
    keyboard = [
        [InlineKeyboardButton("English", callback_data='lang_en')],
        [InlineKeyboardButton("Русский", callback_data='lang_ru')]
    ]
    return InlineKeyboardMarkup(keyboard)

def generate_calendar_keyboard():
    # Пример генерации календарной клавиатуры
    keyboard = [[InlineKeyboardButton("1", callback_data='date_1')]]
    return InlineKeyboardMarkup(keyboard)

def generate_time_selection_keyboard():
    # Пример генерации клавиатуры выбора времени
    keyboard = [[InlineKeyboardButton("10:00", callback_data='time_10')]]
    return InlineKeyboardMarkup(keyboard)

def generate_person_selection_keyboard():
    # Пример генерации клавиатуры выбора количества человек
    keyboard = [[InlineKeyboardButton("1", callback_data='persons_1')]]
    return InlineKeyboardMarkup(keyboard)

def generate_party_styles_keyboard():
    # Пример генерации клавиатуры выбора стиля вечеринки
    keyboard = [[InlineKeyboardButton("Casual", callback_data='style_casual')]]
    return InlineKeyboardMarkup(keyboard)
