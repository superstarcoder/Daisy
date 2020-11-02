import discord
from discord.ext import commands
import globalVars as gv
# from profanity_check import predict, predict_prob
import backend
import random


class ChatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        confused = ["oh uhhh","mm","uhh","wym","mmmmm","oh ok"]
        msg = message.content.split()
        msg2 = message.content
        if message.author == self.bot.user:
            return

        if message.content[0] != "?" and (not (message.author.id in gv.chain)):
            data = gv.readFile("setupLocs.json")
            user = self.bot.get_user(int(message.author.id))
            user = user.name
            varsDict = {"%name%": user}

            if (str(message.channel.id) in data) and data[str(message.channel.id)] == "ON":
                if not (message.author.id in gv.silence):
                    async with message.channel.typing():
                        msg = backend.chatbot_response(message.content, varsDict)
                else:
                    msg = backend.chatbot_response(message.content, varsDict)
                if msg == "//help":
                    await message.channel.send(embed=gv.helpem)
                    if message.author.id in gv.silence:
                        gv.silence.remove(message.author.id)
                elif msg == "//confused":
                    if not (message.author.id in gv.silence):
                        gv.silence.append(message.author.id)
                        await message.channel.send(random.choice(confused))
                        agents = gv.readFile("agents.json")
                        if not (str(message.author.id) in agents):
                            await message.channel.send("NOTE: if you wanna help me become smarter, type `?suggest`")

                else:
                    await message.channel.send(msg)
                    if message.author.id in gv.silence:
                        gv.silence.remove(message.author.id)


# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(ChatCog(bot))
