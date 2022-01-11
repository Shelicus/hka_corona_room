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



@client.event
async def on_ready():
    print("[Ich habe mich eingeloggt]...")
    channel_fail = client.get_channel(fail-channel)
    channel_send = client.get_channel(send-channel)
    await channel_fail.purge()
    await channel_send.purge()

    doppel = 0
    z_tag = 0

    while True:
        try:
            raum = [['raum', 'raum', 'None'], ['raum', 'raum', 'raum','None'], ['raum', 'raum', 'raum', 'raum', 'None']]

            zeit = [['09:30', '11:30'], ['08:00', '09:30', '11:30'], ['09:50', '11:30', '14:00', '15:30']]

            tage = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

            t = datetime.now()
            time_now = t.strftime('%H:%M')

            if time_now == '23:00':
                await channel_send.purge()
                await channel_fail.purge()

            w = datetime.now()
            w_tag = w.strftime('%A')

            for x in range(len(tage)):
                if w_tag == tage[x]:
                    z_tag = x

            if z_tag <= 4:
                for x in range(len(zeit[z_tag])):
                    if time_now == zeit[z_tag][x] and doppel == 0:
                        try:
                            room = raum[z_tag][x]

                            with requests.Session() as s:
                                url = f'https://idp.hs-karlsruhe.de/corona/coronatracker-extro.html?username=scda1096&location={room}'
                                seite = s.get(url)
                            await asyncio.sleep(60)

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


client.run("bot-Token")
