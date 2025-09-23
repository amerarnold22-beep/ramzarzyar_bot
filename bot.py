from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from flask import Flask
import threading
import os

# گرفتن توکن از محیط
TOKEN = os.getenv("BOT_TOKEN")

# هندلر دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ ربات فعاله و جواب داد!")

# اجرای ربات در یک Thread جدا
def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

# اجرای Flask برای باز نگه داشتن پورت
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "✅ Bot is running on Render!"

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    flask_app.run(host='0.0.0.0', port=10000)
