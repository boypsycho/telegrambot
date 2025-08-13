import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# === Configuration ===
BOT_TOKEN = "8180909635:AAFNtlHzS_gxEU4QAl1p5U0FtOirC5mIgec"   # paste your Telegram bot token here
OWNER_ID = 877625275                    # replace with your Telegram numeric user ID
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # get from Railway variables

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# === AI Response Function ===
def get_ai_response(message: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can change to "gpt-4" if your key has access
            messages=[
                {"role": "system", "content": "You are a friendly and helpful AI assistant."},
                {"role": "user", "content": message}
            ],
            max_tokens=200
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"⚠️ Error: {e}"

# === Start Command ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("Access denied ❌")
        return
    await update.message.reply_text("Hello! Your private AI bot is ready 🤖")

# === Message Handler ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("Access denied ❌")
        return
    user_message = update.message.text or ""
    ai_reply = get_ai_response(user_message)
    await update.message.reply_text(ai_reply)

# === Bot Runner ===
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()
