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
    if message.channel.name != "aram-scoreboard" and message.channel.name != "bot-commands":
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

    # detect multi command
    if split_msg[0] == "!multi":
        # seperates message, only works if " joined the lobby" or ", " is between names and region
        user_message_multi = user_message.replace(", ", " joined the lobby")
        split_msg_multi = user_message_multi.split(" joined the lobby")
        # removes "!multi" from array, split_msg_multi should only be names or whitespaces now
        split_msg_multi[0] = split_msg_multi[0].replace("!multi", "")
        last = split_msg_multi[len(split_msg_multi)-1].lower()
        # set default region to euw
        region = "euw"
        # check if specific region is present
        if last.replace(" ", "") == "euw" or last == "eune" or last == "na" or last == "kr":
            region = last.replace(" ", "")
            # remove region from string
            split_msg_multi.pop()
        # limits ammount of names you can look up at the same time to 10, to avoid too many API requests
        if len(split_msg_multi)>10:
            await message.channel.send("too many requests.")
            return
        multi_response = ""
        # construct response by checking each non-empty index
        for i in range(0, len(split_msg_multi)-1):
            if split_msg_multi[i] != " ":
                response = aram_mmr.get_mmr(split_msg_multi[i], region)
                multi_response = multi_response + response
        # print message
        await message.channel.send(multi_response)
        # sleeps for the same time as ammount of names searched for, to limit searches to below 60 per minute
        time.sleep(len(split_msg_multi))
        return

# web server
keep_alive()
client.run(TOKEN)
