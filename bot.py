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
    help_text = '<b>Используйте бота в инлайн режиме!</b>\n\nНапишите в любой чат:\n<pre>@Druobot [получатель] [сообщение]</pre>'
    update.message.reply_text(help_text, parse_mode='HTML')

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

    # Проверяем, кто нажал на кнопку
    if (current_user.username and current_user.username.lower() == recipient_username.lower()) or current_user.id == sender_id:
        query.answer(message_text, show_alert=True)  # Теперь без форматирования
    else:
        query.answer("🔒 Это сообщение не для вас", show_alert=True)

def handle_inline_query(update: Update, context: CallbackContext) -> None:
    """Обработчик инлайн-запросов"""
    query_text = update.inline_query.query.strip()
    
    if not query_text:
        return

    parts = query_text.split(maxsplit=1)
    if len(parts) < 2:
        return

    recipient_username, message_text = parts
    recipient_username = recipient_username.lstrip('@')

    # Форматируем текст для инлайн-режима с HTML
    formatted_text = f'<b>🔒 Личное сообщение для @{recipient_username}</b>\nЧтобы прочитать его, нажмите кнопку ниже. <i>Сообщение увидите только вы.</i>'
    results = [
        InlineQueryResultArticle(
            id="1",
            title=f"Отправить {recipient_username}",
            description=message_text[:100],
            input_message_content=InputTextMessageContent(
                formatted_text,
                parse_mode='HTML'
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
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(handle_inline_button))
    dispatcher.add_handler(InlineQueryHandler(handle_inline_query))

    print("Бот запущен...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
