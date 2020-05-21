import os
import random
import discord

# --- user-defined imports ---
from file_manager import start_managing, restore_files
from process import fakeFileError, fakeImportError, findBackticks, prepend, run_async
from env_process import load_env, output_env, write_env
from alerts import addAlert, sendResponse
from keep_alive import keep_alive

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
os.environ["DISCORD_BOT_TOKEN"]="[REDACTED]"
client = discord.Client()
OWNER_ID = 259680008635809792
HIDDENFILES = []#'pyproject.toml', '.upm', 'poetry.lock', 'envGLOB.py', 'README.md', 'requirements.txt', '__pycache__', 'keep_alive.py', 'spam_data.json', 'detect_spam.py', 'process.py', 'alerts.py', 'main.py', 'cleaner.py', 'envs', 'env_process.py', 'main_backup.py']
HIDDENDIRS = []#"/proc", "/usr/lib/python", "/home/"]
RETORTS = ["haha you tried to find restricted directory :))) go and fly kite", "pls stop coding and go outside, you need exercise :))", "oi what you think you doing ah", "you think you v pro isit", "you could be doing more productive things than trying to hack a sad python bot :("]
ILLEGAL_KEYWORDS=["exec"]
GLOBAL_VARS = ["OWNER_ID", "HIDDENFILES", "HIDDENDIRS", "RETORTS", "TOKEN", "ILLEGAL_KEYWORDS"]

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name='for "py help"'))

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

    lines = code.split('\n')  # before executing file, check for forbidden keywords
    for i in range(len(lines)):
        for FILE in HIDDENFILES:
            if lines[i].find(FILE) > -1:
                await fakeFileError(message, lines[i].strip(), i+1, FILE)
                await addAlert(message, OWNER_ID, FILE, client)
                return
        for DIR in HIDDENDIRS:
            if lines[i].find(DIR) > -1:
                await message.channel.send(random.choice(RETORTS)+f'\n<@{message.author.id}>')
                await addAlert(message, OWNER_ID, DIR, client)
                return
        for WORD in ILLEGAL_KEYWORDS:
            if lines[i].find(WORD) > -1:
                await addAlert(message, OWNER_ID, WORD, client)
                return


    env_stuff = ''
    gen_env = ''
    if contents[0]=='/':
        env_stuff, env_name = load_env(contents) # create env if needed and load variables
        gen_env = output_env(code) # code to output the variables after they are modified
    importer = prepend()

    print(importer+env_stuff+code+gen_env, file=open("envGLOB.py", 'w+'))  # write to file

    out = await run_async()

    if gen_env: # update envrionment
        index = out.find('73a3290c-340b-44b1-9899-8542f0894495')
        data = out[index+37:]
        write_env(env_name, data)
        out = out[:index]

    out=out.replace(TOKEN, '[REDACTED]')
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

    if message.author.id==OWNER_ID:
        if message.content[:6]=="pysend":
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
        if message.content=="py restore":
            owner = client.get_user(OWNER_ID)
            await owner.send("restoring files... ")
            restore_files()
            await owner.send("Success! ")
            return

    if message.content == 'py help':
        await message.channel.send('I am here to help you with anything! (regarding python of course)\nStart your message with the keyphrase "py" and enclose your code within backticks aka "``" and watch the magic happen!\n\nFind my source code on https://github.com/thepoppycat/pythonBot')
        return

    if message.guild is None:
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
        await process_code(message)
        return

start_managing()
keep_alive()
print(f'Bot TOKEN: {TOKEN}')
client.run(TOKEN)
TOKEN = "HAHAHA YOU WILL NEVER FIND OUT... unless :think:"


