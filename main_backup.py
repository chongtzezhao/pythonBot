import os
import random
import discord
from subprocess import CalledProcessError, check_output, STDOUT, TimeoutExpired, Popen, PIPE
from sys import exit
import threading
from cleaner import start_cleaning
from process import fakeFileError, fakeImportError, findBackticks, prepend
from env_process import load_env, output_env, write_env
from alerts import addAlert, sendResponse
from detect_spam import *
from keep_alive import keep_alive

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
os.environ['DISCORD_BOT_TOKEN'] = "[REDACTED]"
client = discord.Client()
OWNER_ID = 259680008635809792
HIDDENFILES = ["main.py", "process.py", "keep_alive.py", "envGLOB.py", "README.md", "runtime.txt", "requirements.txt", "pyproject.toml", "poetry.lock", ".upm", "pycache"]
HIDDENDIRS = ["/usr/lib/python", "/home/"]
RETORTS = ["haha you tried to find restricted directory :))) go and fly kite", "pls stop coding and go outside, you need exercise :))", "oi what you think you doing ah", "you think you v pro isit", "you could be doing more productive things than trying to hack a sad python bot :("]
GLOBAL_VARS = ["OWNER_ID", "HIDDENFILES", "HIDDENDIRS", "RETORTS"]

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name='for "import this"'))

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to the server!\nRun code by starting your message with "py" and enclosing your code in backticks "`"'
    )

async def process_code(message):
    global GLOBAL_VARS
    exec('\nglobal '.join(GLOBAL_VARS)) # setting all the variables to global
    contents = message.content[2:].strip()
    code = findBackticks(contents)
    env_stuff = ''
    gen_env = ''
    if contents[0]=='/':
        env_stuff, env_name = load_env(contents) # create env if needed and load variables
        gen_env = output_env(code) # code to output the variables after they are modified
    timeout = 5
    importer = prepend()

    print(importer+env_stuff+code+gen_env, file=open("envGLOB.py", 'w+'))  # write to file

    lines = open("envGLOB.py", 'r').readlines()  # before executing file, check for forbidden keywords
    for i in range(len(lines)):
        for FILE in HIDDENFILES:
            if lines[i].find(FILE) > -1:
                await fakeFileError(message, lines[i].strip(), i+1, FILE)
                await addAlert(message, OWNER_ID, FILE, client)
                return
        for FILE in HIDDENDIRS:
            if lines[i].find(FILE) > -1:
                await message.channel.send(random.choice(RETORTS)+f'\n<@{message.author.id}>')
                await addAlert(message, OWNER_ID, FILE, client)
                return
    try:
        out = check_output(['python', 'envGLOB.py', '', 'test.txt'],
                            stderr=STDOUT, timeout=timeout).decode()

    except TimeoutExpired:  # Infinite loop 
        out = f'```TimeoutExpired: Your code timed out after {timeout} seconds```'
    except CalledProcessError:  # Indentation error, undefined error etc
        proc = Popen("python envGLOB.py", stderr=STDOUT, stdout=PIPE, shell=True)
        encoded = proc.communicate()[0]
        out = '```'+encoded.decode()+'```'
    except Exception as e:
        out = str(e)
        print("Unpredicted error:")
        await addAlert(message, OWNER_ID, out, client)


    if out.find('73a3290c-340b-44b1-9899-8542f0894495')>-1: # update envrionment
        index = out.find('73a3290c-340b-44b1-9899-8542f0894495')
        data = out[index+37:]
        write_env(env_name, data)
        out = out[:index]

    if out.find("50d96c61-f56d-4704-b781-b36cc2953b16")>-1: # imported something restricted
        arr = out.split(' ')
        num = arr.index("50d96c61-f56d-4704-b781-b36cc2953b16")
        module = arr[num+1]
        await fakeImportError(message, module)
        await addAlert(message, OWNER_ID, module, client)
    elif len(out)>0:
        #await message.channel.send(f'oi bot down lah \n<@{message.author.id}>')
        if len(out)>2000-25:
            to_send = out[:1800]+f'\nOi why your output so long ah? You will get the rest of the output in your pms :)))\n<@{message.author.id}>'
            user = client.get_user(message.author.id)
            await message.channel.send(to_send)
            while out:
                await user.send(out[:min(2000, len(out))])
                out = out[min(2000, len(out)):]
        else:
            out+=f'\n<@{message.author.id}>'
            await message.channel.send(out)

@client.event
async def on_message(message):
    global GLOBAL_VARS
    exec('\nglobal '.join(GLOBAL_VARS)) # setting all the variables to global
    if message.author == client.user:
        return

    if message.author.id==OWNER_ID and message.content[:6]=="pysend":
        contents = message.content[6:].strip()
        stuff = (contents.find(' '), contents.find('\n'),  contents.find('`'))
        index = len(contents)
        for val in stuff: 
            if val>-1: index = min(index, val)
        id = int(contents[:index])
        msg = contents[index+1:]
        channel = client.get_channel(id)
        if channel is None:
            channel = client.get_user(id)
        await channel.send(msg)
        return

    if message.guild is None:
        await addAlert(message, OWNER_ID, "user pmed bot", client)
        if message.content[:2]=='py':
            await message.channel.send("we encourage open source :)) means your code can and should be seen by all")
        await addAlert(message, OWNER_ID, "user pmed bot", client)
        return

    #await message.channel.send(message.content, tts=True)
    if message.content=="test":
        await message.channel.send("hi")

    if message.author.id==708628766833770556 and message.channel.id==711494328056545293 and message.content=="acknowledged":
        await sendResponse(client)

    if message.content[:2].lower() == 'py':
        #t1 = threading.Thread(target=process_code, args=[message])
        #t1.start()
        await process_code(message)
        return
        

start_cleaning()
keep_alive()
print(f'Bot TOKEN: {TOKEN}')
client.run(TOKEN)
TOKEN = "HAHAHA YOU WILL NEVER FIND OUT... unless :think:"


