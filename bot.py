from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
import threading
import os
import requests

TOKEN = os.getenv("BOT_TOKEN")
user_data = {}

# گرفتن شناسه‌ی CoinGecko برای نماد رمزارز
def get_coin_id(symbol):
    url = "https://api.coingecko.com/api/v3/coins/list"
    try:
        response = requests.get(url).json()
        for coin in response:
            if coin["symbol"].lower() == symbol.lower():
                return coin["id"]
        return None
    except:
        return None

# گرفتن قیمت لحظه‌ای با شناسه‌ی CoinGecko
def get_crypto_price_by_id(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    try:
        response = requests.get(url).json()
        return response[coin_id]["usd"]
    except:
        return None

# هندلر دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {"free": 3, "subscribed": False}
    await update.message.reply_text("👋 خوش اومدی! ۳ تحلیل رایگان داری. نماد رمزارز رو بفرست مثل BTC یا ETH یا SHIB")

# هندلر پیام‌های رمزارز
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip().lower()

    if user_id not in user_data:
        user_data[user_id] = {"free": 3, "subscribed": False}

    coin_id = get_coin_id(text)
    if not coin_id:
        await update.message.reply_text(f"❌ نماد '{text.upper()}' پیدا نشد. لطفاً نماد معتبر رمزارز وارد کن.")
        return

    if user_data[user_id]["free"] > 0:
        user_data[user_id]["free"] -= 1
        price = get_crypto_price_by_id(coin_id)
        if price:
            message = f"✅ قیمت لحظه‌ای {text.upper()}: ${price}\nباقی‌مونده رایگان: {user_data[user_id]['free']}"
        else:
            message = f"⚠️ خطا در دریافت قیمت {text.upper()}"
    elif user_data[user_id]["subscribed"]:
        message = f"✅ تحلیل {text.upper()} ارسال شد (اشتراک فعال)"
    else:
        message = (
            "🚫 تحلیل رایگان تموم شد.\n"
            "💳 برای ادامه:\n"
            "➤ پرداخت ۱۰۰۰ تومان برای هر تحلیل\n"
            "➤ یا پرداخت ۱۰ هزار تومان برای اشتراک ماهانه\n"
            "📲 برای پرداخت، بزودی لینک زرین‌پال اضافه می‌شه"
        )

    await update.message.reply_text(message)

# اجرای ربات در Thread جدا
def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

# اجرای Flask برای باز نگه داشتن پورت
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "✅ Bot is running!"

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    flask_app.run(host='0.0.0.0', port=10000)
