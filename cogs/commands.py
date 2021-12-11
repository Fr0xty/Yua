import discord
from discord.ext import commands
import asyncio
from discord_components import *
import os
from datetime import datetime

import config



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

    helpEmbed = []
    embed = discord.Embed( 
      title = "in progress",
      description = f"""
I host **24 hour** music channels! I'm only in a *few selected servers*.

My prefix is `yua`
__I'm under development and I will have more features in the future__ 

Github Repo: https://github.com/Fr0xty/Yua

`setup`
To setup me in the server
""",
      colour = 14982399,
      timestamp=datetime.utcnow()
    )
    embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
    embed.add_field(name = "`addsong <url>`", value = "add song to the server playlist", inline = False)
    embed.add_field(name = "`remsong <index>`", value = "remove song from server playlist", inline = False)
    embed.add_field(name = "`serverplaylist`", value = "get server playlist", inline = False)
    embed.add_field(name = "`vc`", value = "get which voice channel I'm playing in", inline = False)
    embed.add_field(name = "`changevc`", value = "change which channel i play in", inline = False)
    embed.add_field(name = "`serverreset`", value = "remove data of __vc__ and __server playlist__", inline = False)
    embed.add_field(name = "`clearplaylist`", value = "clear all songs from server playlist", inline = False)

    helpEmbed.append(embed)

    await ctx.send(embed = helpEmbed[0])




def setup(client):
  client.add_cog(command(client))