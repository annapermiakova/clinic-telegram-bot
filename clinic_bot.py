from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = '7786203942:AAFTGMQqvCcg05kUFG3SNrbadVNzr1hyVyg'
AGREEMENT_LINK = 'https://alenushka-pediatr.ru/personal-data-agreement'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    await update.message.reply_text(message, reply_markup=InlineKeyboardMarkup(keyboard))

async def button_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'yes':
        await query.edit_message_text("✅ Спасибо! Мы вас ждём завтра 👩‍⚕️")
    elif query.data == 'no':
        await query.edit_message_text("❌ Спасибо за ответ. При необходимости вы можете записаться повторно.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_response))
    print("Бот запущен... Нажмите Ctrl+C для остановки.")
    app.run_polling()

if __name__ == '__main__':
    main()
