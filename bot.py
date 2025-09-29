from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
import threading
import os

# گرفتن توکن از محیط
TOKEN = os.getenv("BOT_TOKEN")

# حافظه موقت کاربران
user_data = {}

# هندلر دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {"free": 3, "subscribed": False}
    await update.message.reply_text("👋 خوش اومدی! ۳ تحلیل رایگان داری. اسم رمزارز رو بفرست مثل BTC یا ETH")

# هندلر پیام‌های رمزارز
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
        await update.message.reply_text(
            "🚫 تحلیل رایگان تموم شد.\n"
            "💳 برای ادامه:\n"
            "➤ پرداخت ۱۰۰۰ تومان برای هر تحلیل\n"
            "➤ یا پرداخت ۱۰ هزار تومان برای اشتراک ماهانه\n"
            "📲 برای پرداخت، بزودی لینک زرین‌پال اضافه می‌شه"
        )

# اجرای ربات در یک Thread جدا
def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

# اجرای Flask برای باز نگه داشتن پورت
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "✅ Bot is running on Render!"

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    flask_app.run(host='0.0.0.0', port=10000)
