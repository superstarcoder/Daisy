import discord
from discord.ext import commands
import globalVars as gv


class SwitchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='turn')
    @commands.Cog.listener()    
    async def on_message(self, message):
        bans = gv.readFile("bans.json")
        if str(message.author.id) in bans:
            await self.bot.get_user(message.author.id).send("You cannot do any agent commands since you have been banned! Please talk to danny to negotiate.")
            return


        print(message.message)
        msg = message.message.content.split()
        if message.author == self.bot.user:
            return

        elif msg[1] == "on":
        #if user has daisy role
            if message.guild == None or any("daisy" == x.name for x in message.author.roles):
                data = gv.readFile("setupLocs.json")
                data[str(message.channel.id)] = "ON"

                gv.writeFile("setupLocs.json", data)

                await message.channel.send("wakey wakey. i have turned on :)")
            else:
                await message.channel.send("you can turn me on only if you have the daisy role :<")


        elif msg[1] == "off":
            if message.guild == None or any("daisy" == x.name for x in message.author.roles):
                data = gv.readFile("setupLocs.json")
                data[str(message.channel.id)] = "OFF"

                gv.writeFile("setupLocs.json", data)

                await message.channel.send("yawn. i am going to turn off. good ni- ZZZZZZZzzzzzz....")
            else:
                await message.channel.send("you can turn me off only if you have the daisy role :<")

    @commands.Cog.listener()    
    async def temp(self, message):
        print(message)
        msg = message.content.split()
        msg2 = message.content
        if message.author == self.bot.user:
            return
        if not (msg2.startswith("?")):
            await message.channel.send("yay")


# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(SwitchCog(bot))
