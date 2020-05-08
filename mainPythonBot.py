import os
import random
import discord
from subprocess import CalledProcessError, check_output, STDOUT, TimeoutExpired, Popen, PIPE
from sys import exit
import threading
from messages import *


TOKEN = os.getenv('DISCORD_BOT_TOKEN')
client = discord.Client()
OWNER_ID = 259680008635809792
HIDDENFILES = ["mainPythonBot.py", "messages.py"]

ENVS_LIST = []


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name='for "import this"'))

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to the server!\nRun code by enclosing them in backticks "`"'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content=="test":
        await message.channel.send("hi")
    if message.content[:2] == 'py':
        code = message.content[2:].strip()
        if code[0] != '`' or code[-1] != '`':
            return
        timeout = 5
        code = code.replace('`', '')

        if code.find("input(")>-1:
            await message.channel.send("Sorry, this bot currently does not support user inputs :(")
            return

        #code = code.replace("\n", "\n\t")
        #code = "try:\n\t"+code+"\nexcept Exception as e:\n\tprint(f'`{e}`')"

        print(code, file=open("envGLOB.py", 'w+'))  # write to file

        lines = open("envGLOB.py", 'r').readlines()  # before executing file, check for forbidden keywords
        for i in range(len(lines)):
            for FILE in HIDDENFILES:
                if lines[i].find(FILE) > -1:
                    await fakeError(message, lines[i].strip(), i+1, FILE)
                    await alertOwner(message, OWNER_ID, FILE, client)
                    return
        try:
            out = check_output(['python', 'envGLOB.py', '', 'test.txt'],
                                stderr=STDOUT, timeout=timeout).decode()
        except TimeoutExpired as e:  # Infinite loop 
            out = f'```TimeoutExpired: Your code timed out after {timeout} seconds```'
        except CalledProcessError as e:  # Indentation error, undefined error etc
            proc = Popen("python envGLOB.py", stderr=STDOUT,  # Merge stdout and stderr
                        stdout=PIPE, shell=True)
            encoded = proc.communicate()[0]
            out = '```'+encoded.decode()+'```'
        except Exception as e:
            out = str(e)
            print("Unpredicted error:")
            await alertOwner(message, OWNER_ID, out, client)

        if len(out)>0:
            print(out)
            while out:
                await message.channel.send(out[:min(2000, len(out))])
                out = out[min(2000, len(out)):]



print(f'Bot token: {TOKEN}')
client.run(TOKEN)


