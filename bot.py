import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent
)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    CallbackContext,
    InlineQueryHandler
)

# Токен бота
TOKEN = os.getenv("BOT_TOKEN")

def start(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /start"""
    update.message.reply_text("Использование: @BotShotBot txt @")

def handle_inline(update: Update, context: CallbackContext) -> None:
    """Обработчик нажатий на инлайн-кнопки"""
    query = update.callback_query
    data = query.data.split(":")
    
    if len(data) < 4:
        query.answer("❌ Ошибка: неверные данные кнопки")
        return

    _, sender_id, recipient_username, message_text = data[:4]
    current_user = query.from_user

    try:
        sender_id = int(sender_id)
    except ValueError:
        query.answer("❌ Ошибка: неверный ID отправителя")
        return

    # Проверяем, кто нажал на кнопку
    if (current_user.username and current_user.username.lower() == recipient_username.lower()) or current_user.id == sender_id:
        query.answer(message_text, show_alert=True)
    else:
        query.answer("🔒 Это сообщение не для вас", show_alert=True)

def handle_message(update: Update, context: CallbackContext) -> None:
    """Обработчик обычных текстовых сообщений"""
    text = update.message.text.strip()
    parts = text.split()

    if len(parts) < 3 or not parts[0].startswith("@"):
        update.message.reply_text("❌ Неверный формат. Используйте: @BotShotBot @получатель сообщение")
        return

    bot_username, recipient_username, *message_parts = parts
    message_text = " ".join(message_parts)

    if not recipient_username.startswith("@"):
        update.message.reply_text("❌ Укажите username получателя через @ (например, @username)")
        return

    recipient_username = recipient_username[1:]  # Убираем "@"

    keyboard = [[
        InlineKeyboardButton(
            "📩 Прочитать сообщение",
            callback_data=f"msg:{update.message.from_user.id}:{recipient_username}:{message_text}"
        )
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        f"🔒 Личное сообщение для {recipient_username}. Чтобы увидеть его, нажмите на кнопку ниже.",
        reply_markup=reply_markup
    )

def inline_query(update: Update, context: CallbackContext) -> None:
    """Обработчик инлайн-режима"""
    query = update.inline_query.query
    if not query:
        return

    parts = query.split(maxsplit=1)
    if len(parts) < 2:
        return

    recipient_username, message_text = parts

    results = [
        InlineQueryResultArticle(
            id="1",
            title=f"Отправить {recipient_username}",
            description=message_text[:50],
            input_message_content=InputTextMessageContent(
                f"🔒 Личное сообщение для {recipient_username}. Нажмите кнопку ниже."
            ),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    "📩 Прочитать сообщение",
                    callback_data=f"msg:{update.inline_query.from_user.id}:{recipient_username}:{message_text}"
                )
            ]])
        )
    ]

    update.inline_query.answer(results)

def main() -> None:
    """Основная функция запуска бота"""
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Регистрируем обработчики
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(handle_inline))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dispatcher.add_handler(InlineQueryHandler(inline_query))

    # Запускаем бота
    print("Бот запущен...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
