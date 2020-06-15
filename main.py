import os
import random
import discord
import asyncio
import subprocess

# --- user-defined imports ---
from file_manager import start_managing, restore_files
from process import fakeFileError, fakeImportError, findBackticks, prepend, run_async, FAKE_IMPORT
from env_process import load_env, output_env, write_env, GEN_ENV
from alerts import addAlert
from keep_alive import keep_alive
from non_program import send_message, multi_find, react_message

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
os.environ["DISCORD_BOT_TOKEN"]="[REDACTED]"

client = discord.Client()
OWNER_ID = 259680008635809792
HIDDENFILES = []#'pyproject.toml', '.upm', 'poetry.lock', 'envGLOB.py', 'README.md', '__pycache__', 'keep_alive.py', 'spam_data.json', 'detect_spam.py', 'process.py', 'alerts.py', 'main.py', 'cleaner.py', 'envs', 'env_process.py', 'main_backup.py']
HIDDENDIRS = []#"/proc", "/usr/lib/python", "/home/"]
RETORTS = ["haha you tried to find restricted directory :))) go and fly kite", "pls stop coding and go outside, you need exercise :))", "oi what you think you doing ah", "you think you v pro isit", "you could be doing more productive things than trying to hack a sad python bot :("]
GLOBAL_VARS = ["OWNER_ID", "HIDDENFILES", "HIDDENDIRS", "RETORTS", "TOKEN", "PAUSED"]
PAUSED = False

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

@client.event
async def on_message_delete(message):
    quotes = ['"Freedom is not worth having if it does not include the freedom to make mistakes." ~Mahatma Gandhi', '"Anyone who has never made a mistake has never tried anything new." ~Albert Einstein', '"We learn from failure, not from success!" ~Bram Stoker, Dracula', '"Good judgment comes from experience, and experience comes from bad judgment." ~Rita Mae Brown, Alma Mater', '"It takes guts and humility to admit mistakes. Admitting we\'re wrong is courage, not weakness." ~Roy T. Bennett, The Light in the Heart']
    if message.content.startswith('py`'):
        await message.channel.send(random.choice(quotes)+'\n'+message.author.mention)

async def process_code(message):
    global GLOBAL_VARS
    exec('\nglobal '.join(GLOBAL_VARS)) # setting all the variables to global
    contents = message.content[2:].strip()
    try:
        code = findBackticks(contents)
    except:
        await message.channel.send("hmm u got close backticks anot "+message.author.mention)
        return

    '''lines = code.split('\n')  # before executing file, check for forbidden keywords
    for i in range(len(lines)):
        for FILE in HIDDENFILES:
            if lines[i].find(FILE) > -1:
                await fakeFileError(message, lines[i].strip(), i+1, FILE)
                await addAlert(message, OWNER_ID, FILE, client)
                return
        for DIR in HIDDENDIRS:
            if lines[i].find(DIR) > -1:
                await message.channel.send(random.choice(RETORTS)+f'\n{message.author.mention}')
                await addAlert(message, OWNER_ID, DIR, client)
                return'''


    env_stuff = ''
    gen_env = ''
    if contents[0]=='/':
        env_stuff, env_name = load_env(contents) # create env if needed and load variables
        gen_env = output_env(code) # code to output the variables after they are modified
    importer = ''#prepend()

    if code.find('input') > -1:
        await message.channel.send('Did you try to receive console inputs? That function is currently not supported, sorry! '+message.author.mention)

    print(importer+env_stuff+code+gen_env, file=open("envGLOB.py", 'w+'))  # write to file

    out = await run_async()
    print(out)

    if gen_env: # update envrionment
        index = out.find(GEN_ENV)
        data = out[index+37:]
        write_env(env_name, data)
        out = out[:index]

    '''out=out.replace(TOKEN, '[REDACTED]')
    if out.find(FAKE_IMPORT)>-1: # imported something restricted
        arr = out.split(' ')
        num = arr.index(FAKE_IMPORT)
        module = arr[num+1]
        await fakeImportError(message, module)
        await addAlert(message, OWNER_ID, module, client)
        return'''
    if len(out)>2000-22:
        to_send = out[:1899]+f'\nOi why your output so long ah? You will get the entire output in your pms :)))\n{message.author.mention}'
        user = client.get_user(message.author.id)
        await message.channel.send(to_send)
        while out:
            await user.send(out[:min(2000, len(out))])
            out = out[min(2000, len(out)):]
    else:
        out+=message.author.mention
        await message.channel.send(out)

@client.event
async def on_message(message):
    global PAUSED
    if message.author == client.user:
        return
    if message.author.id==OWNER_ID:
        if multi_find(message.content, ['pysend', 'allsend'])==0:
            contents = message.content[7:].strip()
            await send_message(message.author.id, client, contents)
            return
        if multi_find(message.content, ['pyre', 'allre'])==0:
            await react_message(message.author.id, client, message.content[5:].strip(), True)
            return
        if multi_find(message.content, ['pyunre', 'allunre'])==0:
            await react_message(message.author.id, client, message.content[7:].strip(), False)
            return
        if message.content=="pypause":
            PAUSED = True
            print("python bot paused")
            await message.channel.send("python bot paused")
        if message.content=="pystart":
            PAUSED = False
            print("python bot started")
            await message.channel.send("python bot started")
            return
        if message.content.startswith("pyraw"):
            try:
                _local = locals()
                exec(message.content[5:].strip(), globals(), _local)
                out = str(_local['out'])
                print(out)
                while out:
                    await message.channel.send(out[:2000])
                    out = out[2000:]
            except Exception as e:
                await message.channel.send(e)
            return
        if message.content=="pysync":
            owner = client.get_user(OWNER_ID)
            await owner.send("restoring files... ")
            restore_files()
            await owner.send("Success! ")
            return
    if message.author.id==721662788694442026:
        if multi_find(message.content, ['pysend', 'allsend'])==0:
            contents = message.content[7:].strip()
            await send_message(message.author.id, client, contents)
            await addAlert(message, False, "user talk to bot", client)
            return

    if PAUSED: return

    if message.content == 'py help':
        await message.channel.send('I am here to help you with anything! (regarding python of course)\nStart your message with the keyphrase "py" and enclose your code within backticks aka "``" and watch the magic happen!\n\nFind my source code on https://github.com/thepoppycat/pythonBot')
        return

    if message.content=="test":
        await message.channel.send("hi")

    if message.content[:2].lower() == 'py':
        if message.guild:
            await addAlert(message, False, "used", client)
        else:
            await addAlert(message, False, "user pmed bot", client)
        await process_code(message)
    elif message.guild is None and message.author.id!=OWNER_ID:
        await addAlert(message, OWNER_ID, "user talk to bot", client)

start_managing()
keep_alive()
print(f'Bot TOKEN: {TOKEN}')
client.run(TOKEN)
