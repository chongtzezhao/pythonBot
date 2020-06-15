def multi_find(contents, arr):
    stuff = [contents.find(exp) for exp in arr if contents.find(exp)>-1]
    if stuff:
        return min(stuff)
    return -1

async def send_message(sender_id, client, contents):
    index = multi_find(contents, [' ', '\n', '`'])
    if index==-1: return
    id = int(contents[:index])
    msg = contents[index:].strip()
    tts = True if msg[:4]=='/tts' else False
    if tts: msg = msg[4:].strip()
    channel = client.get_channel(id)
    if not channel:
        channel = client.get_user(id)
    await channel.send(msg, tts=tts)
    sender = client.get_user(sender_id)
    print(f"{sender.name} has sent {msg} to {channel.name}")
    await sender.send(f"message sent to {channel.mention}")

async def react_message(sender_id, client, contents, add=True):
    arr = contents.split(' ')
    channel = client.get_channel(int(arr[0]))
    if arr[1].isdigit() and len(arr[1])==18:
        msg = await channel.fetch_message(int(arr[1]))
        reacts = arr[2:]
    else:
        msg = await channel.fetch_message(channel.last_message_id)
        reacts = arr[1:]
    for react in reacts:
        for reaction in msg.reactions:
            if reaction.emoji==react and reaction.me==True:
                print("already reacted")
        if add:
            await msg.add_reaction(react)
            print("reacted")
        else:
            member = client.get_user(client.user.id)
            await msg.remove_reaction(react, member)
            print("unreacted")

# Stats functions
async def stats():
    pass