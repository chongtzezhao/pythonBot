

async def fakeError(message, line, line_num, fileName):
    await message.channel.send(f"""
```Traceback(most recent call last):
  File "envGLOB.py", line {line_num}, in < module >
    {line}
FileNotFoundError: [Errno 2] No such file or directory: '{fileName}'```""")


def channelError(args):
    return f'\
Server/Guild ID: {args[0]}\n\
Server/Guild name: {args[1]}\n\
Channel ID: {args[2]}\n\
Channel name: {args[3]}\n\
User ID: {args[4]}\n\
Name: {args[5]}\n\
Display Name: {args[6]}\
        '


def userError(args):
    return f'\
User ID: {args[0]}\n\
Name: {args[1]}\n\
Display Name: {args[2]}\
    '


async def alertOwner(message, OWNER_ID, errorName, client):
    OWNER = client.get_user(OWNER_ID)
    try:
        creds = [message.guild.id,
                    message.guild.name, message.channel.id, message.channel.name, message.author.id, message.author.name, message.author.display_name]
        toSend = channelError(creds)
    except:
        creds = [message.author.id, message.author.name,
                    message.author.display_name]
        toSend = userError(creds)
    toSend += f'\n{errorName}'
    await OWNER.send('```'+toSend+'```')
