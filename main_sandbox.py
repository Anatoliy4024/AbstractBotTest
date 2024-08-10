import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

# Ваш токен
BOT_TOKEN = '7365546887:AAFimfH_lZxsv-v2RyaSktBRk7ww_s5Vs0U'


def generate_calendar_buttons():
    weekdays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    buttons = [[InlineKeyboardButton(day, callback_data=f"weekday_{day}")] for day in weekdays]

    day = 1
    for col in range(5):  # 5 столбцов
        for row in range(7):  # 7 строк (Пн - Вс)
            if day <= 31:
                buttons[row].append(InlineKeyboardButton(f"🔵 {day}", callback_data=f"day_{day}"))
                day += 1
            else:
                buttons[row].append(InlineKeyboardButton(" ", callback_data="empty"))

    return buttons


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = generate_calendar_buttons()
    await update.message.reply_text(
        "Here are your buttons:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    application.run_polling()


if __name__ == "__main__":
    main()
