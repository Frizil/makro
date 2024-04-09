import asyncio
import logging
import sys
from os import getenv

from aiogram.filters import Filter
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

TOKEN = getenv("TOKEN")
allowed_users = [5199147926]
CHANNEL_ID = -1002091418219  
running_process = None 

dp = Dispatcher()


async def start(message: Message):
    user_id = message.from_user.id
    if user_id in allowed_users:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("Slot Ikan", callback_data='slotikan'),
                     types.InlineKeyboardButton("Slot Daun", callback_data='slotdaun'))
        keyboard.add(types.InlineKeyboardButton("Homes", callback_data='homes'),
                     types.InlineKeyboardButton("Homes X", callback_data='homesx'))
        await message.reply("Pilih yang ingin dijalankan:", reply_markup=keyboard)
    else:
        user_info = f"Nama: {message.from_user.full_name}\nUser ID: {user_id}\n<a href='https://t.me/{message.from_user.username}'>Link Profil</a>"
        await bot.send_message(chat_id=CHANNEL_ID, text=user_info, parse_mode="HTML", disable_web_page_preview=True)
        await bot.send_message(chat_id=user_id, text="Anda tidak memiliki izin akses bot ini")


async def run_external_script(callback_query: CallbackQuery):
    global running_process
    user_id = callback_query.from_user.id
    if user_id in allowed_users:
        script_name = callback_query.data
        try:
            running_process = subprocess.Popen(["python", f"{script_name}.py"])
            await callback_query.message.edit_text(text=f"{script_name} telah dijalankan")
        except Exception as e:
            await callback_query.message.edit_text(text=f"Gagal menjalankan {script_name}. Error: {e}")


async def stop_external_script(message: Message):
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
async def cmd_start(message: Message):
    await start(message)


@dp.callback_query_handler()
async def callback_handler(callback_query: CallbackQuery):
    await run_external_script(callback_query)


@dp.message_handler(commands=["stop"])
async def cmd_stop(message: Message):
    await stop_external_script(message)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    bot.set_my_commands([
        types.BotCommand("start", "Memulai bot"),
        types.BotCommand("stop", "Menghentikan bot")
    ])
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())