import os
import asyncio
import sys
import re
import random
import time
from telethon import TelegramClient, events
from dotenv import load_dotenv


load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_file = os.getenv("SESSION_FILE")

bot = ['danaudalamhutan', 'KampungMaifamXBot', 'KampungMaifamX4Bot', 'KampungMaifamBot']
result = "/casino_hasil"
mode = "/casino_FiftyFifty_"
judi = mode + str(random.randint(1, 2)) + "_1e12"
hapus = '/eat_holysnack'
total = 0

narasi = {
    "Bahasa diubah ke Bahasa Indonesia",
    "Berhasil bertaruh",
    "Energi berhasil dipulihkan",
    "Sekarang kamu bebas",
    "Hasil akan keluar",
}

ncasino = {
    "Belum ada taruhan",
    "Kamu bertaruh untuk angka",
    "Tulis angka",
}

nlanjut = {
    "Rumah yang kamu kunjungi",
    "Keamanan rumah yang mau",
    "tidak punya barang untuk dicuri",
    "Alamat yang sama",
    "Oh tidak!!",
}

async def bentar(w):
    await asyncio.sleep(w)

async def mancingddh(client, w):
    while True:
        await client.send_message(bot[0], "/fish")
        await bentar(w)

async def lanjut(tmp, event, buron):
    await asyncio.sleep(1.8)
    if tmp == 5:
        await event.respond(buron)
    else:
        await event.respond(maling[tmp])
    return tmp

with TelegramClient(session_file, api_id, api_hash) as client:
    client.loop.run_until_complete(client.send_message(bot[1], '/homesx'))

    @client.on(events.NewMessage(incoming=True, from_users=bot[1]))
    async def handler(event):
        global maling
        global tmp
        global total

        teks = event.text

        if any(nar in teks for nar in narasi):
            await asyncio.sleep(2)
            await event.respond('/homesx')
            return

        if any(nca in teks for nca in ncasino):
            await asyncio.sleep(2)
            await event.respond(judi)
            return

        if "Rumah Kosong Warga" in teks:
            tmp = 0
            maling = [x for x in teks.split() if '/curibarang' in x]
            await asyncio.sleep(1.8)
            await event.respond(maling[tmp])
            return

        if any(nlan in teks for nlan in nlanjut):
            tmp += 1
            await lanjut(tmp, event, hapus)
            return

        if "Kamu berhasil mencuri" in teks:
            tmp += 1
            total += 40
            print('Skill = ', total)
            await lanjut(tmp, event, hapus)

        if 'Bagus!!' in teks or 'Uuuh rasanya enak' in teks:
            await asyncio.sleep(1.8)
            await event.respond(result)
            return

        if 'Selesaikan permainan' in teks or 'Tidak ada harga buronan' in teks:
            await asyncio.sleep(1.8)
            await event.respond(result)
            return

        if 'Kamu terkurung' in teks:
            await asyncio.sleep(1.8)
            await event.respond('/release')
            return

        if 'Apa kamu yakin' in teks:
            await asyncio.sleep(1.8)
            await event.click(text="Confirm")
            return

        if 'Kamu tidak memiliki cukup energi' in teks:
            await asyncio.sleep(1.8)
            await event.respond("/restore_max_confirm")
            return

    client.start()
    print(time.asctime(), '-', 'Start')
    client.loop.create_task(mancingddh(client, 245))
    client.run_until_disconnected()
    print(time.asctime(), '-', 'Stop')