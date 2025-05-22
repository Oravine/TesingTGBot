import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    CallbackContext,
)

# Токен бота (замените на свой)
TOKEN = os.getenv("7739154280:AAH_zjCongHGonDj00e-xYRhuji5I-B-s4U")

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Использование: @BotShotBot txt @")

def handle_inline(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data.split(":")
    sender_id = int(data[1])
    recipient_username = data[2]
    message_text = data[3]

    current_user = query.from_user

    # Проверяем, кто нажал на кнопку
    if current_user.username.lower() == recipient_username.lower() or current_user.id == sender_id:
        # Показываем сообщение получателю или отправителю
        query.answer(message_text, show_alert=True)
    else:
        # Остальные получают уведомление
        query.answer("🔒 Это сообщение не для вас", show_alert=True)

def handle_message(update: Update, context: CallbackContext) -> None:
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

    # Убираем "@" из username получателя
    recipient_username = recipient_username[1:]

    # Создаем инлайн-кнопку
    keyboard = [
        [InlineKeyboardButton(
            "📩 Прочитать сообщение",
            callback_data=f"msg:{update.message.from_user.id}:{recipient_username}:{message_text}"
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем сообщение с кнопкой
    update.message.reply_text(
        f"🔒 Личное сообщение для {recipient_username}. Чтобы увидеть его, нажмите на кнопку ниже.",
        reply_markup=reply_markup
    )

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))

    # Обработчик инлайн-кнопок
    dispatcher.add_handler(CallbackQueryHandler(handle_inline))

    # Обработчик текстовых сообщений
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
