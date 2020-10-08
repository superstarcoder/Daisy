# Work with Python 3.6
import discord
import random
#import backend
from discord.utils import get
#from profanityfilter import ProfanityFilter
from time import gmtime, strftime
import json
from emoji import UNICODE_EMOJI
from discord.ext import commands
import sys, traceback
from os import listdir
from os.path import isfile, join

#pf = ProfanityFilter()


def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # Notice how you can use spaces in prefixes. Try to keep them simple though.
    prefixes = ['?']

    #we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)

bot = commands.Bot(command_prefix=get_prefix, description='cog test')
bot.remove_command("help")



cogs_dir = "commands"
# Here we load our extensions(cogs) that are located in the cogs directory. Any file in here attempts to load.
if __name__ == '__main__':
    for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
        try:
            bot.load_extension(cogs_dir + "." + extension)
        except (discord.ClientException, ModuleNotFoundError):
            print(f'Failed to load extension {extension}.')
            traceback.print_exc()

#$ git add .
#$ git commit -m "Initial commit"
#$ git push

#data = setupLocs data
#chain = user chain (used for responding to a particular user's messages)
#agents = agents data
global data, chain, agents, suggestion


#for turning on or turning off
with open("json/setupLocs.json", "r") as f:
    data = json.load(f)

with open("json/agents.json", "r") as f:
    agents = json.load(f)


admin = 545063650088452127

#chain for users. allows multiple users to do commands that require more than one message
chain = {}
#suggestions that are still being processed. dictionary of: user ids to suggestion dicts
suggestion = {}

print("ye cool")
@bot.event
async def on_ready():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""

    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

TOKEN = "NzM1Njc5NTExMjEwNzU0MTgx.XxjyIg.JKXEoDCRZjdCFMwzeD_Px3SuzUQ"
bot.run(TOKEN)
