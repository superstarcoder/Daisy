import discord
from discord.ext import commands
import globalVars as gv
from math import ceil
import random
import copy

import math


def countBars(x):
    if x <= 0:
        return 0
    rounded = round(x, -1) // 10
    if rounded == 0:
        rounded = 1
    return rounded
    # a = (int(math.ceil(x / 10.0)) * 10)//10
    # if a == 0:
    #    a = 1
    # return a


def embedMsg(description):
    color = 0xf5a742
    embed = discord.Embed(color=color, description=description)
    return embed


def embedShop(page):
    lenOfPage = 5

    #####emojis#####
    #:moneybag:
    #:money_with_wings:
    #:money_mouth:

    shopList = gv.readFile("shop.json")
    if page > ceil(len(list(shopList)) / lenOfPage):
        return
    embed = discord.Embed(color=0x0080ff, title="epic shop", description="`?buy [item]`")

    # 0, 5
    # 5, 10
    for listIndex in range((page - 1) * lenOfPage, ((page - 1) * lenOfPage) + lenOfPage):

        try:
            nameid = list(shopList)[listIndex]
            title = shopList[nameid]["title"]
            cost = shopList[nameid]["cost"]
            description = shopList[nameid]["description"]
            emoji = shopList[nameid]["emoji"]
            # set emoji
            if cost >= 1000000:
                moneyEmoji = ":money_mouth:"
            elif cost >= 50000:
                moneyEmoji = ":money_with_wings:"
            else:
                moneyEmoji = ":moneybag:"

            # embed.add_field(name=emoji+" "+name, value=description+"\n __"+str(cost)+" coins__"+moneyEmoji+"\n\u200B", inline=False)
            embed.add_field(name=emoji + " " + title,
                            value="__" + str(cost) + " coins__" + moneyEmoji + "\n" + description + "\n\u200B",
                            inline=False)
            embed.set_footer(text="type ?shop " + str(page + 1) + " for next page")
        except IndexError:
            pass

    return embed


def getName(userid, bot):
    user = bot.get_user(userid)
    username = user.name
    return username


def embedProfile(userid, bot):
    user = bot.get_user(userid)
    username = user.name + "#" + user.discriminator
    userid = str(userid)
    agents = gv.readFile("agents.json")

    embed = discord.Embed(color=0x0080ff, title=username + "'s profile", description="")
    embed.add_field(name="XP", value=agents[userid]["xp"], inline=False)
    embed.add_field(name="Coins", value=agents[userid]["coins"], inline=False)
    embed.add_field(name="Suggestion Count", value=agents[userid]["suggestionCount"], inline=False)
    embed.add_field(name="Approved Suggestion Count", value=agents[userid]["approvedSuggestionCount"], inline=False)
    embed.add_field(name="Warnings", value=agents[userid]["warnings"], inline=False)

    value = ("None" if not agents[userid]["items"] else agents[userid]["items"])
    embed.add_field(name="Items", value=value, inline=True)

    value = ("None" if not agents[userid]["houses"] else agents[userid]["houses"])
    embed.add_field(name="Houses", value=value, inline=True)

    value = ("None" if not agents[userid]["weapons"] else agents[userid]["weapons"])
    embed.add_field(name="Weapons", value=value, inline=True)

    value = ("None" if not agents[userid]["trophies"] else agents[userid]["trophies"])
    embed.add_field(name="Merch/Trophies", value=value, inline=True)

    return embed


def getWeapon(userid):
    userid = str(userid)
    agents = gv.readFile("agents.json")
    weapons = agents[str(userid)]["weapons"]
    if "diamond sword" in weapons:
        weapon = "diamond sword"
    elif "iron sword" in weapons:
        weapon = "iron sword"
    elif "wooden sword" in weapons:
        weapon = "wooden sword"
    else:
        weapon = "fist"
    return weapon


