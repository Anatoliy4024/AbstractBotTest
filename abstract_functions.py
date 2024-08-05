from telegram import InlineKeyboardMarkup, InlineKeyboardButton

# Постоянные функции для создания кнопок
def A(update, context, confirmation_text):
    query = update.callback_query
    query.answer()
    user_data = context.user_data
    user_data['last_confirmation_text'] = confirmation_text

    query.message.reply_text(
        confirmation_text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Да", callback_data='yes')],
            [InlineKeyboardButton("Назад", callback_data='no')]
        ])
    )

def B(update, context, next_module):
    query = update.callback_query
    query.answer()

    query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([]))
    next_module(update, context)

def C(update, context, current_module):
    query = update.callback_query
    query.answer()

    current_module(update, context)

def C_combined(update, context, confirmation_text, next_module, current_module):
    A(update, context, confirmation_text)
    B(update, context, next_module)
    C(update, context, current_module)
