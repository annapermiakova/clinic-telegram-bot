from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

TOKEN = '7851691095:AAFtAcAPeIM9oAhYo33VINOCtoKu4ZUw6-E'  # ← ваш токен
ADMIN_ID = 5032722703  # ← ваш Telegram ID
AGREEMENT_LINK = 'https://alenushka-pediatr.ru/personal-data-agreement'

# Главное сообщение с кнопками
async def send_confirmation_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_firstname = update.effective_user.first_name or "Уважаемый пациент"

    message = (
        f"👋 Здравствуйте, {user_firstname}!\n\n"
        f"Вы обратились в клинику «Алёнушка».\n"
        f"📄 Ознакомьтесь с нашей политикой обработки персональных данных:\n"
        f"{AGREEMENT_LINK}\n\n"
        f"Вы записаны на приём завтра. Подтвердите, пожалуйста, своё посещение:"
    )

    keyboard = [
        [InlineKeyboardButton("✅ Приду", callback_data='yes')],
        [InlineKeyboardButton("❌ Не приду", callback_data='no')]
    ]

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Ответ на нажатие кнопок
async def button_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
    username = user.username or "без username"

    if query.data == 'yes':
        await query.edit_message_text("✅ Спасибо! Мы вас ждём завтра 👩‍⚕️")
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"✅ Пациент {full_name} (@{username}) подтвердил приём"
        )
    elif query.data == 'no':
        await query.edit_message_text("❌ Спасибо за ответ. При необходимости вы можете записаться повторно.")
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"❌ Пациент {full_name} (@{username}) отменил приём"
        )

# Обработка любого текста (включая смайлик 😊)
async def handle_any_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_confirmation_message(update, context)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", send_confirmation_message))
    app.add_handler(CallbackQueryHandler(button_response))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_any_text))

    print("Бот запущен... Нажмите Ctrl+C для остановки.")
    app.run_polling()

if __name__ == '__main__':
    main()
