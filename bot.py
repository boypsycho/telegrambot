from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8180909635:AAFNtlHzS_gxEU4QAl1p5U0FtOirC5mIgec"   # <- paste your token here
OWNER_ID = 877625275                # <- put your Telegram user ID here (numbers only)

def get_ai_response(message: str) -> str:
    # Simple placeholder AI (echo). We'll swap this for real AI later.
    return f"You said: {message}\n(This will be replaced with real AI later)"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("Access denied ❌")
        return
    await update.message.reply_text("Hello! Your private AI bot is ready 🛠")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("Access denied ❌")
        return
    user_message = update.message.text or ""
    ai_reply = get_ai_response(user_message)
    await update.message.reply_text(ai_reply)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()
