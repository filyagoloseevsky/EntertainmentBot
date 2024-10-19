import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# Увімкнення логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Список постів
posts = []


# Функція для додавання посту
async def add_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    posts.append(text)
    await update.message.reply_text('Пост додано!')


# Стартова команда бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Місце для прогулянок", callback_data='walk')],
        [InlineKeyboardButton("Випити", callback_data='drink')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Виберіть категорію:', reply_markup=reply_markup)


# Обробка натискання кнопок
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'walk':
        await query.edit_message_text(text="Пости для прогулянок:\n" + get_posts_by_tag('#напрогулянку'))
    elif query.data == 'drink':
        await query.edit_message_text(text="Пости для випивки:\n" + get_posts_by_tag('#випити'))


# Функція для отримання постів за тегом
def get_posts_by_tag(tag):
    filtered_posts = [post for post in posts if tag in post]
    if not filtered_posts:
        return "Немає постів для цієї категорії."
    return "\n".join(filtered_posts)


# Головна функція для запуску бота
def main():
    # Замініть 'YOUR_BOT_TOKEN' на ваш токен від BotFather
    application = Application.builder().token('8106761998:AAEnNooCBgtwzwrOuGle-456r9Hr-nO-fb4').build()

    # Налаштування команд
    application.bot.set_my_commands([
        ('start', 'Запустити бота')
    ])

    # Команда /start
    application.add_handler(CommandHandler("start", start))
    # Обробка текстових повідомлень для додавання постів
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add_post))
    # Обробка натискання кнопок
    application.add_handler(CallbackQueryHandler(button))

    # Запуск бота
    application.run_polling(timeout=30)


if __name__ == '__main__':
    main()