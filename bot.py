from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8325004172:AAGEiM3hhUhW4BCk21gvWTeSnvVZF5TUUXw"

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {"free": 3, "subscribed": False}
    await update.message.reply_text("👋 خوش اومدی! ۳ تحلیل رایگان داری. اسم رمزارز رو بفرست.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.upper()

    if user_id not in user_data:
        user_data[user_id] = {"free": 3, "subscribed": False}

    if user_data[user_id]["free"] > 0:
        user_data[user_id]["free"] -= 1
        await update.message.reply_text(f"✅ تحلیل {text} ارسال شد. باقی‌مونده رایگان: {user_data[user_id]['free']}")
    elif user_data[user_id]["subscribed"]:
        await update.message.reply_text(f"✅ تحلیل {text} ارسال شد (اشتراک فعال)")
    else:
        await update.message.reply_text("🚫 تحلیل رایگان تموم شد.\n➤ پرداخت ۱۰۰۰ تومان برای هر تحلیل\n➤ یا پرداخت ۱۰ هزار تومان برای اشتراک ماهانه")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
