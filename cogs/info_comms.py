import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord import FFmpegPCMAudio
import os, random
from youtube_dl import YoutubeDL
import json
import asyncio
from discord_components import *
from datetime import datetime

import config

class info_comms(commands.Cog):

  def __init__(self, client):
    self.client = client
    self.YDL_OPTIONS = {'format': 'bestaudio', 'yesplaylist':'False'}



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
  @has_permissions(manage_guild=True)
  async def setup(self, ctx):

    with open("./json/info.json", 'r') as f:
      info = json.load(f)

    # check if server is already setup
    issetup, embed = self.check_setup(ctx.guild.id)
    if issetup:
      for i in info:
        if i['server_id'] == ctx.guild.id:
          server = i
        embed = discord.Embed(
          title="Sorry, your server is already setup",
          description=f"I'm currently playing in <#{server['vc_id']}>, come join me!",
          color=config.yua_color
        )
        embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)
        return
    

    # vc setup
    embed = discord.Embed(
      title="Setup voice channel",
      description="""
Please join the voice channel you want me to play music in, and click on the button.

__Timeout in 1 minute__
      """,
      color=config.yua_color
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


    # add a new dict for the server into info.json
    with open("./json/info.json", 'w') as f:

      server_dict = {
        "server_id": ctx.guild.id,
        "vc_id": vc_id,
        "songs": []
      }
      info.append(server_dict)
      json.dump(info, f, indent=2)

    
    # successful!
    embed = discord.Embed(
      title="Your server has been successfully setup!",
      color = config.yua_color,
      timestamp = datetime.utcnow(),
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

    # check setup
    is_setup, embed = self.check_setup(ctx.guild.id)
    if not is_setup:
      await ctx.send(embed=embed)
      return

    # is setup
    embed = discord.Embed(
      title="⚠️ARE YOU SURE⚠️",
      color=config.yua_color,
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

    # awaiting confirmation
    def check(m):
      return m.author == ctx.author and m.channel == ctx.channel and m.content == "CONFIRM"
    try:
      await self.client.wait_for("message", timeout=60, check=check)
    except asyncio.TimeoutError:
      # timedout
      embed = discord.Embed(
        title="Confirmation Timeout",
        color = config.yua_color,
        description="Back to safety! If you decide to reset, do `yua serverreset` again.",
        timestamp = datetime.utcnow()
      )
      embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
      await ctx.send(embed=embed)
      return
    else:
      # confirmed
      with open("./json/info.json", 'r') as f:
        info = json.load(f)
        for i in range(0, len(info)):
          if info[i]['server_id'] == ctx.guild.id:
            info.pop(i)
      with open("./json/info.json", 'w') as f:
        json.dump(info, f, indent=2)
      embed = discord.Embed(
        title="Reset Successful",
        color=config.yua_color,
        description="Every server data has been reset! \n do `yua setup` to setup again!",
        timestamp = datetime.utcnow()
      )
      embed.set_footer(text=f"Reset requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
      await ctx.send(embed=embed)
      return
        




  @commands.command()
  async def clearplaylist(self, ctx):

    # check setup
    is_setup, embed = self.check_setup(ctx.guild.id)
    if not is_setup:
      await ctx.send(embed=embed)
      return

    # if server playlist is empty
    with open("./json/info.json", 'r') as f:
      info = json.load(f)
    
    for i in info:
      if i['server_id'] == ctx.guild.id:
        if i['songs'] == []:
          embed = discord.Embed(
            title="There is nothing to clear!",
            color=config.yua_color,
            timestamp=datetime.utcnow(),
            description="Server Playlist is empty, there is nothing for me to clear! \n do `yua addsong <url>` to add songs!"
          )
          embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
          embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
          await ctx.send(embed=embed)
          return

    # is setup
    embed = discord.Embed(
      title="⚠️ARE YOU SURE⚠️",
      color=config.yua_color,
      description=f"""
This command will **CLEAR** __every song in the server playlist__ **FOREVER**!
Your action is inreversable.

Write "CONFIRM" to confirm your change.
      """
    )
    await ctx.send(embed=embed)

    # awaiting confirmation
    def check(m):
      return m.author == ctx.author and m.channel == ctx.channel and m.content == "CONFIRM"
    try:
      await self.client.wait_for("message", timeout=60, check=check)
    except asyncio.TimeoutError:
      # timedout
      embed = discord.Embed(
        title="Confirmation Timeout",
        color = config.yua_color,
        description="Back to safety! If you decide to clear, do `yua clearplaylist` again.",
        timestamp = datetime.utcnow()
      )
      embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
      await ctx.send(embed=embed)
      return
    else:
      # confirmed
      for i in info:
        if i['server_id'] == ctx.guild.id:
          i['songs'] = []

      with open("./json/info.json", 'w') as f:
        json.dump(info, f, indent=2)

      embed = discord.Embed(
        title="Cleared Successfully",
        color=config.yua_color,
        description="Server Playlist has been cleared \n do `yua addsong <url>` to add new songs!",
        timestamp = datetime.utcnow()
      )
      embed.set_footer(text=f"Cleared by: {ctx.author}", icon_url=ctx.author.avatar_url)
      await ctx.send(embed=embed)
      return


  @commands.command()
  @has_permissions(manage_guild=True)
  async def changevc(self, ctx):

    # check setup
    is_setup, embed = self.check_setup(ctx.guild.id)
    if not is_setup:
      await ctx.send(embed=embed)
      return

    with open("./json/info.json", 'r') as f:
      info = json.load(f)
    
    for i in info:
      if i['server_id'] == ctx.guild.id:

        # vc setup
        embed = discord.Embed(
          title="Resetup voice channel",
          description=f"""
Please join the voice channel you want me to play music in, and click on the button.
Previous channel: <#{i['vc_id']}>

__Timeout in 1 minute__
          """,
          color=config.yua_color
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
            await ctx.send("iyamou-, you took too long! Please do `yua changevc` again when you made up your mind.")
            await vc_setup_embed.delete()
            return
        
        #success
        i['vc_id'] = vc_id
        with open("./json/info.json", 'w') as f:
          json.dump(info, f, indent=2)

        embed = discord.Embed(
          title="Voice Channel Changed Successfully!",
          color = config.yua_color,
          timestamp = datetime.utcnow(),
          description=f"""
    From now on I will be playing in <#{vc_id}>!

    Please add songs to the server playlist with youtube links using the `addsong` command!
    """
        )
        embed.set_footer(text=self.client.user.name, icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)
        await ctx.message.add_reaction(self.client.get_emoji(918494275728179251))











  @commands.command()
  async def remsong(self, ctx, index=None):

    with open("./json/info.json", "r") as f:
      info = json.load(f)

    # check setup
    issetup, embed = self.check_setup(ctx.guild.id)
    if not issetup:
      await ctx.send(embed=embed)
      return

    # if index is not entered
    if index is None:
      await ctx.send("An index is required!")
      return

    # check validity of index arg
    try:
      index = int(index)
    except:
      embed = discord.Embed(
        title="Invalid Index",
        color=config.yua_color,
        timestamp=datetime.utcnow(),
        description=f"""
Please input an integer!

tip: Get the song's number from `yua serverplaylist`
        """
      )
      embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
      embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
      await ctx.send(embed=embed)
      return

    # remove song
    for i in info:
      if i['server_id'] == ctx.guild.id:
        
        if i['songs'] == []:
          # no song in playlist
          embed = discord.Embed(
            title="There is no song in Server Playlist!",
            color=config.yua_color,
            description="start adding songs using `yua addsong`!",
            timestamp = datetime.utcnow()
          )
          embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
          embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
          await ctx.send(embed=embed)
          return

        if index not in range(1, len(i['songs'])+1):
          # index out of range
          embed = discord.Embed(
            title="Invalid Index",
            color=config.yua_color,
            timestamp=datetime.utcnow(),
            description=f"""
There is no song with the number `{index}`!

tip: Get the song's number from `yua serverplaylist`
            """
          )
          embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
          embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
          await ctx.send(embed=embed)
          return
        
        else:
          # valid index
          # confirmation
          index -= 1  # to list index

          embed = discord.Embed(
            title="Are you sure you want to remove the following song?",
            color=config.yua_color,
            timestamp=datetime.utcnow()
          )
          embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
          embed.add_field(name="TITLE", value=i['songs'][index]['title'])
          embed.add_field(name="URL", value=i['songs'][index]['url'])
          embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
          #thumbnail
          with YoutubeDL(self.YDL_OPTIONS) as  ydl:
            try:
              video_data = ydl.extract_info(i['songs'][index]['url'], download=False)
              embed.set_image(url=video_data['thumbnails'][-1]['url'])
            except:
              # if the vid is taken down
              break

          confirmation_embed = await ctx.send(embed=embed, components=[Button(label="Confirm!", style=ButtonStyle.green, emoji = self.client.get_emoji(885845962659074088))])

          def check(interaction):
            return interaction.message == confirmation_embed
          while True:
            try:
              interaction = await self.client.wait_for("button_click", check=check, timeout=60)

              if interaction.author != ctx.author:
                await interaction.send("Only the one who invoked the command can confirm!")

              if interaction.author == ctx.author:
                # confirmed
                await interaction.defer(edit_origin=True)
                i['songs'].pop(index)
                with open("./json/info.json", "w") as _:
                  json.dump(info, _, indent=2)

                embed = discord.Embed(
                  title="Removed Song Successfully",
                  color=config.yua_color,
                  timestamp=datetime.utcnow(),
                  description=f""""""
                )
                embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            except asyncio.TimeoutError:
              embed = discord.Embed(
                title="Timeout",
                color=config.yua_color,
                timestamp=datetime.utcnow(),
                description=f"You took too long! Do `yua remsong <index>` again when you're ready."
              )
              embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
              embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
              await ctx.send(embed=embed)
              return



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
        for i in i['songs']:
          _ += f"{index}. [{i['title']}]({i['url']}) \n "
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



def setup(client):
  client.add_cog(info_comms(client))