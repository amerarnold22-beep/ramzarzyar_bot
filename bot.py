from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {"free": 3}
    await update.message.reply_text("👋 خوش اومدی! ۳ تحلیل رایگان داری. اسم رمزارز رو بفرست مثل BTC یا ETH")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.upper()

    if user_id not in user_data:
        user_data[user_id] = {"free": 3}

    if user_data[user_id]["free"] > 0:
        user_data[user_id]["free"] -= 1
        await update.message.reply_text(f"✅ تحلیل {text} ارسال شد. باقی‌مونده رایگان: {user_data[user_id]['free']}")
    else:
        await update.message.reply_text(
            "🚫 اعتبار رایگان تموم شد.\n"
            "💳 برای ادامه پرداخت لازم است.\n"
            "📲 لینک پرداخت زرین‌پال بزودی اضافه می‌شه"
        )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
