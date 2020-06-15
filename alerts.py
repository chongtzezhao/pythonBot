import uuid

def guildError(args):
    return '```\
Content: {}\n\
Name: {}\n\
Display Name: {}\n\
User ID: {}\n\
Server/Guild ID: {}\n\
Server/Guild name: {}\n\
Channel ID: {}\n\
Channel name: {}\n\
Error: {}```\
        '.format(*args)


def userError(args):
    return '```\
Content: {}\n\
Name: {}\n\
Display Name: {}\n\
User ID: {}\n\
Error: {}```'.format(*args)

async def alertOwner(client, OWNER_ID, toSend):
    owner = client.get_user(OWNER_ID)
    while toSend:
        await owner.send(toSend[:2000])
        toSend = toSend[2000:]


async def addAlert(message, OWNER_ID, errorName, client):
    data = [message.content, message.author.name, message.author.display_name,message.author.id]
    if message.guild:
        data.extend([message.guild.name, message.guild.id, message.channel.name, message.channel.id])
    data.append(errorName)
    
    if OWNER_ID:
        if errorName=='user talk to bot':
            toSend = f'{message.author.id} {message.author.mention}: {message.content}'
        else:
            if len(data)>5:
                toSend = guildError(data)
            else:
                toSend = userError(data)
        await alertOwner(client, OWNER_ID, toSend)

    channel = client.get_channel(711494328056545293)
    SEP = str(uuid.uuid4())
    await channel.send(SEP+' incoming')
    data = SEP.join(map(str, data))
    while data:
        await channel.send(data[:2000])
        data = data[2000:]
    await channel.send('done')
    