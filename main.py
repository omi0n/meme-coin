from flask import Flask
from keep_alive import keep_alive

import logging
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# In-memory tokens (esempio)
valid_tokens = []

# Funzione per il timer (esempio)
def tempo_rimanente(token):
    return "15m"

# Funzione di benvenuto nuovi membri
async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_members = update.message.new_chat_members
    for member in new_members:
        await update.message.reply_text(f"Benvenuto {member.full_name}! 😊")

# Funzione start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📈 Ultimi Score", callback_data='ultimi')],
        [InlineKeyboardButton("🔝 Top Token Oggi", callback_data='top')],
        [InlineKeyboardButton("⏳ Timer in corso", callback_data='timer')],
        [InlineKeyboardButton("✅ Aiuto", callback_data='aiuto')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Scegli un'opzione:", reply_markup=reply_markup)

# Funzione gestione pulsanti
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "ultimi":
        if valid_tokens:
            text = "\n\n".join([f"🆕 {t['name']} - {t['score']} punti" for t in valid_tokens[-5:]])
        else:
            text = "⚠️ Nessun token valido trovato."
    elif query.data == "top":
        if valid_tokens:
            top = sorted(valid_tokens, key=lambda x: x['score'], reverse=True)
            text = f"🔝 Top token: {top[0]['name']} - {top[0]['score']} punti"
        else:
            text = "⚠️ Nessun token valido trovato."
    elif query.data == "timer":
        if not valid_tokens:
            text = "⏳ Nessun token in attesa."
        else:
            text = "⏳ Timer attivi:\n" + "\n".join([f"🪙 {t['name']} - {tempo_rimanente(t)}" for t in valid_tokens[-5:]])
    elif query.data == "aiuto":
        text = "Comandi:\n/start\n📈 Ultimi\n🔝 Top\n⏳ Timer\n"
    else:
        text = "Comando non valido."
    await query.edit_message_text(text=text)

# Main
async def main():
    application = Application.builder().token("8113756420:AAGQaBaY8GrnxUZ7YKLkQZtjHYlpEI3jkB0").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))
    keep_alive()
    await application.run_polling()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
