import os
import random
import discord
#import aiohttp
from subprocess import CalledProcessError, check_output, STDOUT, TimeoutExpired, Popen, PIPE
import textwrap

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GUILD = "698935414345695254"
client = discord.Client()
OWNER = client.get_user(381870129706958858)

ENVS_LIST = []


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name="for code"))

@client.event
async def on_member_join(member):
    return
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to the server!'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content=="test":
        await message.channel.send("hi")
    if message.content[0] == '`' and message.content[-1] == '`':
        timeout = 5
        code = message.content.replace('`', '')

        if code.find("input(")>-1:
            await message.channel.send("Sorry, this bot currently does not support user inputs :(")
            return
        #code = code.replace('while True:', 'for i in range(9999):')
        #code = code.replace("\n", "\n\t")
        #code = "try:\n\t"+code+"\nexcept Exception as e:\n\tprint(f'`{e}`')"
        print(code, file=open("envGLOB.py", 'w+'))  # write to file
        try:
            out = check_output("python envGLOB.py",
                                stderr=STDOUT, timeout=timeout).decode()
        except TimeoutExpired as e:  # Infinite loop 
            out = '```'+str(e)+'```'
        except CalledProcessError as e:  # Indentation error, undefined error etc
            proc = Popen("python envGLOB.py", stderr=STDOUT,  # Merge stdout and stderr
                        stdout=PIPE, shell=True)
            out = '```'+proc.communicate()[0].decode()+'```'
        except Exception as e:
            out = str(e)
            print("Unpredicted error: "+str(out))
            await OWNER.send(
                f'''Unpredicted error: {out}
                Channel: {message.channel.id}
                UserID: {message.author.id}
                '''
            )
        if len(out)>0:
            print(out)
            while out:
                await message.channel.send(out[:min(2000, len(out))])
                out = out[min(2000, len(out)):]

    return
    
    '''try:
        with aiohttp.ClientSession() as session:
            async with session.get(message.attachments[0]['url']) as resp:
                data = await resp.json()
                card = data["card_image"]
                async with session.get(card) as resp2:
                    test = await resp2.read()
                    with open("cardtest2.png", "wb") as f:
                        f.write(test)
    except:
        print("unable to print attachments")'''

print(f'Bot token: {TOKEN}')
client.run(TOKEN)
