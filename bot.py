from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
import threading
import os
import requests

def get_crypto_price(symbol):
    symbol_map = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "DOGE": "dogecoin",
        "BNB": "binancecoin"
    }

    if symbol not in symbol_map:
        return None

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol_map[symbol]}&vs_currencies=usd"
    try:
        response = requests.get(url).json()
        price = response[symbol_map[symbol]]["usd"]
        return price
    except:
        return None
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
price = get_crypto_price(text)
if price:
    message = f"✅ قیمت لحظه‌ای {text}: ${price}\nباقی‌مونده رایگان: {user_data[user_id]['free']}"
else:
    message = f"❌ نماد {text} شناخته نشد. لطفاً BTC یا ETH یا DOGE یا BNB وارد کن."

await update.message.reply_text(message)
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
