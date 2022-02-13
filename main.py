import os
import discord
import time
import aram_mmr
from keep_alive import keep_alive

# set token for discord bot
TOKEN = os.environ["TOKEN"]

EMOTES = {"Iron": "<:Iron:942351359720714280>", "Bronze": "<:Bronze:942351369262731304>",
          "Silver": "<:Silver:942351378955780126>",  "Gold": "<:Gold:942351389168902144>",
          "Platinum": "<:Platinum:942351398723543070>", "Diamond": "<:Diamond:942351409343512616>",
          "Master": "<:Master:942351422656221234>", "Grandmaster": "<:Grandmaster:942351432751919104>",
          "Challenger": "<:Challenger:942350255469494313>"}

client = discord.Client()


@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    time.sleep(1)
    # username = str(message.author).split('#')[0]
    user_message = str(message.content)
    # print(f"{username}: {user_message}")

    # bot doesn't respond to own message. Just for safety.
    if message.author == client.user:
        return
    msg = user_message
    # detect mmr command
    if message.content.startswith("!mmr"):
        # detect multi command
        if "," in msg or "joined the lobby" in user_message:
            msg = user_message.replace(" joined the lobby", ", ")
            msg = msg.replace("\n", "")
            if msg[len(msg) - 2] == ",":
                msg = msg[:-2]
            msg = msg.split(", ")
            msg[0] = msg[0].replace("!mmr ", "")
            last_name = msg[len(msg) - 1].split()
            last = last_name[len(last_name) - 1]
            region = "euw"
            if last == "euw" or last == "eune" or last == "na" or last == "kr":
                region = last
                last_name.pop()
                msg[len(msg) - 1] = " ".join(last_name)
            if len(msg) > 5:
                await message.channel.send("Please only provide at most five summoner names.")
                return
            multi_response = ""
            # construct response by checking each non-empty index
            for i in range(0, len(msg)):
                if msg[i].lower() == "isabelle":
                    response = "Isabelle is the rank 1 ARAM player."
                    rank = "Challenger"
                else:
                    response, rank = aram_mmr.get_mmr(msg[i], region)
                if rank is not None:
                    rank = rank.split()[0]
                    multi_response = multi_response + response + EMOTES[rank] + "\n"
                else:
                    multi_response = multi_response + response + "\n"
            # print message
            await message.channel.send(multi_response)
            # sleeps for the same time as ammount of names searched for, to limit searches to below 60 per minute
            time.sleep(len(msg))
            return
        else:
            if user_message.lower() == "!mmr isabelle":
                await message.channel.send("Isabelle is the rank 1 ARAM player on EUW. Congratulations!",
                                           file=discord.File("images/challenger.webp"))
                return
            msg = user_message.split()
            last = msg[len(msg)-1].lower()
            # set default region to euw
            region = "euw"
            name = ""
            # check if specific region is present
            if last == "euw" or last == "eune" or last == "na" or last == "kr":
                region = last
                # remove region from string
                msg.pop()
            # construct name if it includes spaces
            for i in range(1, len(msg)):
                name = name + " " + msg[i]
            name = name.lstrip()
            response, rank = aram_mmr.get_mmr(name, region)
            # print message and corresponding image
            if rank is None:
                await message.channel.send(response)
            else:
                await message.channel.send(response, file=discord.File("images/" +
                                                                       rank.lower().split(" ")[0] + ".webp"))
            return
    return
# web server
keep_alive()
client.run(TOKEN)
