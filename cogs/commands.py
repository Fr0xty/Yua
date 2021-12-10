import discord
from discord.ext import commands
import asyncio
from discord_components import *
import os

import config


client = discord.Client()

















class command(commands.Cog):

  def __init__(self, client):
    self.client = client


  client = commands.Bot(command_prefix = config.prefixList, case_insensitive=True, intents = discord.Intents().all())
  client.remove_command('help')                 #remove default built-in help command
  





  @commands.command()
  async def rename(self, ctx, name):
    if ctx.author.id == 395587171601350676:
      await self.client.user.edit(username=name)



  @commands.command()
  async def help(self, ctx):

    helpEmbed = discord.Embed( 
      title = "in progress",
      description = f"""
I host **24 hour** music channels! I'm only in a *few selected servers*.

My prefix is `yua`
__I'm under construction and I will have more features in the future__ 

`setup`
To setup me in the server
""",
      colour = 14982399
    )
    helpEmbed.set_author(name = self.client.user, icon_url = self.client.user.avatar_url)
    helpEmbed.add_field(name = "`addsong`", value = "add song to the server playlist", inline = False)
    helpEmbed.add_field(name = "`serverplaylist`", value = "get server playlist", inline = False)

    await ctx.send(embed = helpEmbed)




def setup(client):
  client.add_cog(command(client))