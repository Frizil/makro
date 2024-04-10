import os
import logging
from dotenv import load_dotenv
import subprocess
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor

# Load environment variables from .env file
load_dotenv()

# Get bot token and allowed user from environment variables
TOKEN = os.getenv("TOKEN")

# Define the available scripts
scripts = {
    '1': 'homes.py',
    '2': 'homesx.py',
    '3': 'slotikan.py',
    '4': 'slotdaun.py'
}

# Global variable to hold the running script process
running_script_process = None

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# Define states
class ScriptSelection(StatesGroup):
    waiting_for_script = State()

# Start command handler
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply(f'Hai, {message.from_user.first_name} ini script yang tersedia\n'
                        '1. Homes (homes.py)\n'
                        '2. Homesx (homesx.py)\n'
                        '3. Slotikan (slotikan.py)\n'
                        '4. Slotdaun (slotdaun.py)\n'
                        'Silahkan pilih (1-4):')

# Command handler for selecting and running a script
@dp.message_handler(Text(equals=['1', '2', '3', '4'], ignore_case=True), state=ScriptSelection.waiting_for_script)
async def select_script(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['selected_script'] = message.text.strip()

    if data['selected_script'] in scripts:
        global running_script_process
        if running_script_process is not None:
            running_script_process.kill()
            await message.reply('Script berhasil dihentikan')

        script_name = scripts[data['selected_script']]
        running_script_process = subprocess.Popen(['python', script_name])
        await message.reply(f'Script {script_name} berhasil dijalankan')
    else:
        await message.reply('Maaf, pilihan tidak tersedia. Silahkan pilih kembali (1-4):')

# Stop command handler
@dp.message_handler(commands=['stop'])
async def stop(message: types.Message):
    global running_script_process
    if running_script_process is not None:
        running_script_process.kill()
        await message.reply('Script berhasil dihentikan')
        running_script_process = None
    else:
        await message.reply('Tidak ada script yang dijalankan')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)