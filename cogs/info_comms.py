import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord import FFmpegPCMAudio
import os, random
from youtube_dl import YoutubeDL
import json
import asyncio
from discord_components import *

import config

class info_comms(commands.Cog):

  def __init__(self, client):
    self.client = client
    self.YDL_OPTIONS = {'format': 'bestaudio', 'yesplaylist':'False'}
    self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    self.sList = []
    self.nowplaying = ''

    self.yua_color = 16235890



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
        color=self.yua_color,
        description="Please do `yua setup` first!"
      )
      embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
      return(False, embed)

    else:
      return(True, None)







  @commands.command()
  @has_permissions(manage_guild=True)
  async def setup(self, ctx):

    with open("./json/info.json", 'r') as f:
      info = json.load(f)

    #check if server is already setup
    issetup, embed = self.check_setup(ctx.guild.id)
    if issetup:
      for i in info:
        if i['server_id'] == ctx.guild.id:
          server = i
        embed = discord.Embed(
          title="Sorry, your server is already setup",
          description=f"I'm currently playing in <#{server['vc_id']}>, come join me!",
          color=self.yua_color
        )
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)
        return
    

    #vc setup
    embed = discord.Embed(
      title="Setup voice channel",
      description="""
Please join the voice channel you want me to play music in, and click on the button.

__Timeout in 1 minute__
      """,
      color=self.yua_color
    )
    embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
    vc_setup_embed = await ctx.send(embed=embed, components=[Button(label="Select!", style=ButtonStyle.green, emoji = self.client.get_emoji(885845968048779304))])

    def check(interaction):
      return interaction.message == vc_setup_embed

    timeout = False
    while timeout is False:
      try:
        interaction = await self.client.wait_for("button_click", timeout = 60, check=check)

        if interaction:
          if interaction.author != ctx.author:
            await interaction.send("Only the one who invoked the command can select!")
            await interaction.defer(edit_origin=True)
          
          if interaction.author.voice:
            vc_id = ctx.author.voice.channel.id
            await vc_setup_embed.delete()
            timeout = True
          else:
            await interaction.send("Please connect to a voice channel before clicking it")

      except asyncio.TimeoutError:
        await ctx.send("iyamou-, you took too long! Please do `yua setup` again when you made up your mind.")
        await vc_setup_embed.delete()
        return


    #add a new dict for the server into info.json
    with open("./json/info.json", 'w') as f:

      server_dict = {
        "server_id": ctx.guild.id,
        "vc_id": vc_id,
        "songs": []
      }
      info.append(server_dict)
      json.dump(info, f, indent=2)

    
    #successful!
    embed = discord.Embed(
      title="Your server has been successfully setup!",
      color = self.yua_color,
      description=f"""
From now on I will be playing in <#{vc_id}>!

Please add songs to the server playlist with youtube links using the `addsong` command!
"""
    )
    embed.set_footer(text=self.client.user.name, icon_url=self.client.user.avatar_url)
    await ctx.send(embed=embed)
    await ctx.message.add_reaction(self.client.get_emoji(918494275728179251))
    




  @commands.command()
  @has_permissions(manage_guild=True)
  async def serverreset(self, ctx):

    is_setup, embed = self.check_setup(ctx.guild.id)
    if not is_setup:
      await ctx.send(embed=embed)
      return

    embed = discord.Embed(
      title="⚠️ARE YOU SURE⚠️",
      color=self.yua_color,
      description=f"""
This command will **REMOVE** your __Voice Channel__ and __Server Playlist__ data **FOREVER**!
Your action is inreversable.

You might want to:
> `yua changevc`
> `yua resetplaylist`

Write "CONFIRM" to confirm your change.
      """
    )
    await ctx.send(embed=embed)

    def check(m):
      return m.author == ctx.author and m.channel == ctx.channel and m.content == "CONFIRM"
    try:
      await self.client.wait_for("message", timeout=60, check=check)
    except asyncio.TimeoutError:
      embed = discord.Embed(
        title="Confirmation Timeout",
        color = self.yua_color,
        description="Back to safety! If you decide to reset, do `yua serverreset` again."
      )
      embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
      await ctx.send(embed=embed)
      return
    else:
      #with open

      embed = discord.Embed(
        title="Reset Successful",
        color=self.yua_color,
        description="Every server data has been reset! \n do `yua setup` to setup again!"
      )
      embed.set_footer(text=f"Reset requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
      await ctx.send(embed=embed)
      return
        



  @commands.command()
  @has_permissions(manage_guild=True)
  async def changevc(self, ctx):
    pass





  @commands.command()
  @has_permissions(manage_guild=True)
  async def addsong(self, ctx, url):

    with YoutubeDL(self.YDL_OPTIONS) as  ydl:
      try:
        video_data = ydl.extract_info(url, download=False)
      except:
        embed = discord.Embed(
          title="Failed to add song",
          color = self.yua_color,
          description=f"""
The link provide is invalid.
```{url}```
          
I can only accept YouTube links. Although other music bots accept Spotify links, they're still searching on YouTube due to limitation imposed by Spotify.
          """
        )
        await ctx.send(embed=embed)
        return
      
      #success
      with open("./json/info.json") as f:
         info = json.load(f)

         for i in info:
           setup = False

           if i["server_id"] == ctx.guild.id:
             setup = True
             i["songs"].append({"title": video_data['title'], "url": url})
             with open("./json/info.json", "w") as fw:
               json.dump(info, fw, indent=2)

      if not setup:
        embed = discord.Embed(
          title="Server is not setup yet!",
          color=self.yua_color,
          description="Please do `yua setup` first!"
        )
        embed.set_footer(text=self.client.user.name, icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)
        return

      embed = discord.Embed(
        title="Success!",
        color=self.yua_color,
        description="New banger music added to the server playlist, looking good!"
      )
      embed.add_field(name="TITLE", value=video_data['title'])
      embed.add_field(name="URL", value=url)
      embed.set_image(url=video_data['thumbnails'][-1]['url'])
      embed.set_footer(text=f"Song added by: {ctx.author}", icon_url=ctx.author.avatar_url)
      await ctx.send(embed=embed)
      await ctx.message.add_reaction(self.client.get_emoji(918494275728179251))
      


  @commands.command()
  async def remsong(self, ctx):
    pass



  @commands.command()
  async def serverplaylist(self, ctx):
    
    with open("./json/info.json", "r") as f:
      info = json.load(f)

    #get songs arranged
    setup = False
    for i in info:

      if i['server_id'] == ctx.guild.id:
        setup = True
        _ = ''

        index = 1
        for i in i['songs']:
          
          _ += f"{index}. [{i['title']}]({i['url']}) \n "
          index += 1
        
    #return if not setup
    if not setup:
      embed = discord.Embed(
        title="Server is not setup yet!",
        color=self.yua_color,
        description="Please do `yua setup` first!"
      )
      embed.set_footer(text=self.client.user.name, icon_url=self.client.user.avatar_url)
      await ctx.send(embed=embed)
      return

    #send playlist
    embed = discord.Embed(
      title=f"Playlist for {ctx.guild.name}",
      color=self.yua_color,
      description=_
    )
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
    await ctx.message.add_reaction(self.client.get_emoji(918494275728179251))
      
        



def setup(client):
  client.add_cog(info_comms(client))