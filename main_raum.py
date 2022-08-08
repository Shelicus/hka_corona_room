#---------------------------------------------------------------------------------------------------
# Bibliotheken die Importiert wurden
#---------------------------------------------------------------------------------------------------
import requests
from datetime import datetime
import discord
import asyncio
from discord.ext import commands
from Datenbank_steuerung import *


intents = discord.Intents.default()
client = commands.Bot(
    command_prefix="$",
    help_command=None,
    intents=intents
)

# --------------------------------------------------------------------------------------------------------
#                           Validiert Content| Methode
# --------------------------------------------------------------------------------------------------------
def validateContent(message):
    try:

        if message.count(':') == 1 and type(int(message.split(' ')[2])) == int and message.count(' ') == 5:
            if type(int(message.split(' ')[3].split(':')[0])) == int and type(int(message.split(' ')[3].split(':')[1])) == int:
                match message.split(' ')[4]:
                    case "Monday":
                        return True
                    case "Tuesday":
                        return True
                    case "Wednesday":
                        return True
                    case "Thursday":
                        return True
                    case "Friday":
                        return True
                    case "Saturday":
                        return True
                    case "Sunday":
                        return True
        return False
    except:
        return False

#---------------------------------------------------------------------------------------------------
# Main Programm
#---------------------------------------------------------------------------------------------------
wdhl = 0
@client.event
async def on_connect():
    await client.wait_until_ready()
    print("[Ich habe mich eingeloggt]...")
    client.loop.create_task(change_status())
    client.loop.create_task(verarbeitung())

