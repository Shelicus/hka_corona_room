#---------------------------------------------------------------------------------------------------
# Bibliotheken die Importiert wurden
#---------------------------------------------------------------------------------------------------
import requests
from datetime import datetime
import discord
import asyncio
from discord.ext import commands


intents = discord.Intents.default()
client = commands.Bot(
    command_prefix="$",
    help_command=None,
    intents=intents
)

#---------------------------------------------------------------------------------------------------
# Main Programm
#---------------------------------------------------------------------------------------------------
wdhl = 0
@client.event
async def on_connect():
    print("[Ich habe mich eingeloggt]...")
    
    global wdhl
    if(wdhl = 0):
        wdhl = 1
        await client.wait_until_ready()
        channel_fail = client.get_channel(fail-channel)
        channel_send = client.get_channel(send-channel)
        await channel_fail.purge()
        await channel_send.purge()

        doppel = 0
        z_tag = 0

        while True:
            try:
                raum = [['raum', 'raum'], ['raum', 'raum', 'raum'], ['raum', 'raum', 'raum', 'raum'],[],[],[],[]]

                zeit = [['09:30', '11:30'], ['08:00', '09:30', '11:30'], ['09:50', '11:30', '14:00', '15:30'],[],[],[],[]]

                tage = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

                t = datetime.now()
                time_now = t.strftime('%H:%M')

                if time_now == '23:00':
                    await channel_send.purge()
                    await channel_fail.purge()

                w = datetime.now()
                w_tag = w.strftime('%A')

                for x in range(7):
                    if w_tag == tage[x]:
                        z_tag = x


                for x in range(len(zeit[z_tag])):
                    if time_now == zeit[z_tag][x] and doppel == 0:
                        try:
                            room = raum[z_tag][x]

                            with requests.Session() as s:                                                      #Bnutzer muss hier noch eingefügt werden
                                url = f'https://idp.hs-karlsruhe.de/corona/coronatracker-extro.html?username={benutzer_kürzel}&location={room}'
                                seite = s.get(url)

                            await channel_send.send(f'Bestätigt: {room}, {seite}')

                            doppel = 1

                        except Exception as fail:

                            channel_fail = client.get_channel(fail-channel)
                            await channel_fail.send('Fail beim bestätigen:')
                            await channel_fail.send(fail)

                    else:
                        doppel = 0

                await asyncio.sleep(30)
            except Exception as fail:
                channel_fail = client.get_channel(fail-channel)
                await channel_fail.send('Fail beim bestätigen:')
                await channel_fail.send(fail)

#---------------------------------------------------------------------------------------------------
# Bot-Token
#---------------------------------------------------------------------------------------------------
client.run("bot-Token")
