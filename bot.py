import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
import subprocess

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
ALLOWED_USERS = os.getenv('ALLOWED_USERS', '').split(',')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

async def start(message: types.Message):
    if str(message.from_user.id) in ALLOWED_USERS:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("homes.py", callback_data="homes.py"))
        keyboard.add(types.InlineKeyboardButton("homesx.py", callback_data="homesx.py"))
        keyboard.add(types.InlineKeyboardButton("slotikan.py", callback_data="slotikan.py"))
        keyboard.add(types.InlineKeyboardButton("slotdaun.py", callback_data="slotdaun.py"))
        await message.reply("Pilih script yang ingin dijalankan:", reply_markup=keyboard)
    else:
        await message.reply("Maaf, Anda tidak diizinkan untuk menggunakan bot ini.")

async def button_handler(callback_query: types.CallbackQuery):
    selected_script = callback_query.data
    await bot.send_message(callback_query.from_user.id, f"Menjalankan script {selected_script}")
    subprocess.Popen(["python", selected_script])

async def stop(message: types.Message):
    await message.reply("Menghentikan script yang sedang berjalan...")
    subprocess.run(['pkill', '-f', 'python .*\\.py'])

dp.register_message_handler(start, CommandStart())
dp.register_callback_query_handler(button_handler)
dp.register_message_handler(stop, commands=['stop'])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)