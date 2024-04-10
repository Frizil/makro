import os
from dotenv import load_dotenv
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
import logging
import subprocess

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
ALLOWED_USERS = os.getenv('ALLOWED_USERS', '').split(',')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) in ALLOWED_USERS:
        keyboard = [[InlineKeyboardButton(script, callback_data=script)] for script in ["homes.py", "homesx.py", "slotikan.py", "slotdaun.py"]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Pilih script yang ingin dijalankan:", reply_markup=reply_markup)
    else:
        update.message.reply_text("Maaf, Anda tidak diizinkan untuk menggunakan bot ini.")

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    selected_script = query.data
    query.message.reply_text(f"Menjalankan script {selected_script}")
    run_script(selected_script)

def stop(update: Update, context: CallbackContext) -> None:
    query = update.message
    query.reply_text("Menghentikan script yang sedang berjalan...")
    subprocess.run(['pkill', '-f', 'python .*\\.py'])

def run_script(script_name: str) -> None:
    try:
        subprocess.Popen(["python", script_name])
    except FileNotFoundError:
        update.message.reply_text("File script tidak ditemukan")

def main() -> None:
    bot = Bot(token=TOKEN)
    updater = Updater(bot=bot)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(CommandHandler("stop", stop))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()