import logging
import os
import subprocess
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler

load_dotenv()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

allowed_users = [5199147926]
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = -1002091418219
running_process = None

def start(update, context):
    user_id = update.effective_user.id
    if user_id in allowed_users:
        keyboard = [
            [InlineKeyboardButton("Slot Ikan", callback_data='slotikan')],
            [InlineKeyboardButton("Slot Daun", callback_data='slotdaun')],
            [InlineKeyboardButton("Homes", callback_data='homes')],
            [InlineKeyboardButton("Homes X", callback_data='homesx')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Pilih yang ingin dijalankan:', reply_markup=reply_markup)
    else:
        user_info = f"Nama: {update.effective_user.full_name}\nUser ID: {user_id}\n<a href='https://t.me/{update.effective_user.username}'>Link Profil</a>"
        context.bot.send_message(chat_id=CHANNEL_ID, text=user_info, parse_mode="HTML", disable_web_page_preview=True)
        context.bot.send_message(chat_id=user_id, text="Anda tidak memiliki izin akses bot ini")

def run_external_script(update, context):
    global running_process
    query = update.callback_query
    user_id = query.from_user.id
    if user_id in allowed_users:
        script_name = query.data
        try:
            running_process = subprocess.Popen(["python", f"{script_name}.py"])
            query.edit_message_text(text=f"{script_name} telah dijalankan")
        except Exception as e:
            query.edit_message_text(text=f"Gagal menjalankan {script_name}. Error: {e}")

def stop_external_script(update, context):
    global running_process
    user_id = update.effective_user.id
    if user_id in allowed_users:
        if running_process is not None:
            running_process.terminate()
            update.message.reply_text("Bot telah dihentikan")
            logger.info("Skrip eksternal dihentikan")
        else:
            update.message.reply_text("Bot sedang tidak dijalankan")
            logger.warning("Bot sedang tidak dijalankan")
    else:
        update.message.reply_text("Anda tidak memiliki izin untuk menghentikan bot.")
        

def main():
    updater = Updater(TOKEN.strip())
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(run_external_script))
    dp.add_handler(CommandHandler("stop", stop_external_script))
    
    updater.start_polling()
    logger.info("Bot dimulai.")
    updater.idle()

if __name__ == '__main__':
    main()