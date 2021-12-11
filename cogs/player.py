import discord
from discord.ext import commands
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
    self.YDL_OPTIONS = {'format': 'bestaudio', 'yesplaylist':'True'}
    self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}




  def read_info_json(self):
    with open("./json/info.json", 'r') as f:
      info = json.load(f)
      return info

  def read_info_clone_json(self):
    with open("./json/info_clone.json", 'r') as f:
      info = json.load(f)
      return info





  @commands.Cog.listener()
  async def on_ready(self):

    # get info.json
    info = self.read_info_json()

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




  async def start(self, server_id):

    # get server songs
    info = self.read_info_clone_json()

    # get the server dict and store into "server"
    for i in info:
      if i['server_id'] == server_id:
        server = copy.copy(i)

    ch = await self.client.fetch_channel(873844031048785960)

    # shuffle server['songs'] list and play first song
    random.shuffle(server['songs'])

    with YoutubeDL(self.YDL_OPTIONS) as ydl:
      success = False
      while success is False:
        try:
          video_data = ydl.extract_info(server['songs'][0]['url'], download=False)
          success = True
        except:
          #failed (yt vid taken down)
          #remove the song from info.json
          info = self.read_info_json()
          for i in info:
            if i['server_id'] == server_id:
              for song in i['songs']:
                if song['url'] == server['songs'][0]:

                  # dm owner of the server of the change
                  embed = discord.Embed(
                    title="Song removed from your Server's Playlist!",
                    description=f"This is happening because the video is either taken down from YouTube or the publisher privated the video.",
                    color=config.yua_color,
                    timestamp=datetime.utcnow()
                  )
                  embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
                  embed.add_field(name="TITLE", value=song['title'])
                  embed.add_field(name="URL", value=song['url'])
                  guild = await self.client.fetch_guild(server['server_id'])
                  await guild.owner.send(embed=embed)
                  
                  i['songs'].remove(song)

              with open("./json/info.json", 'w') as f:
                json.dump(info, f, indent=2)
            
          

          #pop the failed song out / update info_clone.json
          server['songs'].pop(0)
          info = self.read_info_json()
          with open("./json/info_clone.json", 'w') as f:
            json.dump(info, f, indent=2)
        
      #after ytdl success
      vc = discord.utils.get(self.client.voice_clients, guild=self.client.get_guild(server['server_id']))
      vc.play(discord.FFmpegPCMAudio(video_data['url'], **self.FFMPEG_OPTIONS), after = lambda e: asyncio.run_coroutine_threadsafe(self.player(server['server_id'])))


  async def player(self, server_id):
    return





  client = commands.Bot(command_prefix = config.prefixList, case_insensitive=True, intents = discord.Intents().all())







def setup(client):
  client.add_cog(player(client))