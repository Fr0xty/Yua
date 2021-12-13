import discord
from discord.ext import commands
import json
from datetime import datetime

import config

class user_comms(commands.Cog):

  def __init__(self, client):
    self.client = client



  #declare prefix
  client = commands.Bot(command_prefix = config.prefixList, case_insensitive=True, intents = discord.Intents().all())


  def check_setup(self, server_id):

    setup = False
    with open("./json/info.json", "r") as f:
        info = json.load(f)
        for i in info:
          if i['server_id'] == server_id:
            setup = True

    if not setup:
      embed = discord.Embed(
        title="Server is not setup yet!",
        color=config.yua_color,
        description="Please do `yua setup` first!",
      )
      embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
      return(False, embed)

    else:
      return(True, None)




  @commands.command()
  async def serverplaylist(self, ctx):
    
    with open("./json/info.json", "r") as f:
      info = json.load(f)

    # check setup
    issetup, embed = self.check_setup(ctx.guild.id)
    if not issetup:
      await ctx.send(embed=embed)
      return

    # is setup
    for i in info:
      if i['server_id'] == ctx.guild.id:

        _ = ''
        index = 1
        for song in i['songs']:
          dur = config.convert_seconds(song['dur'])
          _ += f"{index}. [{song['title']}]({song['url']}) {dur} \n "
          index += 1

    
    if _ == '':
      # no song in playlist
      embed = discord.Embed(
        title="There is no song in Server Playlist!",
        color=config.yua_color,
        description="start adding songs using `yua addsong`!",
        timestamp = datetime.utcnow()
      )
      embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
      embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
    else:
      # has song in playlist
      embed = discord.Embed(
        title=f"Playlist for {ctx.guild.name}",
        color=config.yua_color,
        description=_,
        timestamp = datetime.utcnow()
      )
      embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
      embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed)
    await ctx.message.add_reaction(self.client.get_emoji(918494275728179251))
      
        


  @commands.command()
  async def vc(self, ctx):

    # check setup
    issetup, embed = self.check_setup(ctx.guild.id)
    if not issetup:
      await ctx.send(embed=embed)
      return

    #find vc_id
    with open("./json/info.json", "r") as f:
      info = json.load(f)
    
    for i in info:
      if i['server_id'] == ctx.guild.id:
        embed = discord.Embed(
          title="Voice Channel",
          color=config.yua_color,
          timestamp=datetime.utcnow(),
          description=f"""
I'm currently playing music in <#{i['vc_id']}> in this server!
          """
        )
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        return



  @commands.command(aliases=['np'])
  async def nowplaying(self, ctx):

    issetup, embed = self.check_setup(ctx.guild.id)
    if not issetup:
      await ctx.send(embed=embed)
      return

    with open("./json/info_clone.json", 'r')  as f:
      info = json.load(f) 

    for server in info:
      if server['server_id'] == ctx.guild.id:
        songs = server['songs'] 
        break

    if server['songs'] == []:
      embed = discord.Embed(
        title="There is nothing playing!",
        color=config.yua_color,
        timestamp=datetime.utcnow(),
        description="Server Playlist is empty, there is nothing playing! \n do `yua addsong <url>` to add songs!"
      )
      embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
      embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
      await ctx.send(embed=embed)
      return
    
    # have song
    dur = config.convert_seconds(songs[0]['dur'])
    embed = discord.Embed(
      title="Currently Playing:",
      color = config.yua_color,
      timestamp = datetime.utcnow(),
      description = f"[{songs[0]['title']}]({songs[0]['url']}) {dur}"
    )
    embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
    embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url=songs[0]['thumbnail'])
    await ctx.send(embed=embed)





  @commands.command()
  async def skip(self, ctx):

    # check setup
    issetup, embed = self.check_setup(ctx.guild.id)
    if not issetup:
      await ctx.send(embed=embed)
      return
    
    vc = discord.utils.get(self.client.voice_clients, guild=self.client.get_guild(ctx.guild.id))
    if vc:
      vc.stop()
      await ctx.message.add_reaction(self.client.get_emoji(918494275728179251))
    else:
      embed = discord.Embed(
        title="I'm not playing any songs!",
        color=config.yua_color,
        timestamp=datetime.utcnow(),
        description=f"Please add songs to the serverplaylist by doing `yua addsong <url>`"
      )
      embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
      embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
      await ctx.send(embed=embed)





  @commands.command(aliases=['q'])
  async def queue(self, ctx):

    # check setup
    issetup, embed = self.check_setup(ctx.guild.id)
    if not issetup:
      await ctx.send(embed=embed)
      return

    vc = discord.utils.get(self.client.voice_clients, guild=self.client.get_guild(ctx.guild.id))
    if not vc:
      embed = discord.Embed(
        title="I'm not playing any songs!",
        color=config.yua_color,
        timestamp=datetime.utcnow(),
        description=f"Please add songs to the serverplaylist by doing `yua addsong <url>`"
      )
      embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
      embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
      await ctx.send(embed=embed)
      return

    info_clone = config.read_from_info_clone()
    _ = ''
    index = 1

    for server in info_clone:
      if server['server_id'] == ctx.guild.id:
        for song in server['songs']:
          dur = config.convert_seconds(song['dur'])
          if index == 1:
            _ += f"**Now Playing** \n [{song['title']}]({song['url']}) {dur} \n\n "
          else:
            _ += f"{index}. [{song['title']}]({song['url']}) {dur} \n "
          index += 1
    _ += "\n __Queue will be replenished once there's no songs!__"
    embed = discord.Embed(
      title=f"Server Queue for {ctx.guild}",
      color = config.yua_color,
      timestamp=datetime.utcnow(),
      description=_
    )
    embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
    embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)





def setup(client):
  client.add_cog(user_comms(client))