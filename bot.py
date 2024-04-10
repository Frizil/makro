import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from dotenv import load_dotenv
import subprocess

# Load environment variables from .env file
load_dotenv()

# Get bot token and allowed user from environment variables
TOKEN = os.getenv("TOKEN")
ALLOWED_USER = os.getenv("ALLOWED_USERS")

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the available scripts
scripts = {
    '1': 'homes.py',
    '2': 'homesx.py',
    '3': 'slotikan.py',
    '4': 'slotdaun.py'
}

# Global variable to hold the running script process
running_script_process = None

# Start command handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hai, {update.effective_user.first_name} ini script yang tersedia\n'
                              '1. Homes (homes.py)\n'
                              '2. Homesx (homesx.py)\n'
                              '3. Slotikan (slotikan.py)\n'
                              '4. Slotdaun (slotdaun.py)\n'
                              'Silahkan pilih (1-4):')

# Command handler for selecting and running a script
def select_script(update: Update, context: CallbackContext) -> None:
    selected_script = update.message.text.strip()

    if selected_script in scripts:
        global running_script_process
        if running_script_process is not None:
            running_script_process.kill()
            update.message.reply_text('Script berhasil dihentikan')

        script_name = scripts[selected_script]
        running_script_process = subprocess.Popen(['python', script_name])
        update.message.reply_text(f'Script {script_name} berhasil dijalankan')
    else:
        update.message.reply_text('Maaf, pilihan tidak tersedia. Silahkan pilih kembali (1-4):')

# Stop command handler
def stop(update: Update, context: CallbackContext) -> None:
    global running_script_process
    if running_script_process is not None:
        running_script_process.kill()
        update.message.reply_text('Script berhasil dihentikan')
        running_script_process = None
    else:
        update.message.reply_text('Tidak ada script yang dijalankan')

# Unknown command handler
def unknown(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Maaf, perintah tidak dikenali.')

def main() -> None:
    # Create the Updater and pass it your bot's token
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.regex(r'^[1-4]$'), select_script))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, unknown))

    # Start the Bot
    updater.start_polling()
    logger.info("Bot is running...")

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()