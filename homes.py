import os
import re
import asyncio
import sys
import random
import time
from telethon import TelegramClient, events
from dotenv import load_dotenv


load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_file = os.getenv("SESSION_FILE")

dest = ('danaudalamhutan', 'KampungMaifamBot', 'KampungMaifamXBot')

async def nungguin(w):
   await asyncio.sleep(w)

async def mancingddh(client, w):
    while True:
        await client.send_message(dest[0], "/fish")
        await nungguin(w)

with TelegramClient(session_file, api_id, api_hash) as client:
    client.loop.run_until_complete(client.send_message(dest[2], '/homes_curiUang'))

    @client.on(events.NewMessage(from_users=dest[2]))
    async def handler(event):
        pesan = event.raw_text

        if "Villager's Houses" in pesan or "Rumah Warga" in pesan:
            print(time.asctime() + " Kunjungi Rumah Warga ke - ")
            time.sleep(2)
            x = pesan.split('/curi')
            file = open("Homes.txt", "a+")
            count = 0
            for i in range(1, 11):
                y = x[i].split(' - ')
                z = y[0].replace('Uang', '/curiTernak')
                await event.respond(z)
                print(time.asctime() + " Masuk Rumah")
                file.write(z+'\n')
                print(time.asctime() + " Maling Alamat ke-" + str(i))
                count += 1

                if count % 10 == 0:
                    time.sleep(2)
                    await event.respond('Hapus menggunakan Uang')
                    print(time.asctime(), 'hapus buron')
                time.sleep(3)
            await event.respond('/homes_curiUang')
            file.close()
            return

        if 'Kamu tidak memiliki cukup energi' in pesan:
            print(time.asctime(), 'Habis energi')
            time.sleep(2)
            await event.respond('/restore_max_confirm')
            time.sleep(2)
            return

        if 'Energi berhasil dipulihkan' in pesan:
            print('energi di pulihkan')
            await nungguin(1)

        if 'Polisi menemukanmu' in pesan:
            print('kena polisi')
            await client.send_message(dest[2], '/release_denganKartu')
            print('nyogok polisi')
            await nungguin(1)

        if 'Apa kamu yakin untuk menggunakan' in pesan:
            print(time.asctime(), 'Sogok polisi dlu')
            time.sleep(2)
            await event.click(text="Confirm")
            return

    client.start()
    client.loop.create_task(mancingddh(client, 245))
    client.run_until_disconnected()