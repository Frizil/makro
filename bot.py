from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler, Updater

from dotenv import load_dotenv
import os
import subprocess

load_dotenv()

TOKEN = os.getenv("TOKEN")
allowed_users = [5199147926]
CHANNEL_ID = -1002091418219
running_process = None


def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id in allowed_users:
        keyboard = [
            [
                InlineKeyboardButton("Slot Ikan", callback_data='slotikan'),
                InlineKeyboardButton("Slot Daun", callback_data='slotdaun')
            ],
            [
                InlineKeyboardButton("Homes", callback_data='homes'),
                InlineKeyboardButton("Homes X", callback_data='homesx')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Pilih yang ingin dijalankan:", reply_markup=reply_markup)
    else:
        user_info = f"Nama: {update.effective_user.full_name}\nUser ID: {user_id}\nLink Profil: https://t.me/{update.effective_user.username}"
        context.bot.send_message(chat_id=CHANNEL_ID, text=user_info, disable_web_page_preview=True)
        update.message.reply_text("Anda tidak memiliki izin akses bot ini")


def run_external_script(update: Update, context: CallbackContext):
    global running_process
    user_id = update.effective_user.id
    if user_id in allowed_users:
        script_name = context.callback_query.data
        try:
            running_process = subprocess.Popen(["python3", f"{script_name}.py"])  # Ubah 'python' menjadi 'python3'
            update.callback_query.message.edit_text(text=f"{script_name} telah dijalankan")
        except Exception as e:
            update.callback_query.message.edit_text(text=f"Gagal menjalankan {script_name}. Error: {e}")


def stop_external_script(update: Update, context: CallbackContext):
    global running_process
    user_id = update.effective_user.id
    if user_id in allowed_users:
        if running_process is not None:
            running_process.terminate()
            update.message.reply_text("Bot telah dihentikan")
        else:
            update.message.reply_text("Bot sedang tidak dijalankan")
    else:
        update.message.reply_text("Anda tidak memiliki izin untuk menghentikan bot.")


def main() -> None:
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(run_external_script))
    dp.add_handler(CommandHandler("stop", stop_external_script))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()