async def verarbeitung():
    global wdhl
    if wdhl == 0:
        wdhl = 1
        await client.wait_until_ready()
        channel_fail = client.get_channel(#channel-id)
        channel_send = client.get_channel(#channel-id)
        await channel_fail.purge()
        await channel_send.purge()

        doppel = 0
        while True:
            try:

                t = datetime.now()
                time_now = t.strftime('%H:%M')

                if time_now == '23:00':
                    await channel_send.purge()
                    await channel_fail.purge()

                w = datetime.now()
                w_tag = w.strftime('%A')


                for x in range(len(anzeigenbyTag(w_tag))):
                    if time_now == anzeigenbyTag(w_tag)[x][2] and doppel == 0 and anzeigenbyTag(w_tag)[x][5] == 'False':
                        try:
                            room = anzeigenbyTag(w_tag)[x][4]

                            with requests.Session() as s:                                                      #Bnutzer muss hier noch eingefügt werden
                                url = f'https://idp.hs-karlsruhe.de/corona/coronatracker-extro.html?username={Benutzer}&location={room}'
                                seite = s.get(url)

                            await channel_send.send(f'Bestätigt: {room}, {seite}')

                            doppel = 1

                        except Exception as fail:

                            channel_fail = client.get_channel(#channel-id)
                            await channel_fail.send('Fail beim bestätigen:')
                            await channel_fail.send(fail)

                    elif time_now == anzeigenbyTag(w_tag)[x][2] and doppel == 0 and anzeigenbyTag(w_tag)[x][5] == 'True':
                        doppel = 1
                        update_datenbank(anzeigenbyTag(w_tag)[x][0],
                                                 anzeigenbyTag(w_tag)[x][1],
                                                 anzeigenbyTag(w_tag)[x][2],
                                                 anzeigenbyTag(w_tag)[x][3],
                                                 anzeigenbyTag(w_tag)[x][4], 'False')

                    else:
                        doppel = 0

                await asyncio.sleep(40)
            except Exception as fail:
                channel_fail = client.get_channel(#channel-id)
                await channel_fail.send('Fail beim bestätigen:')
                await channel_fail.send(fail)

# --------------------------------------------------------------------------------------------------------
#                           Befehl - Hilfe für Befehlsliste | Command - help
# --------------------------------------------------------------------------------------------------------
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.content == "$help":  # color=0x11ff00 17 255
        embed_help = discord.Embed(title="Du kannst folgende dreckige Dinge mit mir anstellen:", color=0x11ff00)
        embed_help.add_field(name="$addfach [Fachname] [Erkennung-ID] [Std:min] [Day] [Raum]:", value="Fach hinzufügen", inline=True)
        embed_help.add_field(name="Sehr wichtig:", value="ID muss immer unterschiedlich sein!", inline=True)
        embed_help.add_field(name="$del:", value="Liste löschen", inline=True)
        embed_help.add_field(name="$show [Day]:", value="Zeigt Fach anhand von Day an", inline=True)
        embed_help.add_field(name="$update [Fachname] [Erkennung-ID(same id] [Std:min] [Day] [Raum]:", value="update eintrag", inline=True)
        embed_help.add_field(name="$showall: ",value="Zeigt alles an", inline=True)
        embed_help.add_field(name="$blockte [Uhrzeit] [Tag]: ", value="Blockiert Termin", inline=True)
        embed_help.add_field(name="$blockday [Uhrzeit] [Tag]: ", value="Blockiert Termine ganzen Tag", inline=True)
        await message.channel.send(embed=embed_help)
# --------------------------------------------------------------------------------------------------------
#                           Befehl - hinzufügen| Command - $addfach
# --------------------------------------------------------------------------------------------------------
    elif message.content.startswith("$addfach"):
        try:
            if validateContent(message.content) == True:
                hinzufuegen(str(message.content.split(' ')[1]), message.content.split(' ')[2], message.content.split(' ')[3], str(message.content.split(' ')[4]), str(message.content.split(' ')[5]), 'False')
                embed_nach = discord.Embed(title="Erfolgreich hinzugefügt", color=0x00ff00)
                await message.channel.send(embed=embed_nach)
            else:
                embed_nach = discord.Embed(title="Die Eingabe ist leider Falsch - Nicht gespeicher", color=0xff0000)
                await message.channel.send(embed=embed_nach)
        except Exception as f:
            embed_nach = discord.Embed(title="Das hat leider nicht funktioniert - Nicht gespeichert", color=0xff0000)
            await message.channel.send(embed=embed_nach)
            await message.channel.send(f)

# --------------------------------------------------------------------------------------------------------
#                           Befehl - Update Content| Command - $update
# --------------------------------------------------------------------------------------------------------
    elif message.content.startswith("$update"):
        try:
            if validateContent(message.content) == True:
                update_datenbank(str(message.content.split(' ')[1]), message.content.split(' ')[2], message.content.split(' ')[3], str(message.content.split(' ')[4]), str(message.content.split(' ')[5]), 'False')
                embed_nach = discord.Embed(title="Erfolgreich Upgedatet", color=0x00ff00)
                await message.channel.send(embed=embed_nach)
            else:
                embed_nach = discord.Embed(title="Die Eingabe ist leider Falsch - Nicht gespeicher", color=0xff0000)
                await message.channel.send(embed=embed_nach)
        except Exception as f:
            embed_nach = discord.Embed(title="Das hat leider nicht funktioniert - Nicht gespeichert", color=0xff0000)
            await message.channel.send(embed=embed_nach)
            await message.channel.send(f)

# --------------------------------------------------------------------------------------------------------
#                           Befehl - Block Termin| Command - $block
# --------------------------------------------------------------------------------------------------------
    elif message.content.startswith("$blockte"):
        try:
            blockiert = 0
            for x in range(len(anzeigenbyTag(message.content.split(' ')[2]))):
                if message.content.split(' ')[1] == anzeigenbyTag(message.content.split(' ')[2])[x][2]:
                    update_datenbank(anzeigenbyTag(message.content.split(' ')[2])[x][0], anzeigenbyTag(message.content.split(' ')[2])[x][1], anzeigenbyTag(message.content.split(' ')[2])[x][2], anzeigenbyTag(message.content.split(' ')[2])[x][3],anzeigenbyTag(message.content.split(' ')[2])[x][4], 'True')
                    embed_nach = discord.Embed(title="Erfolgreich Blockiert", color=0x00ff00)
                    await message.channel.send(embed=embed_nach)
                    blockiert = 1
            if blockiert == 0:
                embed_nach = discord.Embed(title="Konnte leider nicht Blockiert werden", color=0xff0000)
                await message.channel.send(embed=embed_nach)
        except Exception as f:
            embed_nach = discord.Embed(title="Das hat leider nicht funktioniert - Nicht gespeichert", color=0xff0000)
            await message.channel.send(embed=embed_nach)
            await message.channel.send(f)

# --------------------------------------------------------------------------------------------------------
#                           Befehl - Block Termine Day| Command - $blockday
# --------------------------------------------------------------------------------------------------------
    elif message.content.startswith("$blockday"):
        try:
            blockiert = 0
            for x in range(len(anzeigenbyTag(message.content.split(' ')[1]))):
                    update_datenbank(anzeigenbyTag(message.content.split(' ')[1])[x][0],
                                     anzeigenbyTag(message.content.split(' ')[1])[x][1],
                                     anzeigenbyTag(message.content.split(' ')[1])[x][2],
                                     anzeigenbyTag(message.content.split(' ')[1])[x][3],
                                     anzeigenbyTag(message.content.split(' ')[1])[x][4], 'True')
                    blockiert = 1
            if blockiert == 0:
                embed_nach = discord.Embed(title="Konnte leider nicht Blockiert werden", color=0xff0000)
                await message.channel.send(embed=embed_nach)
            else:
                embed_nach = discord.Embed(title="Erfolgreich Blockiert", color=0x00ff00)
                await message.channel.send(embed=embed_nach)
        except Exception as f:
            embed_nach = discord.Embed(title="Das hat leider nicht funktioniert - Nicht gespeichert", color=0xff0000)
            await message.channel.send(embed=embed_nach)
            await message.channel.send(f)

# --------------------------------------------------------------------------------------------------------
#                          Befehl - Anzeigen| Command - $showall
# --------------------------------------------------------------------------------------------------------
    elif message.content == "$showall":
        try:
            for x in range(len(alles_anzeigen())):
                await message.channel.send(str(alles_anzeigen()[x]))
            if len(alles_anzeigen()) == 0:
                embed_nach = discord.Embed(title="Es wurden keine Termine eingegeben!", color=0x00ff00)
                await message.channel.send(embed=embed_nach)
        except Exception as f:
            embed_nach = discord.Embed(title="Das hat leider nicht funktioniert", color=0xff0000)
            await message.channel.send(embed=embed_nach)
            await message.channel.send(f)

# --------------------------------------------------------------------------------------------------------
#                           Befehl - Anzeigen| Command - $showday
 # --------------------------------------------------------------------------------------------------------
    elif message.content.startswith("$showday"):
        try:
            for x in range(len(anzeigenbyTag(message.content.split(' ')[1]))):
                embed_nach = discord.Embed(title=anzeigenbyTag(message.content.split(' ')[1])[x], color=0x00ff00)
                await message.channel.send(embed=embed_nach)
        except Exception as f:
            embed_nach = discord.Embed(title="Das hat leider nicht funktioniert", color=0xff0000)
            await message.channel.send(embed=embed_nach)
            await message.channel.send(f)

# --------------------------------------------------------------------------------------------------------
#                           Befehl - gelöscht| Command - $del
# --------------------------------------------------------------------------------------------------------
    elif message.content == "$del":
        try:
            delete_liste()
            embed_nach = discord.Embed(title="Erfolgreich gelöscht", color=0x00ff00)
            await message.channel.send(embed=embed_nach)
        except Exception as f:
            embed_nach = discord.Embed(title="Das hat leider nicht funktioniert", color=0xff0000)
            await message.channel.send(embed=embed_nach)
            await message.channel.send(f)

#---------------------------------------------------------------------------------------------------
# Veränderung des Status des Bots
#--------------------------------------------------------------------------------------------------
async def change_status():
    while True:
        try:
            await client.change_presence(activity=discord.Activity(
                type=discord.ActivityType.playing,
                name="Verarbeitung der Daten!",
                status=discord.Status.online))
            await asyncio.sleep(7.5)
            await client.change_presence(activity=discord.Activity(
                type=discord.ActivityType.listening,
                name="Uhrzeit ablesen!",
                status=discord.Status.do_not_disturb))
            await asyncio.sleep(7.5)
        except:
            pass

#---------------------------------------------------------------------------------------------------
# Bot-Token
#---------------------------------------------------------------------------------------------------
client.run("bot-token")
