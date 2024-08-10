from telegram import InlineKeyboardButton

def generate_calendar_buttons():
    days_of_week = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    days_in_month = 31
    calendar_buttons = []

    # Инициализируем строки календаря: первая колонка — дни недели
    for day in days_of_week:
        calendar_buttons.append([InlineKeyboardButton(text=day, callback_data='none')])

    # Теперь заполняем оставшиеся колонки числами от 1 до 31
    current_day = 1
    for col in range(6):  # У нас 6 колонок для чисел
        for row in range(7):  # У нас 7 строк (понедельник - воскресенье)
            if current_day <= days_in_month:
                calendar_buttons[row].append(InlineKeyboardButton(text=f"🔵 {current_day}", callback_data='none'))
                current_day += 1
            else:
                # Если дни закончились, больше не добавляем пустые кнопки
                calendar_buttons[row].append(InlineKeyboardButton(text=" ", callback_data='none'))

    # Удаляем последнюю пустую колонку, если она полностью пустая
    for row in range(7):
        if len(calendar_buttons[row]) > 6:
            calendar_buttons[row] = calendar_buttons[row][:7]

    return calendar_buttons
