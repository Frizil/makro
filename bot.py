import logging
import os
import subprocess
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

allowed_users = [5199147926]
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = -1002091418219
running_process = None

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

async def start(message: types.Message):
    user_id = message.from_user.id
    if user_id in allowed_users:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton("Slot Ikan", callback_data='slotikan'),
                     InlineKeyboardButton("Slot Daun", callback_data='slotdaun'))
        keyboard.row(InlineKeyboardButton("Homes", callback_data='homes'),
                     InlineKeyboardButton("Homes X", callback_data='homesx'))
        await message.reply("Pilih yang ingin dijalankan:", reply_markup=keyboard)
    else:
        user_info = f"Nama: {message.from_user.full_name}\nUser ID: {user_id}\n<a href='https://t.me/{message.from_user.username}'>Link Profil</a>"
        await bot.send_message(chat_id=CHANNEL_ID, text=user_info, parse_mode="HTML", disable_web_page_preview=True)
        await bot.send_message(chat_id=user_id, text="Anda tidak memiliki izin akses bot ini")

async def run_external_script(callback_query: types.CallbackQuery):
    global running_process
    user_id = callback_query.from_user.id
    if user_id in allowed_users:
        script_name = callback_query.data
        try:
            running_process = subprocess.Popen(["python", f"{script_name}.py"])
            await callback_query.message.edit_text(text=f"{script_name} telah dijalankan")
        except Exception as e:
            await callback_query.message.edit_text(text=f"Gagal menjalankan {script_name}. Error: {e}")

async def stop_external_script(message: types.Message):
    global running_process
    user_id = message.from_user.id
    if user_id in allowed_users:
        if running_process is not None:
            running_process.terminate()
            await message.reply("Bot telah dihentikan")
            logger.info("Skrip eksternal dihentikan")
        else:
            await message.reply("Bot sedang tidak dijalankan")
            logger.warning("Bot sedang tidak dijalankan")
    else:
        await message.reply("Anda tidak memiliki izin untuk menghentikan bot.")

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await start(message)

@dp.callback_query_handler()
async def callback_handler(callback_query: types.CallbackQuery):
    await run_external_script(callback_query)

@dp.message_handler(Command("stop"))
async def cmd_stop(message: types.Message):
    await stop_external_script(message)

def main():
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    main()