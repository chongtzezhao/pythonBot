DATA = ""


def channelError(args):
    return f'\
Content: {args[0]}\n\
Name: {args[1]}\n\
Display Name: {args[2]}\n\
User ID: {args[3]}\n\
Server/Guild ID: {args[4]}\n\
Server/Guild name: {args[5]}\n\
Channel ID: {args[6]}\n\
Channel name: {args[7]}\n\
Error: {args[8]}\
        '


def userError(args):
    return f'\
Content: {args[0]}\n\
Name: {args[1]}\n\
Display Name: {args[2]}\n\
User ID: {args[3]}\n\
Error: {args[4]}\
    '

async def alertOwner(client, OWNER_ID, toSend):
    owner = client.get_user(OWNER_ID)
    while toSend:
        await owner.send(toSend[:2000])
        toSend = toSend[2000:]


async def addAlert(message, OWNER_ID, errorName, client):
    global DATA
    data = [message.content, message.author.name, message.author.display_name,message.author.id]
    if message.guild:
        data.extend([message.guild.name, message.guild.id, message.channel.name, message.channel.id])
    data.append(errorName)
    if len(data)>5:
        toSend = channelError(data)
    else:
        toSend = userError(data)
    channel = client.get_channel(711494328056545293)
    data = '!@#$'.join(map(str, data))
    if len(data)>2000:
        await channel.send('2 packets incoming')
        DATA = data
    else:
        await channel.send(data)
    await alertOwner(client, OWNER_ID, toSend)
    

async def sendResponse(client):
    global DATA 

    channel = client.get_channel(711494328056545293)
    await channel.send(DATA[:2000])
    await channel.send(DATA[2000:])
