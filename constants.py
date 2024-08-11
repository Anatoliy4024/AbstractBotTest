import os

# Путь к базе данных SQLite
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'sqlite.db')

# Заголовки для выбора времени
time_selection_headers = {
    'start': {
        'en': "Select start and end time (minimum duration 2 hours)",
        'ru': "Выберите начальное и конечное время (минимальная продолжительность 2 часа)"
    },
    'end': {
        'en': "Select the end time",
        'ru': "Выберите конечное время"
    }
}

# Заголовки для выбора количества людей
people_selection_headers = {
    'en': "How many people are attending?",
    'ru': "Сколько человек будет присутствовать?"
}

# Заголовки для выбора стиля мероприятия
party_styles_headers = {
    'en': "What style do you choose?",
    'ru': "Какой стиль вы выбираете?"
}

# Заголовки для выбора города
city_selection_headers = {
    'en': "Select your city",
    'ru': "Выберите ваш город"
}

# Заголовки для выбора предпочтений
preferences_headers = {
    'en': "Please specify your preferences",
    'ru': "Укажите ваши предпочтения"
}

# Статусы пользователей
user_statuses = {
    'active': 1,
    'inactive': 0
}

# Статусы заказов
order_statuses = {
    'pending': 0,
    'confirmed': 1,
    'canceled': 2
}

# Словарь всех возможных заголовков для удобства
all_headers = {
    'time_selection': time_selection_headers,
    'people_selection': people_selection_headers,
    'party_styles': party_styles_headers,
    'city_selection': city_selection_headers,
    'preferences': preferences_headers
}

# Класс для хранения временных данных
class TemporaryData:
    def __init__(self):
        self.user_name = None
        self.city = None
        self.preferences = None
        self.language = None  # Поддержка языка

    def set_user_name(self, user_name):
        self.user_name = user_name

    def get_user_name(self):
        return self.user_name

    def clear_user_name(self):
        self.user_name = None

    def set_city(self, city):
        self.city = city

    def get_city(self):
        return self.city

    def clear_city(self):
        self.city = None

    def set_preferences(self, preferences):
        self.preferences = preferences

    def get_preferences(self):
        return self.preferences

    def clear_preferences(self):
        self.preferences = None

    def set_language(self, language):
        self.language = language  # Метод для установки языка

    def get_language(self):
        return self.language  # Метод для получения языка

    def clear_language(self):
        self.language = None  # Метод для очистки языка
