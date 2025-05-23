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
    CallbackQueryHandler,
    CallbackContext,
    InlineQueryHandler
)

TOKEN = os.getenv("BOT_TOKEN")

def start(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /start"""
    update.message.reply_text("Бот работает через инлайн режим: @PM_ChBot")

def handle_inline_button(update: Update, context: CallbackContext) -> None:
    """Обработчик нажатий на инлайн-кнопки"""
    query = update.callback_query
    data = query.data.split(":")
    
    if len(data) != 4:
        query.answer("❌ Ошибка: неверные данные кнопки")
        return

    _, sender_id, recipient_username, message_text = data
    current_user = query.from_user

    try:
        sender_id = int(sender_id)
    except ValueError:
        query.answer("❌ Ошибка: неверный ID отправителя")
        return

    # Проверяем, кто нажал на кнопку (отправитель или получатель)
    if (current_user.username and current_user.username.lower() == recipient_username.lower()) or current_user.id == sender_id:
        query.answer(message_text, show_alert=True)
    else:
        query.answer("⚠️🔒 Это сообщение не для вас.", show_alert=True)

def handle_inline_query(update: Update, context: CallbackContext) -> None:
    """Обработчик инлайн-запросов"""
    query_text = update.inline_query.query.strip()
    
    if not query_text:
        return

    # Разбиваем запрос на получателя и сообщение
    parts = query_text.split(maxsplit=1)
    if len(parts) < 2:
        return

    recipient_username, message_text = parts
    recipient_username = recipient_username.lstrip('@')  # Удаляем @ если есть

    # Создаем результат для инлайн-режима
    results = [
        InlineQueryResultArticle(
            id="1",
            title=f"Отправить {recipient_username}",
            description=message_text[:100],  # Показываем начало сообщения
            input_message_content=InputTextMessageContent(
                f"**🔒 Личное сообщение для @{recipient_username}.**\nНажмите кнопку ниже, чтобы прочитать его. __Сообщение увидите только вы.__"
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
    dispatcher.add_handler(CallbackQueryHandler(handle_inline_button))
    dispatcher.add_handler(InlineQueryHandler(handle_inline_query))

    # Запускаем бота
    print("Бот запущен...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
