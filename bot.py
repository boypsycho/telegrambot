import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # from Render Environment Variables
OWNER_ID = 877625275  # replace with your numeric Telegram user ID
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # from Render Environment Variables

# === Start Command ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("Access denied ❌")
        return
    await update.message.reply_text("Hello! Your private Gemini AI bot is ready 🤖")

# === Gemini Chat Function ===
async def chat_with_gemini(message):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{
            "parts": [{"text": message}]
        }]
    }
    response = requests.post(url, json=payload)
    data = response.json()
    try:
        return data['candidates'][0]['content']['parts'][0]['text']
    except:
        return "Sorry, I couldn’t process that."

# === Message Handler ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("Access denied ❌")
        return
    user_message = update.message.text
    reply = await chat_with_gemini(user_message)
    await update.message.reply_text(reply)

# === Bot Runner ===
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()
