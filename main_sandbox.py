import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levellevel)s - %(message)s',
    level=logging.DEBUG
)

# Ваш токен
BOT_TOKEN = '7365546887:AAFimfH_lZxsv-v2RyaSktBRk7ww_s5Vs0U'


def generate_calendar_buttons(selected_day=None, disable=False):
    weekdays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    buttons = [[InlineKeyboardButton(day, callback_data=f"weekday_{day}")] for day in weekdays]

    day = 1
    for col in range(5):  # 5 столбцов
        for row in range(7):  # 7 строк (Пн - Вс)
            if day <= 31:
                if str(day) == selected_day:
                    buttons[row].append(InlineKeyboardButton(f"🔴 {day}", callback_data=f"day_{day}"))
                else:
                    text = f"🟢 {day}" if not disable else f"{day}"
                    callback_data = f"day_{day}" if not disable else 'none'
                    buttons[row].append(InlineKeyboardButton(text, callback_data=callback_data))
                day += 1
            else:
                buttons[row].append(InlineKeyboardButton(" ", callback_data="empty"))

    return buttons


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = generate_calendar_buttons()
    message = await update.message.reply_text(
        "Выберите дату:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    context.user_data['last_message_id'] = message.message_id


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_data = context.user_data

    if query.data.startswith('day_'):
        selected_day = query.data.split('_')[1]
        user_data['selected_day'] = selected_day

        # Блокируем все кнопки и отмечаем выбранную дату красным
        buttons = generate_calendar_buttons(selected_day=selected_day, disable=True)
        await query.message.edit_text("Выберите дату:", reply_markup=InlineKeyboardMarkup(buttons))

        # Отправляем сообщение с подтверждением
        await query.message.reply_text(
            f"Вы выбрали {selected_day}. Правильно?",
            reply_markup=yes_no_keyboard(disable=False)
        )

    elif query.data == 'yes':
        # Блокируем "Да" и "Изменить"
        await query.message.edit_reply_markup(reply_markup=yes_no_keyboard(disable=True))

        # Завершаем сценарий
        await query.message.reply_text(
            "Спасибо, тест закончен. Чтобы начать снова, нажмите /start."
        )

    elif query.data == 'no':
        # Возвращаем календарь с активными зелеными кнопками
        buttons = generate_calendar_buttons()
        await query.message.edit_text("Выберите дату:", reply_markup=InlineKeyboardMarkup(buttons))


def yes_no_keyboard(disable=False):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Да", callback_data='yes' if not disable else 'none'),
            InlineKeyboardButton("Изменить", callback_data='no' if not disable else 'none')
        ]
    ])


def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))

    application.run_polling()


if __name__ == "__main__":
    main()
