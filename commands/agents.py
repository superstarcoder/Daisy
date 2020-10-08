import discord
from discord.ext import commands
import globalVars as gv
#from profanity_check import predict, predict_prob

def embedMsg(description):
    color=0xf5a742
    embed=discord.Embed(color=color, description=description)
    return embed
    


class AgentsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()    
    async def on_message(self, message):
        print(message)
        msg = message.content.split()
        msg2 = message.content
        if message.author == self.bot.user:
            return
        

    
        elif message.content.startswith("?suggest") and (not (message.author.id in gv.chain)):
            bans = gv.readFile("bans.json")
            if str(message.author.id) in bans:
                await self.bot.get_user(message.author.id).send("You cannot do any agent commands since you have been banned! Please talk to danny to negotiate.")
                return

            agents = gv.readFile("agents.json")
            if str(message.author.id) in agents:
                embed=embedMsg("""%s alrightt. tell me what the input should be. Please note:

                        -minimum 3 inputs required
                        -input must be seperated by commas
                        -keep your inputs as diverse as possible
                        -nothing inappropriate
    example:
    `hey who are you, what are you, are you a robot?`""" % message.author.mention)
                await message.channel.send(embed=embed)

                gv.chain[message.author.id] = "suggest1"
            else:
                embed = embedMsg("""%s you aren't an agent of the daisy squad. type `?join squad` to join :)""" % message.author.mention)
                await message.channel.send(embed=embed)

        elif (message.author.id in gv.chain) and gv.chain[message.author.id] == "suggest1":
            agents = gv.readFile("agents.json")

            if str(message.author.id) in agents:
                
                print("ive created the suggestion dict")
                gv.suggestion[message.author.id] = {}

                gv.suggestion[message.author.id]["patterns"] = [x.strip() for x in message.content.split(',')]

                if len(message.content.split(",")) < 3:
                    embed = embedMsg("""%s You must have at least 3 inputs required (seperated by a comma). Type `?suggest` again to restart""" % message.author.mention)
                    await message.channel.send(embed=embed)
                    gv.chain.pop(message.author.id)
                    gv.suggestion.pop(message.author.id)
                #elif float(predict_prob([message.content])[0]*100) > 65:
                elif False:
                    embed=embedMsg("""%s You just said something that either contains a bad word or is not age appropriate. You have been warned. Please understand that further action as such will result in a ban from using this bot""" % message.author.mention)
                    await message.channel.send(embed=embed)
                    gv.chain.pop(message.author.id)
                    gv.suggestion.pop(message.author.id)

                else:

                    embed = embedMsg("""%s alrightt. tell me what the output should be. Please note:
                        -minimum 1 output required
                        -output must be seperated by commas
                        -output should be a response to the input
                        -nothing inappropriate
    example:
    `I chose to be a robot because humans are weird!, actually i do not know`""" % message.author.mention)
                    await message.channel.send(embed=embed)
                    gv.chain[message.author.id] = "suggest2"
            else:
                embed=embedMsg("""%s you aren't an agent of the daisy squad. type `?join squad` to join :)""" % message.author.mention)
                await message.channel.send(embed=embed)

        elif (message.author.id in gv.chain) and gv.chain[message.author.id] == "suggest2":
            
            agents = gv.readFile("agents.json")
            if str(message.author.id) in agents:
                
                gv.suggestion[message.author.id]["responses"] = [x.strip() for x in message.content.split(',')]
                gv.suggestion[message.author.id]["id"] = message.author.id

                #if float(predict_prob([message.content])[0]*100) > 65:
                if False:
                    embed=embedMsg("""%s You just said something that either contains a bad word or is not age appropriate. You have been warned. Please understand that further action as such will result in a ban from using this bot""" % message.author.mention)
                    await message.channel.send(embed=embed)
                    gv.chain.pop(message.author.id)
                    gv.suggestion.pop(message.author.id)

                else:
                    embed=embedMsg("""%s alrightt your suggestion has been made. thank you SO MUCH! your suggestion will be reviewed anytime between 5 seconds to 24 hours later, and you will recieve your credit! Also, **you can suggest more**, but make sure your data is quality and meets the requirements""" % message.author.mention)
                    await message.channel.send(embed=embed)
                    gv.chain.pop(message.author.id)
                    #code to increase credits




                    suggestions = gv.readFile("suggestions.json")
                    agents = gv.readFile("agents.json")
                    if not(str(message.author.id) in suggestions):
                        suggestions[str(message.author.id)] = []
                        print("so ive added it in")
                        print( suggestions[str(message.author.id)])
                        print(gv.suggestion)
                        print(gv.suggestion[message.author.id])
                    suggestions[str(message.author.id)].append(gv.suggestion[message.author.id])

                    
                    gv.writeFile("suggestions.json", suggestions)


                    await self.bot.get_user(message.author.id).send("Thanks for suggesting! :)")
                    await self.bot.get_user(gv.admin).send("someone just suggested. nice")


            

            else:
                embed=embedMsg("""%s you aren't an agent of the daisy squad. type `?join squad` to join :)""" % message.author.mention)
                await message.channel.send(embed=embed)



# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(AgentsCog(bot))
