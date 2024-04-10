from telethon.sync import TelegramClient, events
import os
from dotenv import load_dotenv
import subprocess

# Load environment variables from .env file
load_dotenv()

# Get bot token and allowed user from environment variables
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Define the available scripts
scripts = {
    '1': 'homes.py',
    '2': 'homesx.py',
    '3': 'slotikan.py',
    '4': 'slotdaun.py'
}

# Global variable to hold the running script process
running_script_process = None

# Initialize the Telegram client
client = TelegramClient('bot_session', API_ID, API_HASH)

# Start command handler
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond(f'Hai, {event.sender.username} ini script yang tersedia\n'
                        '1. Homes (homes.py)\n'
                        '2. Homesx (homesx.py)\n'
                        '3. Slotikan (slotikan.py)\n'
                        '4. Slotdaun (slotdaun.py)\n'
                        'Silahkan pilih (1-4):')

# Command handler for selecting and running a script
@client.on(events.NewMessage(pattern='/[1-4]'))
async def select_script(event):
    selected_script = event.raw_text.strip()[1:]

    if selected_script in scripts:
        global running_script_process
        if running_script_process is not None:
            running_script_process.kill()
            await event.respond('Script berhasil dihentikan')

        script_name = scripts[selected_script]
        running_script_process = subprocess.Popen(['python', script_name])
        await event.respond(f'Script {script_name} berhasil dijalankan')
    else:
        await event.respond('Maaf, pilihan tidak tersedia. Silahkan pilih kembali (1-4):')

# Command handler for stopping the script
@client.on(events.NewMessage(pattern='/stop'))
async def stop(event):
    global running_script_process
    if running_script_process is not None:
        running_script_process.kill()
        await event.respond('Script berhasil dihentikan')
        running_script_process = None
    else:
        await event.respond('Tidak ada script yang dijalankan')

# Run the client
client.start(bot_token=BOT_TOKEN)
client.run_until_disconnected()