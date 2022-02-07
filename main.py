import os
import discord
import time
import aram_mmr
from keep_alive import keep_alive

# set token for discord bot
TOKEN = os.environ["TOKEN"]

client = discord.Client()


@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    time.sleep(1)
    if message.channel.name != "aram-scoreboard":
        return
    # username = str(message.author).split('#')[0]
    user_message = str(message.content)
    # print(f"{username}: {user_message}")

    # bot doesn't respond to own message. Just for safety.
    if message.author == client.user:
        return
    split_msg = user_message.split()
    # detect mmr command
    if split_msg[0] == "!mmr":
        last = split_msg[len(split_msg)-1].lower()
        # set default region to euw
        region = "euw"
        name = ""
        # check if specific region is present
        if last == "euw" or last == "eune" or last == "na" or last == "kr":
            region = last
            # remove region from string
            split_msg.pop()
        # construct name if it includes spaces
        for i in range(1, len(split_msg)):
            name = name + " " + split_msg[i]
        name = name.lstrip()
        response, rank = aram_mmr.get_mmr(name, region)
        # print message and corresponding image
        if rank is None:
            await message.channel.send(response)
        else:
            await message.channel.send(response, file=discord.File("images/" + rank.lower().split(" ")[0] + ".webp"))
        return

# web server
keep_alive()
client.run(TOKEN)
