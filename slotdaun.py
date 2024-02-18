import os
import re
import asyncio
import time
from telethon import TelegramClient, events
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_file = os.getenv("SESSION_FILE")

cmd = '/th_SlotMachine_SixLeaves'
cmd1 = '/th_SlotMachine_add'
bot = 'KampungMaifamX4Bot'
invest = '/invest_Helikopter_beli_100'
ch = 'inMaifam'

jackpot = 0
poin = 0
cv = 0
sk = 0
af = 0
fp = 0
hw = 0
mm = 0
bd = 0
cc = 0
md = 0
mp = 0
mpm = '2'

with TelegramClient(session_file, api_id, api_hash) as client:
        client.loop.run_until_complete(client.send_message(bot, cmd))
        @client.on(events.NewMessage(from_users=bot))
        async def handler(event):
            global jackpot
            global poin
            global cv
            global sk
            global af
            global fp
            global hw
            global mm
            global bd
            global cc
            global md
            global mp
            
            me = await client.get_me()
            dn = me.first_name
            usn = me.username
            
            if '10000000Qn' in event.raw_text:
                await asyncio.sleep(2)
                await event.respond('/tamanHiburan_TembakTopeng')
                print('Mulai Dart')
                return
            
            if 'kemampuan+1' in event.raw_text:
                sk += 1
            
            if 'PoinSlot' in event.raw_text:
                poin_match = re.search(r'(\d+)\s*PoinSlot', event.raw_text)
                if poin_match:
                   poin += int(poin_match.group(1))
        
            if 'PoinJackpot' in event.raw_text:
                jackpot_match = re.search(r'(\d+)\s*PoinJackpot', event.raw_text)
                if jackpot_match:
                   jackpot += int(jackpot_match.group(1))
       
            if '💎' in event.raw_text:
               gems_match = re.search(r'(\d+)\s*💎', event.raw_text)
               if gems_match:
                  gems += int(gems_match.group(1))
        
            if '🎫Tiket' in event.raw_text:
                tiket_match = re.search(r'(\d+)\s*🎫Tiket', event.raw_text)
                if tiket_match:
                   tiket += int(tiket_match.group(1))
        
            if 'KemampuanMemancing' in event.raw_text:
                skill_match = re.search(r'(\d+)\s*KemampuanMemancing', event.raw_text)
                if skill_match:
                   skill += int(skill_match.group(1))
        

            if '🏵' in event.raw_text:
                cv_match = re.search(r'(\d+)\s*🏵', event.raw_text)
                if cv_match:
                   cv += int(cv_match.group(1))
                   
            if 'Kamu memperoleh: 🧌ActionFigure' in event.raw_text:
                af += 1
                
            if 'Kamu memperoleh: 🏎HotWheels' in event.raw_text:
                hw += 1
                
            if 'Kamu memperoleh: 👾FunkoPop' in event.raw_text:
                fp += 1
                
            if 'Kamu memperoleh: 🤖MechaModel' in event.raw_text:
                mm += 1
                
            if 'Kamu memperoleh: 👱‍♀️BarbieDoll' in event.raw_text:
                bd += 1
                
            if 'Kamu memperoleh: 📕ClassicalComic' in event.raw_text:
                cc += 1
                
            if 'Kamu memperoleh: 🏎Mini4WD' in event.raw_text:
                md += 1
                
            if 'Kamu memperoleh: 🦄MyLittlePony' in event.raw_text:
                mp += 1
                
                
            elif 'Ada tujuh jenis ikan' in event.raw_text:
                await asyncio.sleep(2)
                await event.click(1, 0)
                return
            
            elif 'Ada enam jenis daun' in event.raw_text:
                if 'Gunakan gelar SlotKing' in event.raw_text:
                    await asyncio.sleep(2)
                    await event.respond('/addtitle_SlotKing')
                else: 
                    await asyncio.sleep(2)
                    await event.click(1, 0)
                return
              
            elif 'Berhasil menambahkan gelar' in event.raw_text:
                await asyncio.sleep(2)
                await event.respond(cmd)
                return
                        
            elif 'Kamu memutar SlotMachine 10x' in event.raw_text:
                await asyncio.sleep(2)
                await event.click(1, 0)
                return
            
            elif 'Koin untuk' in event.raw_text:
                if mpm == '1':
                    await asyncio.sleep(2)
                    await event.respond(cmd1)
                    return
                else:
                    await asyncio.sleep(2)
                    await event.respond("/collectibleFragment_SixLeaves")
                    return
            
            elif 'CollectibleFragment SixLeaves untuk memperoleh' in event.raw_text:
                await asyncio.sleep(2)
                await event.click(text="Get CollectibleItem")
                await asyncio.sleep(2)
                await event.respond(cmd1)
                return
            
            elif 'Apa kamu' in event.raw_text:
                await asyncio.sleep(2)
                await event.click(text="Confirm")
                return
            
            elif 'Berhasil membeli tambahan' in event.raw_text:
                await asyncio.sleep(2)
                await event.respond(cmd)
                return
            
            elif 'Setiap harinya' in event.raw_text:
                await asyncio.sleep(2)
                await event.click(text='Mulai')
                return
 
            elif 'Pilih sasaran' in event.raw_text:
                await asyncio.sleep(2)
                await event.click(0, 1)
                return
            
            elif 'Lemparanmu berhasil' in event.raw_text:
                await asyncio.sleep(2)
                await event.click(text='Lanjut')
                return
            
            elif 'Sayang sekali' in event.raw_text:
                await asyncio.sleep(2)
                await event.click(text)
                await event.click(text='Mulai')
                return
 
            elif 'Pilih sasaran' in event.raw_text:
                await asyncio.sleep(2)
                await event.click(0, 1)
                return
            
            elif 'Lemparanmu berhasil' in event.raw_text:
                await asyncio.sleep(2)
                await event.click(text='Lanjut')
                return
            
            elif 'Sayang sekali' in event.raw_text:
                await asyncio.sleep(2)
                await event.click(text='Lanjut')
                return

            elif 'Kesempatan untuk melempar' in event.raw_text or 'dibuka setiap hari' in event.raw_text:
                finalresult = """
🎰 <b>Final Slot Result:</b> {} - @{}

- 🌟 <b>PoinJackpot:</b> <i>+{}</i>
- 🎖 <b>PoinSlot:</b> <i>+{}</i>
- 🏵 <b>CarnivalPoin:</b> <i>+{}</i>
- 🎯 <b>DartSkill:</b> <i>+{}</i>
- 🧌 <b>Action Figure:</b> <i>+{}</i>
- 🤖 <b>Mecha Model:</b> <i>+{}</i>
- 👾 <b>Funko Pop:</b> <i>+{}</i>
- 🏎 <b>Hot Wheels:</b> <i>+{}</i>
- 👱‍♀️ <b>BarbieDoll:</b> <i>+{}</i>
- 📕 <b>ClassicalComic:</b> <i>+{}</i>
- 🏎 <b>Mini4WD:</b> <i>+{}</i>
- 🦄 <b>MyLittlePony:</b> <i>+{}</i>

🎮 <b>Mode:</b> <code>{}</code> 
⏰: <code>{}</code>
"""
                await asyncio.sleep(2)
                await event.respond(invest)
                await asyncio.sleep(2)
                await client.send_message(ch, '' + str(finalresult).format(dn, usn, jackpot, poin, cv, sk, af, mm, fp, hw, bd, cc, md, mp, cmd, time.asctime()) + '', parse_mode='html')
                return
                
            elif 'investasi termahal' in event.raw_text or 'Tiap petani hanya bisa' in event.raw_text or 'Saldo WorldBank tidak mencukupi' in event.raw_text:
                await asyncio.sleep(2)
                print('--Selesai--')
                exit

        client.start()
        print(time.asctime(), '-', 'Slot Started')
        client.run_until_disconnected()