import discord
from discord.ext import commands
import globalVars as gv


class joinSquadCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        msg = message.content.split()
        if message.author == self.bot.user:
            return

        elif message.content == "?join squad" and (not (message.author.id in gv.chain)):
            agents = gv.readFile("agents.json")
            if not (str(message.author.id) in agents):
                await message.channel.send(
                    "%s Hello! You are not yet an agent of the daisy squad. First, you have to understand what your role is. You will be contributing to my training data. By doing this, you will gain credits. You can buy SUPER COOL INGAME STUFF and MUCH MORE WITH coins and flex on your friends! type `next` to continue" % (
                        self.bot.get_user(int(message.author.id))).name)
                gv.chain[message.author.id] = "step1"
            else:
                await message.channel.send(
                    "%s you're already an agent of the daisy squad haha" % message.author.mention)

        elif (message.author.id in gv.chain) and gv.chain[message.author.id] == "step1":
            if message.content == "next":
                await message.channel.send("""%s cool! so how the data works is, there are two things: inputs and outputs. for each data unit, you must have at least 3 inputs, and 1 output. Don't understand? Here is an example:
                        input: `hey who are you, what are you, are you a robot?`
                        output: `I chose to be a robot because humans are weird!, actually i do not know`
                        so as you can see above, there are at least 3 inputs, and 1 or more outputs
                        also remember to keep your inputs as diverse as possible too.
    if you're wondering why, this ensures that the data remains in good quality for Daisy to train from
    type `next` to continue...""" % (self.bot.get_user(int(message.author.id))).name)
                gv.chain[message.author.id] = "step2"
            else:
                await message.channel.send(
                    """%s oh ummmm i think you typed something else instead of `next`. Your application for being an agent has been cancelled. Type `?join squad` again to join back :) """ % message.author.mention)
                gv.chain.pop(message.author.id)

        elif (message.author.id in gv.chain) and gv.chain[message.author.id] == "step2":
            if message.content == "next":
                await message.channel.send(
                    """%s alright cool! I need you to confirm one LAST thing. Do you agree to not suggest inappropriate data? Type `next` to AGREE and continue""" % (
                        self.bot.get_user(int(message.author.id))).name)
                gv.chain[message.author.id] = "step3"
            else:
                await message.channel.send(
                    """%s oh ummmm i think you typed something else instead of `next`. Your application for being an agent has been cancelled. Type `?join squad` again to join back :) """ % message.author.mention)
                gv.chain.pop(message.author.id)

        elif (message.author.id in gv.chain) and gv.chain[message.author.id] == "step3":
            if message.content == "next":
                await message.channel.send(
                    """%s alright YAY. YOU ARE NOW OFFICIALLY AN AGENT OF THE DAISY SQUAD! Now, anytime, you can type `?suggest` to suggest data.""" % message.author.mention)
                gv.chain.pop(message.author.id)

                agents = gv.readFile("agents.json")

                agents[str(message.author.id)] = {"xp": 0,
                                                  "coins": 0,
                                                  "suggestionCount": 0,
                                                  "approvedSuggestionCount": 0,
                                                  "warnings": 0,
                                                  "items": [],
                                                  "houses": [],
                                                  "weapons": [],
                                                  "trophies": []
                                                  }

                gv.writeFile("agents.json", agents)

            else:
                await message.channel.send(
                    """%s oh ummmm i think you typed something else instead of `next`. Your application for being an agent has been cancelled. Type `?join squad` again to join back :) """ % message.author.mention)
                gv.chain.pop(message.author.id)


def setup(bot):
    bot.add_cog(joinSquadCog(bot))
