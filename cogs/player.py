import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import os, random
import json
from youtube_dl import YoutubeDL
import asyncio
from datetime import datetime
import copy

import config

class player(commands.Cog):

  def __init__(self, client):
    self.client = client
    self.YDL_OPTIONS = {'format': 'bestaudio', 'yesplaylist':'False'}
    self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}







  @commands.Cog.listener()
  async def on_ready(self):

    # get info.json
    info = config.read_from_info()

    # clone info into info_clone.json
    with open("./json/info_clone.json", 'w') as f:
      json.dump(info, f, indent=2)

    for i in info:
      # leave already connect channels to avoid error
      voice_client = discord.utils.get(self.client.voice_clients, guild=self.client.get_guild(i['server_id']))
      if voice_client is not None:
        voice_client.disconnect()

      # join vc_id if the server playlist has songs
      if i['songs'] != []:
        channel = await self.client.fetch_channel(i['vc_id'])
        await channel.connect()
        # pass to start()
        await self.start(i['server_id'])




  async def first_time_start(self, server_id):
    info = config.read_from_info()
    info_clone = config.read_from_info_clone()

    for server in info:
      if server['server_id'] == server_id:
        the_server = server
        break

    for server in info_clone:
      if server['server_id'] == server_id:
        server['songs'] = the_server['songs']
        break
        
    with open("./json/info_clone.json", 'w') as f:
      json.dump(info_clone, f, indent=2)
    
    ch = await self.client.fetch_channel(the_server['vc_id'])
    await ch.connect()
    await self.start(server_id)

    

  async def start(self, server_id):

    # get server songs
    clone_info = config.read_from_info_clone()

    # get the server dict and reference server to it
    for i in clone_info:
      if i['server_id'] == server_id:
        the_server = i

    # shuffle server['songs'] list and play first song
    random.shuffle(the_server['songs'])
    with open("./json/info_clone.json", 'w') as f:
      json.dump(clone_info, f, indent=2)

    with YoutubeDL(self.YDL_OPTIONS) as ydl:
      success = False
      while success is False:
        try:
          video_data = ydl.extract_info(the_server['songs'][0]['url'], download=False)
          # store thumbnail for current song in info_clone.json / for "np" command
          the_server['songs'][0].update({"thumbnail": video_data['thumbnail']})
          with open("./json/info_clone.json", 'w') as f:
            json.dump(clone_info, f, indent=2)
          success = True
        except:
          # failed (yt vid taken down)
          # dm server owner of the change

          embed = discord.Embed(
            title="Song removed from your Server's Playlist!",
            description=f"This is happening because the video is either taken down from YouTube or the publisher privated the video.",
            color=config.yuna_color,
            timestamp=datetime.utcnow()
          )
          embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
          embed.add_field(name="TITLE", value=the_server['songs'][0]['title'])
          embed.add_field(name="URL", value=the_server['songs'][0]['url'])
          guild = await self.client.fetch_guild(the_server['server_id'])
          await guild.owner.send(embed=embed)

          # remove the song from info.json
          the_server['songs'].pop(0)

          info = config.read_from_info()
          for server in info:
            if server['server_id'] == server_id:
              # find song
              for song in server:
                if song['url'] == the_server['songs'][0]:
                  server['songs'].remove(song)
                  break

          with open("./json/info.json", 'w') as f:
            json.dump(info, f, indent=2)
        
      # after ytdl success
      vc = discord.utils.get(self.client.voice_clients, guild=self.client.get_guild(the_server['server_id']))
      vc.play(discord.FFmpegPCMAudio(video_data['url'], **self.FFMPEG_OPTIONS), after = lambda e: asyncio.run_coroutine_threadsafe(self.player(the_server['server_id']), self.client.loop))





  async def player(self, server_id):
    clone_info = config.read_from_info_clone()
    
    # find server
    for server in clone_info:
      if server['server_id'] == server_id:

        server['songs'].pop(0)
        with open("./json/info_clone.json", 'w') as f:
          json.dump(clone_info, f, indent=2)
          
        # if no more songs
        if server['songs'] == []:
          #replenish info_clone.json
          server_songs = config.get_server_songs(server_id)
          config.replenish_song_in_info_clone(server_id, server_songs)
        
        clone_info = clone_info = config.read_from_info_clone()

        for server in clone_info:
          if server['server_id'] == server_id:
            the_server = server

        with YoutubeDL(self.YDL_OPTIONS) as ydl:
          success = False
          while success is False:
            try:
              video_data = ydl.extract_info(the_server['songs'][0]['url'], download=False)
              # store thumbnail for current song in info_clone.json / for "np" command
              the_server['songs'][0].update({"thumbnail": video_data['thumbnail']})
              with open("./json/info_clone.json", 'w') as f:
                json.dump(clone_info, f, indent=2)
              success = True
            except:
              # failed (yt vid taken down)
              # dm server owner of the change

              embed = discord.Embed(
                title="Song removed from your Server's Playlist!",
                description=f"This is happening because the video is either taken down from YouTube or the publisher privated the video.",
                color=config.yuna_color,
                timestamp=datetime.utcnow()
              )
              embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
              embed.add_field(name="TITLE", value=the_server['songs'][0]['title'])
              embed.add_field(name="URL", value=the_server['songs'][0]['url'])
              guild = await self.client.fetch_guild(the_server['server_id'])
              await guild.owner.send(embed=embed)

              # remove the song from info.json
              the_server['songs'].pop(0)

              info = config.read_from_info()
              for server in info:
                if server['server_id'] == server_id:
                  # find song
                  for song in server:
                    if song['url'] == the_server['songs'][0]:
                      server['songs'].remove(song)
                      break

              with open("./json/info.json", 'w') as f:
                json.dump(info, f, indent=2)
            
          # after ytdl success
          vc = discord.utils.get(self.client.voice_clients, guild=self.client.get_guild(the_server['server_id']))
          vc.play(discord.FFmpegPCMAudio(video_data['url'], **self.FFMPEG_OPTIONS), after = lambda e: asyncio.run_coroutine_threadsafe(self.player(the_server['server_id']), self.client.loop))

    





  client = commands.Bot(command_prefix = config.prefixList, case_insensitive=True, intents = discord.Intents().all())






def setup(client):
  client.add_cog(player(client))