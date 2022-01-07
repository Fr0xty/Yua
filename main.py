import discord
import os
from discord.ext import commands
import asyncio
from discord_components import *

from keep_alive import keep_alive                         #keep online
import config


client = commands.Bot(command_prefix = config.prefixList, case_insensitive=True, intents = discord.Intents().all())
client.remove_command('help')                                 #remove default built-in help command



@client.event                                                                                         #configurations
async def on_ready():
    print('We have logged in as {0.user}'.format(client))         

    await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening, name='songs forever'))

    DiscordComponents(client)




for filename in os.listdir('./cogs'):                                             #load all extensions in 'cogs' folder
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.load_extension('jishaku')
help_command=None







keep_alive()                                                    #stay online
my_secret = os.environ['Token']        
client.run(my_secret)                                                                                #login