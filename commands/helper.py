import discord
from discord.ext import commands
import globalVars as gv
#from profanity_check import predict, predict_prob
import backend


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='help')
    @commands.Cog.listener()    
    async def on_message(self, message):
        #print(message.message)
        msg = message.message.content.split()
        if message.author == self.bot.user:
            return

        if len(msg) == 1:
            await message.channel.send(embed=gv.helpem)

        elif msg[1] == "agent":
            embed=discord.Embed(color=0x0080ff)
            embed.add_field(name="?suggest", value="suggest some data to daisy bot, and also earn some coins", inline=True)
            embed.add_field(name="?profile", value="see your coins and your stats", inline=True)
            embed.add_field(name="?shop", value="buy some item from the biggest shop in town", inline=True)
            await message.channel.send(embed=embed)

        elif msg[1] == "admin":
            embed=discord.Embed(color=0x00ff00)
            embed.add_field(name="?approve", value="`[coins from 1-100]` `[tag]` `[update automatically yes/no]` `[comment (default already exists)]`", inline=False)
            embed.add_field(name="?reject", value="`[comment (optional)]`", inline=False)
            embed.add_field(name="?warn", value="`[warnID]` `[warnValue]` `[comment (optional)]`", inline=False)
            embed.add_field(name="?info", value="get suggestion numbers", inline=False)
            embed.add_field(name="?load", value="load oldest unreviewed suggestion", inline=False)
            await message.channel.send(embed=embed)


# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(HelpCog(bot))

def imp():
    import globalVars as gv
