import os
import subprocess
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
import logging

# Load token from .env file
load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Load allowed users from .env file
ALLOWED_USERS = os.getenv('ALLOWED_USERS').split(',') if os.getenv('ALLOWED_USERS') else []

# Initialize updater and dispatcher
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variable to store running script
running_script = None

# Dictionary to track which scripts are selected
selected_scripts = {}

# Handler for /start command
def start(update, context):
    user_id = str(update.effective_user.id)
    if user_id in ALLOWED_USERS:
        keyboard = [
            [InlineKeyboardButton("homes.py", callback_data="homes.py")],
            [InlineKeyboardButton("homesx.py", callback_data="homesx.py")],
            [InlineKeyboardButton("slotikan.py", callback_data="slotikan.py")],
            [InlineKeyboardButton("slotdaun.py", callback_data="slotdaun.py")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Pilih script yang ingin dijalankan:", reply_markup=reply_markup)
    else:
        update.message.reply_text("Maaf, Anda tidak diizinkan untuk menggunakan bot ini.")

# Handler for inline keyboard button callback
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    selected_script = query.data
    selected_scripts[selected_script] = query.message.message_id
    run_script(query.message, context, selected_script)
    hide_button(query)

# Function to hide button after it's pressed
def hide_button(query):
    script_name = query.data
    message_id = selected_scripts.get(script_name)
    if message_id:
        query.message.delete_reply_markup(reply_markup=InlineKeyboardMarkup([]))

# Handler for /stop command
def stop(update, context):
    global running_script
    if running_script:
        running_script.kill()
        update.message.reply_text(f"Script {running_script.args} dihentikan")
        running_script = None
    else:
        update.message.reply_text("Tidak ada script yang berjalan")

# Handler for running scripts
def run_script(message, context, script_name):
    global running_script
    if running_script:
        message.reply_text("Script sedang berjalan. Gunakan /stop untuk menghentikannya.")
    else:
        try:
            running_script = subprocess.Popen(["python", script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = running_script.communicate()
            if stderr:
                message.reply_text(f"Error saat menjalankan script: {stderr.decode()}")
            else:
                message.reply_text(f"Script {script_name} berhasil dijalankan")
        except FileNotFoundError:
            message.reply_text("File script tidak ditemukan")

# Add handlers to dispatcher
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

stop_handler = CommandHandler('stop', stop)
dispatcher.add_handler(stop_handler)

dispatcher.add_handler(CallbackQueryHandler(button))

updater.start_polling()