def playerInfo(userid, bot, info):
    inline = False
    bar = "■"
    user = bot.get_user(userid)
    username = user.name + "#" + user.discriminator
    embed = discord.Embed(color=0x0080ff, title=username + "'s fight info", description="")
    embed.add_field(name="Money on the Line", value=info["betAmt"], inline=False)
    embed.add_field(name="Weapon", value=info["weapon"], inline=inline)
    d = {"health": "Health", "defense": "Defense", "energy": "Energy"}
    for x in d:
        value = str(countBars(round(info[x])) * bar) + " " + str(round(info[x]))
        embed.add_field(name=d[x], value=value, inline=inline)

    # print(countBars(round(info["health"]))*bar)
    # embed.add_field(name="Defense", value=str(countBars(round(info["defense"]))*bar), inline=inline)
    # print(countBars(round(info["defense"]))*bar)
    # embed.add_field(name="Energy", value=str(countBars(round(info["energy"]))*bar), inline=inline)
    # print(countBars(round(info["energy"]))*bar)
    return embed


def getFightIndex(userid):
    i = 0
    for x in gv.fight:
        if (not "waitingFor" in list(x)) and x["cur"] == userid:
            return i
    return None


def displayAttacks(userid, bot, message):
    return message.channel.send("""it is %s's turn. your moves:
                            `?attack`: use 25%% of your current energy to deal damage
                            `?supreme attack`: use 50%% of your current energy to deal damage
                            `?defend`: wear some gear to defend yourself
                            `?sleep`: you have a 60%% chance to safely sleep. if you're lucky, you'll get some energy back
                            `?hospital`: lets you heal up, but this will cost you 500 coins! There is a 10%% chance you will die on your way there though..
                            `?annoy`: annoy your opponent and have a 20%% chance to drain ALL his energy
                            `?eat`: eat some good food and gain energy""")


def ifAttacking(message):
    attacks = ["?attack", "?supreme attack", "?defend", "?sleep", "?hospital", "?annoy", "?eat"]
    for x in attacks:
        if message.content.startswith(x):
            return x
    return None


def calculateDiff(old, new, curid, oppid, bot):
    found = []
    for userid in [curid, oppid]:
        mention = bot.get_user(userid).mention

        for feature in ["health", "defense", "energy"]:

            if new[userid][feature] > old[userid][feature]:
                diff = new[userid][feature] - old[userid][feature]
                found.append("**%s gained %s %s!**" % (getName(userid, bot), round(diff), feature))

            elif new[userid][feature] < old[userid][feature]:
                diff = old[userid][feature] - new[userid][feature]
                found.append("**%s lost %s %s!**" % (getName(userid, bot), round(diff), feature))
    if found == []:
        found.append("**nothing happened!**")
    return found


# limits values to between 0 and 100
def fixOffsets(i, curid, oppid):
    for userid in [curid, oppid]:
        for feature in ["health", "defense", "energy"]:
            if gv.fight[i][userid][feature] > 100:
                gv.fight[i][userid][feature] = 100
            elif gv.fight[i][userid][feature] < 0:
                gv.fight[i][userid][feature] = 0


class ShopCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        msg = message.content.split()
        msg2 = message.content
        if message.author == self.bot.user:
            return

        if message.content[0] != "?" and (not (message.author.id in gv.chain)):
            return

        elif message.content.startswith("?shop") and (not (message.author.id in gv.chain)):
            agents = gv.readFile("agents.json")
            if not (str(message.author.id) in agents):
                await message.channel.send(
                    "%s you aren't an agent of the daisy squad. type `?join squad` to join :)" % message.author.mention)
                return
            if len(msg) == 2:
                embed = embedShop(int(msg[1]))
            else:
                embed = embedShop(1)
            await message.channel.send(embed=embed)

        elif message.content.startswith("?profile") and (not (message.author.id in gv.chain)):
            embed = embedProfile(message.author.id, self.bot)
            await message.channel.send(embed=embed)
            # img = discord.File("images/cool.jpg", filename="test")
            # await channel.send("content", file=img)




        elif message.content.startswith("?buy") and (not (message.author.id in gv.chain)):
            # read what item is going to be bought
            userid = str(message.author.id)
            try:
                item = " ".join(msg[1:])
            except IndexError:
                await message.channel.send("sir, you've got to tell me what item u wanna buy :P. try the command again")
                return

            item = item.lower()

            # check if items exists in shop
            shop = gv.readFile("shop.json")

            if not (item in [x.lower() for x in list(shop)]):
                await message.channel.send("uhh the item you have listed does not exist?")
                return

            # get cost of item
            cost = shop[item]["cost"]
            itemType = shop[item]["type"]

            # change value of coins
            agents = gv.readFile("agents.json")
            if cost > agents[str(userid)]["coins"]:
                await message.channel.send(
                    "you do not have enough money to buy this item! help daisy out more to earn more coins")
                return
            agents[str(userid)]["coins"] -= cost

            # add item to inventory
            agents[userid][itemType].append(item)
            gv.writeFile("agents.json", agents)
            await message.channel.send("you have bought 1 " + item + ". type `?use " + item + "` to use that item")

        elif message.content.startswith("?use") and (not (message.author.id in gv.chain)):
            # read what item is going to be used
            userid = str(message.author.id)
            try:
                item = " ".join(msg[1:])
            except IndexError:
                await message.channel.send("sir, you've got to tell me what item u wanna use :P. try the command again")
                return

            item = item.lower()

            if item.startswith("fortune cookie"):
                item = "fortune cookie"

            # check if item is in player's inventory
            agents = gv.readFile("agents.json")
            inventory = agents[str(message.author.id)]["items"] + agents[str(message.author.id)]["houses"] + \
                        agents[str(message.author.id)]["weapons"] + agents[str(message.author.id)]["trophies"]
            shop = gv.readFile("shop.json")

            if not (item in inventory):
                if not (item in shop):
                    await message.channel.send(
                        "that item you just talked about does not exist. Please type `?shop` for list of items.")
                    return
                else:
                    await message.channel.send(
                        "you dont have that item currently. if you would like to buy it, please type `?buy " + item + "`")
                return

            # use the item
            if item == "fortune cookie":
                fortune = random.choice(gv.readFile("fortunes.json")["list"])
                await message.channel.send(random.choice(shop[item]["gifs"]))
                await message.channel.send("opening fortune cookie.. :fortune_cookie:")
                await message.channel.send("**" + fortune + "**")
            elif item == "cookie":
                await message.channel.send(random.choice(shop[item]["gifs"]))
                await message.channel.send(random.choice(shop[item]["reactions"]))
            elif item == "pizza":
                await message.channel.send(random.choice(shop[item]["gifs"]))
                await message.channel.send(random.choice(shop[item]["reactions"]))
            elif item in ["wooden sword", "iron sword", "diamond sword"]:
                await message.channel.send("please type `?fight [player] [coins that you bet]` to fight")

            # remove item from person's inventory
            for x in ["items", "weapons", "trophies, houses"]:
                try:
                    agents[str(message.author.id)][x].remove(item)
                except ValueError:
                    pass  # do nothing!

            # add xp to player
            xpGain = shop[item]["xp"]
            if xpGain != -404:
                await message.channel.send("you also gained **" + str(xpGain) + " XP** !")
                agents[str(message.author.id)]["xp"] += xpGain
                gv.writeFile("agents.json", agents)

        # fight has dicts having the following format:
        # {cur: id, opp:id, id: [weapon, health, defense, energy, bet amt], id: [weapon, health, defense, energy, bet amt.]
        elif message.content.startswith("?fight"):

            await message.channel.send("This command is still in development. Please be patient :3")
            return

            if message.author.id in gv.chain and gv.chain[message.author.id][0] in ["cur", "opp"]:
                await message.channel.send(
                    "You're already in a game. Please type `?forfeit` if you wanna give up and pay the price")
                return
            # if message.author.id

            elif message.author.id in gv.chain:
                return

            if len(msg) != 3:
                await message.channel.send("You're using the wrong format. Please use `?fight [@user] [bet amt]`")
                return

            # check if fight isnt already available
            curid = message.author.id
            ping = str(msg[1])[3:-1]
            betAmt = int(msg[2])

            weapon = getWeapon(message.author.id)

            health = 100
            defense = 25
            energy = 50
            # update fight list
            gv.fight.append({"waitingFor": int(ping), "cur": curid,
                             curid: {"weapon": weapon, "health": 100, "defense": 25, "energy": 50, "betAmt": betAmt}})

            await message.channel.send(
                "%s, %s has requested to fight with you with a %s. Whoever wins gets %s coins from the other person. please type `?accept fight` or `?reject fight`. \nneither of you will win or lose money if you reject." % (
                msg[1], message.author.mention, weapon, betAmt))




        elif message.content.startswith("?reject fight") and (not (message.author.id in gv.chain)):

            # check if fight exists
            rejected = False
            for x in gv.fight:
                if "waitingFor" in list(x) and message.author.id == x["waitingFor"]:
                    gv.fight.remove(x)
                    rejected = True

                    await message.channel.send("%s has rejected %s's request to fight" % (
                    message.author.mention, self.bot.get_user(x["cur"]).mention))
                    return

            await message.channel.send("There is nothing for you to currently reject")

        elif message.content.startswith("?accept fight") and (not (message.author.id in gv.chain)):

            # check if fight exists
            accepted = False
            i = 0
            for x in gv.fight:
                if "waitingFor" in list(x) and message.author.id == x["waitingFor"]:
                    gv.fight[i].pop("waitingFor")
                    weapon = getWeapon(message.author.id)
                    health = 100
                    defense = 25
                    energy = 50
                    curid = gv.fight[i]["cur"]
                    gv.fight[i]["opp"] = message.author.id
                    oppid = gv.fight[i]["opp"]

                    gv.fight[i][oppid] = {"weapon": weapon, "health": 100, "defense": 25, "energy": 50,
                                          "betAmt": gv.fight[i][curid]["betAmt"]}
                    # gv.fight[i]["gamestate"] = "host turn"

                    accepted = True
                    # await message.channel.send("%s, please play. %s" % (self.bot.get_user(x["host"]).mention, gv.fight))
                    await displayAttacks(curid, self.bot, message)

                    gv.chain[int(curid)] = ["cur", message.channel.id]
                    gv.chain[message.author.id] = ["opp", message.channel.id]
                    return
                i += 1

            await message.channel.send("There is nothing for you to currently accept")

        # def checkInFight(usrid, ):

        elif ifAttacking(message) and (gv.chain[message.author.id][0] in ["cur", "opp"]):
            if gv.chain[message.author.id][1] != message.channel.id:
                await message.channel.send("you must attack from the channel your fight started")
                return

            if gv.chain[message.author.id][0] == "opp":
                await message.channel.send("You cannot play yet. It is your opponents turn!")
                return
            if gv.chain[message.author.id][0] != "cur":
                await message.channel.send(
                    "You need to be in a game to use this move. Type `fight [user] [betAmt]` to fight someone.")
            userid = message.author.id

            """it is %s's turn. your moves:
            `?attack`: use 50%% of your current energy to deal damage
            `?supreme attack`: use 100%% of your current energy to deal damage
            `?defend`: wear some gear to defend yourself
            `?sleep`: you have a 60%% chance to sleep and get some energy back
            `?hospital`: lets you heal up, but this will cost you 500 coins! There is a 10%% chance you will die on your way there though..
            `?annoy`: annoy your opponent and have a 20%% chance to drain ALL his energy
            `?eat`: eat some good food and gain energy"""

            i = getFightIndex(userid)
            if i == None:
                return

            curid = gv.fight[i]["cur"]
            oppid = gv.fight[i]["opp"]
            oldFightData = copy.deepcopy(gv.fight[i])
            attack = ifAttacking(message)

            if attack == "?attack":
                if gv.fight[i][curid]["energy"] == 0:
                    await message.channel.send("You do not have enough energy to use this. Please use another command")
                    return
                energy = 1 / 4 * (gv.fight[i][curid]["energy"])
                gv.fight[i][curid]["energy"] -= energy

                defense = gv.fight[i][oppid]["defense"]
                damage = random.randrange(0, int(energy)) * 4
                if defense > damage:
                    defense = damage

                gv.fight[i][oppid]["health"] -= damage - defense
                gv.fight[i][oppid]["defense"] -= damage

            if attack == "?supreme attack":
                if gv.fight[i][curid]["energy"] == 0:
                    await message.channel.send("You do not have enough energy to use this. Please use another command")
                    return
                energy = 1 / 2 * (gv.fight[i][curid]["energy"])
                gv.fight[i][curid]["energy"] -= energy

                defense = gv.fight[i][oppid]["defense"]
                damage = random.randrange(0, int(energy)) * 4
                if defense > damage:
                    defense = damage

                gv.fight[i][oppid]["health"] -= damage - defense
                gv.fight[i][oppid]["defense"] -= damage

            elif attack == "?defend":
                if gv.fight[i][curid]["defense"] >= 100:
                    await message.channel.send("You'e already at max defense. Use a different command!")
                    return
                gv.fight[i][curid]["defense"] += random.randrange(0, 50)

            elif attack == "?sleep":
                if gv.fight[i][curid]["energy"] >= 100:
                    await message.channel.send("You'e already at max energy. Use a different command!")
                    return

                if random.randrange(0, 101) < 60:
                    gv.fight[i][curid]["energy"] += random.randrange(0, 100)
                else:
                    pass
            elif attack == "?hospital":
                agents = gv.readFile("agents.json")
                if agents[str(curid)]["coins"] < 500:
                    await message.channel.send("you do not have 500 coins. Please use another command!")
                agents[str(curid)]["coins"] -= 500
                await message.channel.send("you payed 500 coins to go to the hospital")
                gv.writeFile("agents.json", agents)
                if random.randrange(0, 101) < 90:
                    gv.fight[i][curid]["health"] += random.randrange(50, 100)

            # elif attack == "?supreme attack":

            fixOffsets(i, curid, oppid)
            responses = calculateDiff(oldFightData, gv.fight[i], curid, oppid, self.bot)
            for x in responses:
                await message.channel.send(x)
            if gv.fight[i][curid]["health"] == 0 or gv.fight[i][oppid]["health"] == 0:
                if gv.fight[i][curid]["health"] == 0:
                    loser = self.bot.get_user(curid)
                    winner = self.bot.get_user(oppid)
                else:
                    loser = self.bot.get_user(oppid)
                    winner = self.bot.get_user(curid)

                await message.channel.send("%s has died!!!! GJ %s! You have won! GG" % (loser.mention, winner.mention))
                betAmt = gv.fight[i][winner]["betAmt"]
                # exchange money
                agents = gv.readFile("agents.json")
                agents[str(loser.id)]["coins"] -= betAmt
                agents[str(winner.id)]["coins"] += betAmt
                gv.writeFile("agents.json", agents)

                await message.channel.send("%s has won %s coins from %s!" % (winner.mention, betAmt, winner.mention))
                gv.fight.pop(i)

            # display current stage of fight
            await message.channel.send(embed=playerInfo(oppid, self.bot, gv.fight[i][oppid]))
            await message.channel.send("it is now %s's turn" % self.bot.get_user(oppid).mention)

            # switch turns, cur and opp
            gv.fight[i]["cur"] = oppid
            gv.fight[i]["opp"] = curid
            gv.chain[curid][0] = "opp"
            gv.chain[oppid][0] = "cur"

            return
        elif message.content.startswith("?showdata"):
            await message.channel.send("you attacked your opponent! %s" % gv.fight)


def setup(bot):
    bot.add_cog(ShopCog(bot))


"""
-studio
-clothing (obsesses, life is her canvas. canvas is her life)
-soundtracks (take you on a journey, help create intensity in painting)
-writing (writing to capture thought for painting)
-studio (whole studio is diary of herself)
-teddy left (questioned what it means to)
-how different things in her life connect to be represented in her artwork

"""
