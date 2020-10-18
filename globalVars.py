import json
import discord

switch = 0
admin = 545063650088452127
chain = {} #for ongoing chains in other commands that require more than one message to answer
suggestion = {} #for ongoing suggestion requests
silence = [] #to those whom the "idk" is too much
fight = [] #for players to fight
alreadyImported = False #makes importing stuff easier for admin.py
#fight has dicts having the following format:
#{gamestate:"waiting/host turn/not host turn", waitingFor: id, host: id, id: [weapon, health, defense, energy, bet amt], id: [weapon, health, defense, energy, bet amt.]}

dataDir = "json/"



#help embed
helpem=discord.Embed(description=" wutup gamer okkkk I am an AI bot created by Danny. I pretend to be like a human. you can chat with me if you are bored :): \n", color=0x0080ff)
helpem.add_field(name="?turn on", value="start chatting in a particular channel. (you need a role named daisy to do this)", inline=True)
helpem.add_field(name="?turn off", value="stop chatting in a particular channel. (you need a role named daisy to do this)", inline=True)
helpem.add_field(name="chat anything with me", value=":)", inline=True)
helpem.add_field(name="search wiki", value="type search wiki and an argument for me to search wikipedia", inline=True)
helpem.add_field(name="make me laugh", value="funny coding jokes. only tru coders will get them", inline=True)
helpem.add_field(name="?join squad", value="JOIN THE EPIC DAISY SQUAD!!!!! AND BECOME AN AGENT!", inline=True)
helpem.add_field(name="?help agent", value="help for agents", inline=True)

def readFile(path):
    with open(dataDir+path, 'r') as f:
        return json.load(f)

def writeFile(path, data):
    with open(dataDir+path, 'w') as f:
        json.dump(data, f, indent=4)

#sends a msg
def send(message, messageObj):
    return messageObj.channel.send(message)
