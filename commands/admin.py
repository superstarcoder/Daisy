import discord
from discord.ext import commands
import globalVars as gv
import importlib
#import train_chatbot


# checks if tag is already in intents.json
def checkTag(tag, intents):
    return any(tag == x["tag"] for x in intents["intents"])


def embedMsg(description):
    color = 0xf5a742
    embed = discord.Embed(color=color, description=description)
    return embed


class joinSquadCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        msg = message.content.split()
        if message.author == self.bot.user:
            return
        if message.author.id != gv.admin:
            return

        if message.author.id == gv.admin and message.content == "?info":

            suggestions = gv.readFile("suggestions.json")
            num = 0
            for x in suggestions:
                num += len(suggestions[x])

            msg = """
    %s users have suggested
    %s unreviewed suggestions""" % (len(suggestions), num)
            embed = discord.Embed(color=0x00ff00, description="")
            embed.add_field(name="number of users suggested:", value=len(suggestions), inline=False)
            embed.add_field(name="number of unreviewed suggestions:", value=num, inline=False)
            await message.channel.send(embed=embed)

        elif message.author.id == gv.admin and message.content == "?train":
            try:
                if gv.alreadyImported:
                    import train_chatbot
                    importlib.reload(train_chatbot)
                else:
                    import train_chatbot
                    gv.alreadyImported = True
                await message.channel.send("I've been trained!")
                import backend
                backend.reloadModel()
            except Exception as e:
                await message.channel.send("OOF THERES AN  ERROR: `%s`" % e)


        elif message.author.id == gv.admin and message.content == "?load":
            try:
                suggestions = gv.readFile("suggestions.json")
                userid = list(suggestions)[0]
                user = self.bot.get_user(int(userid))
                user = user.name + "#" + user.discriminator

                embed = discord.Embed(color=0x00ff00, description="oh")
                embed.add_field(name="ID", value=userid, inline=False)
                embed.add_field(name="user", value=user, inline=False)
                embed.add_field(name="patterns", value=suggestions[userid][0]["patterns"], inline=False)
                embed.add_field(name="responses", value=suggestions[userid][0]["responses"], inline=False)
                await message.channel.send(embed=embed)

                # await message.channel.send("**suggestion**:\n"+str(suggestions[userid][0]))
                # msg = """

                #    help on admin commands:
                #    `?approve [coins] [tag] [update automatically yes/no] [comment (default already exists)]`
                #    `?reject [comment (optional)]`
                #    `?warn [warnID] [warnValue] [comment (optional)]`
                # """
                # await message.channel.send(msg)
            except IndexError:
                msg = "no suggestions yet"
                await message.channel.send(msg)

        # ?approve [coins] [tag] [update automatically yes/no] [comment (default already exists)]
        elif message.author.id == gv.admin and message.content.startswith("?approve"):
            if len(message.content.split()) >= 4:
                msg = message.content.split()

                # store arguments to vars
                coins = int(msg[1])
                tag = msg[2]
                update = msg[3]
                comment = "your suggestion has been approved. TYSM for contributing! :D You have recieved `%s coins.` GJ" % coins

                if checkTag(tag, gv.readFile("intents.json")):
                    await message.channel.send("hey! that tag already exists!")
                    return

                if len(message.content.split()) > 4:
                    comment = "your suggestion has been approved. You have received `%s coins.` GJ. comment from admin: `%s`" % (coins, " ".join(msg[4:]))

                # get userid who suggested
                suggestions = gv.readFile("suggestions.json")

                userid = list(suggestions)[0]

                # edit agents file and add coins

                agents = gv.readFile("agents.json")

                agents[userid]["coins"] += coins
                agents[userid]["xp"] += int(coins / 5)
                agents[userid]["suggestionCount"] += 1
                agents[userid]["approvedSuggestionCount"] += 1

                gv.writeFile("agents.json", agents)

                # message user with comment
                await self.bot.get_user(int(userid)).send(comment)

                # add tag to suggestion dict
                suggestions[userid][0]["tag"] = tag

                # add suggestion to intents.json
                if update == "yes":
                    intents = gv.readFile("intents.json")

                    intents["intents"].append(suggestions[userid][0])

                    gv.writeFile("intents.json", intents)
                    await self.bot.get_user(gv.admin).send("dataset has been updated")

                # remove suggestion from suggestion.json
                suggestions[userid].pop(0)
                if suggestions[userid] == []:
                    suggestions.pop(userid)

                gv.writeFile("suggestions.json", suggestions)

            else:
                await message.channel.send(
                    "ERROR! required format: `?approve [coins] [tag] [update automatically yes/no] [comment (default already exists)]`")

        ###############################################################################################################################################
        # ?reject [comment (optional)]
        elif message.author.id == gv.admin and message.content.startswith("?reject"):
            # get userid who suggested
            suggestions = gv.readFile("suggestions.json")
            if list(suggestions) == []:
                await message.channel.send("no suggestions to reject")
                return


            userid = list(suggestions)[0]

            # remove suggestion from suggestion.json
            suggestions[userid].pop(0)
            if suggestions[userid] == []:
                suggestions.pop(userid)

            gv.writeFile("suggestions.json", suggestions)

            # add suggestionCount to agent profile
            agents = gv.readFile("agents.json")

            agents[userid]["suggestionCount"] += 1

            gv.writeFile("agents.json", agents)

            # message user that suggestion has not been made
            if len(message.content.split()) > 1:
                comment = "your suggestion has been rejected. comment from admin: `%s`" % " ".join(message.content.split()[1:])
            else:
                comment = "your suggestion has been rejected. try suggesting one that will be useful for me to learn from! :D"
            await self.bot.get_user(int(userid)).send(comment)

        # ?warn [warnID] [warnValue] [comment (optional)]
        elif message.author.id == gv.admin and message.content.startswith("?warn"):
            # assign args to vars
            msg = message.content.split()
            warnid = msg[1]
            warnValue = int(msg[2])
            comment = "You just suggested data that contains a bad word, is considered as spam, or is not age appropriate. You have been warned. Please understand that further action as such will result in a ban from using this bot"
            if len(msg) > 3:
                comment = "comment from admin: " + " ".join(msg[3:])

            # add warnings to agent profile
            agents = gv.readFile("agents.json")

            agents[warnid]["warnings"] += warnValue

            gv.writeFile("agents.json", agents)

            # dm user that needs to be warned
            await self.bot.get_user(int(warnid)).send(comment)
        ###############################################################################################################################################
        # ban [userid]
        elif message.author.id == gv.admin and message.content.startswith("?ban"):
            msg = message.content.split()
            if len(str(msg[1])) != 18:
                await message.channel.send("hey admin, ur gunna have to use the user id number, not the ping")
                return

            bans = gv.readFile("bans.json")
            if str(message.author.id) in bans:
                await message.channel.send("user has been banned already before")
            else:
                bans[msg[1]] = "banned"
                gv.writeFile("bans.json", bans)
                await message.channel.send("user has been banned successfuly!")
        # unban [userid]
        elif message.author.id == gv.admin and message.content.startswith("?unban"):
            msg = message.content.split()
            bans = gv.readFile("bans.json")
            if str(message.author.id) in bans:
                bans.pop(msg[1])
                gv.writeFile("bans.json", bans)
                await message.channel.send("user has been unbanned successfuly!")
            else:
                await message.channel.send("user has been unbanned already before")
        ###############################################################################################################################################

        elif message.author.id == gv.admin and message.content.startswith("?add") and (
                not (message.author.id in gv.chain)):
            bans = gv.readFile("bans.json")
            if str(message.author.id) in bans:
                await self.bot.get_user(message.author.id).send(
                    "You cannot do any agent commands since you have been banned! Please talk to danny to negotiate.")
                return

            agents = gv.readFile("agents.json")
            if len(message.content.split()) != 3:
                await message.channel.send(
                    "you did not follow the correct format. you must do: ?add `[ID of agent who suggested] [tag]`")
            elif str(message.author.id) in agents:
                gv.agentId = int(message.content.split()[1])
                gv.tempTag = message.content.split()[2]
                if checkTag(gv.tempTag, gv.readFile("intents.json")):
                    await message.channel.send("tag already exists")
                    return
                embed = embedMsg("""%s alrightt. tell me what the input should be. Please note:

                        -minimum 3 inputs required
                        -input must be seperated by commas
                        -keep your inputs as diverse as possible
                        -nothing inappropriate
    example:
    `hey who are you, what are you, are you a robot?`""" % message.author.mention)
                await message.channel.send(embed=embed)

                gv.chain[message.author.id] = "add1"
            else:
                embed = embedMsg(
                    """%s you aren't an agent of the daisy squad. type `?join squad` to join :)""" % message.author.mention)
                await message.channel.send(embed=embed)

        elif message.author.id == gv.admin and (message.author.id in gv.chain) and gv.chain[
            message.author.id] == "add1":
            agents = gv.readFile("agents.json")

            if str(message.author.id) in agents:

                gv.suggestion[message.author.id] = {}

                gv.suggestion[message.author.id]["patterns"] = [x.strip() for x in message.content.split(',')]
                gv.suggestion[message.author.id]["tag"] = gv.tempTag

                if len(message.content.split(",")) < 3:
                    embed = embedMsg(
                        """%s You must have at least 3 inputs required (seperated by a comma). Type `?add` again to restart""" % message.author.mention)
                    await message.channel.send(embed=embed)
                    gv.chain.pop(message.author.id)
                    gv.suggestion.pop(message.author.id)
                # elif float(predict_prob([message.content])[0]*100) > 65:
                # elif False:
                #     embed = embedMsg(
                #         """%s You just said something that either contains a bad word or is not age appropriate. You have been warned. Please understand that further action as such will result in a ban from using this bot""" % message.author.mention)
                #     await message.channel.send(embed=embed)
                #     gv.chain.pop(message.author.id)
                #     gv.suggestion.pop(message.author.id)

                else:

                    embed = embedMsg("""%s alrightt. tell me what the output should be. Please note:
                        -minimum 1 output required
                        -output must be seperated by commas
                        -output should be a response to the input
                        -nothing inappropriate
    example:
    `I chose to be a robot because humans are weird!, actually i do not know`""" % message.author.mention)
                    await message.channel.send(embed=embed)
                    gv.chain[message.author.id] = "add2"
            else:
                embed = embedMsg(
                    """%s you aren't an agent of the daisy squad. type `?join squad` to join :)""" % message.author.mention)
                await message.channel.send(embed=embed)

        elif message.author.id == gv.admin and (message.author.id in gv.chain) and gv.chain[
            message.author.id] == "add2":

            agents = gv.readFile("agents.json")
            if str(message.author.id) in agents:

                gv.suggestion[message.author.id]["responses"] = [x.strip() for x in message.content.split(',')]
                gv.suggestion[message.author.id]["id"] = gv.agentId

                # if float(predict_prob([message.content])[0]*100) > 65:
                # if False:
                #     embed = embedMsg(
                #         """%s You just said something that either contains a bad word or is not age appropriate. You have been warned. Please understand that further action as such will result in a ban from using this bot""" % message.author.mention)
                #     await message.channel.send(embed=embed)
                #     gv.chain.pop(message.author.id)
                #     gv.suggestion.pop(message.author.id)

                if True:
                    embed = embedMsg("""%s alrightt your addition has been made""" % message.author.mention)
                    await message.channel.send(embed=embed)
                    gv.chain.pop(message.author.id)

                    intents = gv.readFile("intents.json")
                    intents["intents"].append(gv.suggestion[message.author.id])

                    gv.writeFile("intents.json", intents)

            else:
                embed = embedMsg(
                    """%s you aren't an agent of the daisy squad. type `?join squad` to join :)""" % message.author.mention)
                await message.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(joinSquadCog(bot))
