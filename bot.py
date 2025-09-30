from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
import requests

TOKEN = os.getenv("BOT_TOKEN")
user_data = {}

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
        return response[symbol_map[symbol]]["usd"]
    except:
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {"free": 3, "subscribed": False}
    await update.message.reply_text("👋 خوش اومدی! ۳ تحلیل رایگان داری. اسم رمزارز رو بفرست مثل BTC یا ETH")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.upper()

    if user_id not in user_data:
        user_data[user_id] = {"free": 3, "subscribed": False}

    if user_data[user_id]["free"] > 0:
        user_data[user_id]["free"] -= 1
        price = get_crypto_price(text)
        if price:
            message = f"✅ قیمت لحظه‌ای {text}: ${price}\nباقی‌مونده رایگان: {user_data[user_id]['free']}"
        else:
            message = f"❌ نماد {text} شناخته نشد. لطفاً BTC یا ETH یا DOGE یا BNB وارد کن."
    elif user_data[user_id]["subscribed"]:
        message = f"✅ تحلیل {text} ارسال شد (اشتراک فعال)"
    else:
        message = (
            "🚫 تحلیل رایگان تموم شد.\n"
            "💳 برای ادامه:\n"
            "➤ پرداخت ۱۰۰۰ تومان برای هر تحلیل\n"
            "➤ یا پرداخت ۱۰ هزار تومان برای اشتراک ماهانه\n"
            "📲 برای پرداخت، بزودی لینک زرین‌پال اضافه می‌شه"
        )

    await update.message.reply_text(message)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
