import os
import random
import discord
#import aiohttp
import subprocess

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GUILD = "698935414345695254"
client = discord.Client()

ENVS_LIST = []

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to Gi\'s Slaves!'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content[0] == '`' and message.content[-1] == '`':
        code = message.content.replace('`', '')
        if message.channel.id == 707423080238284872:
            print(code, file=open("envGLOB.py", 'w+'))
            proc = subprocess.Popen(
                ["python", "-c", "import envGLOB"], stdout=subprocess.PIPE)
            out = proc.communicate()[0].decode('latin-1')
            print(out)
            await message.channel.send(out)

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

client.run(TOKEN)
print(f'Bot token: {TOKEN}')
