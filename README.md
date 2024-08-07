# Event Organization Bot

## 1. Суть проекта
Проект направлен на автоматическое администрирование организации ивентов. Пользователи взаимодействуют с ботом Telegram, чтобы планировать мероприятия, выбирая даты, время, количество участников, стиль вечеринки и прочие предпочтения.

## 2. Файловая структура
Проект состоит из следующих файлов и директорий:
- `main.py`: Основной файл, запускающий бота и обрабатывающий взаимодействие с пользователями.
- `database_logger.py`: Модуль для логирования операций с базой данных.
- `abstract_functions.py`: Модуль, содержащий вспомогательные функции для работы с базой данных.
- `keyboards.py`: Модуль, создающий различные клавиатуры для взаимодействия с пользователем.
- `view_database.py`: Модуль для просмотра данных из базы данных.
- `user_sessions.db`: Файл базы данных SQLite, где хранятся сессии пользователей.
- `message_handlers.py`: Модуль для обработки сообщений и команд.
- `media/`: Директория с видеороликами для приветствия пользователей.

## 3. Архитектура

### 3.1 Принцип каскадности
Принцип каскадности используется для разделения модулей на переменные и постоянные абстракции:
- **Переменные абстракции** учитывают пожелания пользователя и предлагают выбор из различных опций (например, язык, дата, время и т.д.).
- **Постоянные абстракции** выполняют одно повторяющееся действие, такое как запрос подтверждения действия (например, "Введите имя", "Вы выбрали...") и кнопки "Да" и "Нет".

Всего имеется: *на момент разработки документации - 7.08.2024 (предполагается еще 2 переменных и 2 постоянных)
- Переменных абстракций: 7
- Постоянных абстракций: 6

### 3.2 Перечень модулей с их названиями

1. **Модуль 1** (Переменный)
   - Название: `language_selection`
   - Описание: Выбор языка пользователем.
   - Функции: `language_selection_keyboard()`

2. **Модуль 2** (Постоянный)
   - Название: `greeting`
   - Описание: Приветствие пользователю и запрос имени с последующим вопросом .
   - Функции: `handle_name()`

3. **Модуль 3** (Переменный)
   - Название: `date_selection`
   - Описание: Выбор даты мероприятия.
   - Функции: `generate_calendar_keyboard()`, `show_calendar()`

4. **Модуль 4** (Постоянный)
   - Название: `date_confirmation`
   - Описание: Подтверждение выбранной даты.
   - Функции: `disable_calendar_buttons()`

5. **Модуль 5** (Переменный)
   - Название: `time_selection`
   - Описание: Выбор времени мероприятия.
   - Функции: `generate_time_selection_keyboard()`

6. **Модуль 6** (Постоянный)
   - Название: `time_confirmation`
   - Описание: Подтверждение выбранного времени.
   - Функции: `disable_time_buttons()`

7. **Модуль 7** (Переменный)
   - Название: `people_selection`
   - Описание: Выбор количества участников.
   - Функции: `generate_person_selection_keyboard()`

8. **Модуль 8** (Постоянный)
   - Название: `people_confirmation`
   - Описание: Подтверждение количества участников.
   - Функции: `disable_person_buttons()`

9. **Модуль 9** (Переменный)
   - Название: `style_selection`
   - Описание: Выбор стиля мероприятия.
   - Функции: `generate_party_styles_keyboard()`

10. **Модуль 10** (Постоянный)
    - Название: `style_confirmation`
    - Описание: Подтверждение выбранного стиля.
    - Функции: `disable_style_buttons()`

11. **Модуль 11** (Переменный)
    - Название: `preferences_request`
    - Описание: Запрос предпочтений пользователя.
    - Функции: `handle_preferences()`

12. **Модуль 12** (Переменный)
    - Название: `city_request`
    - Описание: Запрос города проведения мероприятия.
    - Функции: `handle_city()`

13. **Модуль 13** (Постоянный)
    - Название: `city_confirmation`
    - Описание: Подтверждение введенного города.
    - Функции: `handle_city_confirmation()`

### 3.3 Принцип взаимодействия файлов

1. **main.py**: Основной файл, запускающий бота и обрабатывающий все взаимодействия с пользователем.
2. **database_logger.py**: Содержит функции для логирования операций с базой данных.
3. **abstract_functions.py**: Вспомогательные функции для работы с базой данных.
4. **keyboards.py**: Функции для создания клавиатур в Telegram.
5. **message_handlers.py**: Содержит обработчики сообщений и команд.
6. **view_database.py**: Модуль для просмотра данных в базе данных.
7. **user_sessions.db**: Файл базы данных SQLite, где хранятся сессии пользователей.
8. **media/**: Директория с видеороликами для приветствия пользователей.

## 4. Перечень функций

- `create_connection(db_file)`: Создает соединение с базой данных SQLite.
- `execute_query_with_logging(conn, query, params=())`: Выполняет SQL-запрос с логированием.
- `log_message(message)`: Логирует сообщение.
- `log_query(query, params=())`: Логирует SQL-запрос.
- `generate_calendar_keyboard(month_offset=0, language='en')`: Генерирует клавиатуру с календарем.
- `generate_time_selection_keyboard(language, stage='start', start_time=None)`: Генерирует клавиатуру для выбора времени.
- `language_selection_keyboard()`: Генерирует клавиатуру для выбора языка.
- `yes_no_keyboard(language)`: Генерирует клавиатуру с кнопками "Да" и "Нет".
- `generate_person_selection_keyboard(language)`: Генерирует клавиатуру для выбора количества участников.
- `generate_party_styles_keyboard(language)`: Генерирует клавиатуру для выбора стиля мероприятия.
- `handle_name(update, context)`: Обрабатывает ввод имени пользователя.
- `show_calendar(query, month_offset, language)`: Показывает календарь для выбора даты.
- `disable_calendar_buttons(reply_markup, selected_date)`: Деактивирует кнопки календаря.
- `disable_time_buttons(reply_markup, selected_time)`: Деактивирует кнопки времени.
- `disable_person_buttons(reply_markup, selected_person)`: Деактивирует кнопки количества участников.
- `disable_style_buttons(reply_markup, selected_style)`: Деактивирует кнопки стиля.
- `disable_yes_no_buttons(reply_markup)`: Деактивирует кнопки "Да" и "Нет".
- `handle_preferences(update, context)`: Обрабатывает ввод предпочтений пользователя.
- `handle_city(update, context)`: Обрабатывает ввод города проведения мероприятия.
- `handle_city_confirmation(update, context)`: Подтверждает введенный город.