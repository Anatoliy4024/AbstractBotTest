import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'sqlite.db')

#Создание класса TemporaryData, который будет хранить временные данные, такие как user_name, city, и preferences.

class TemporaryData:
    def __init__(self):
        self.user_name = None
        self.city = None
        self.preferences = None

    def set_user_name(self, user_name):
        self.user_name = user_name

    def get_user_name(self):
        return self.user_name

    def clear_user_name(self):
        self.user_name = None

    # Аналогичные методы для city и preferences
