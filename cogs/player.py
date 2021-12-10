import discord
from discord.ext import commands
import os, random
import json
from youtube_dl import YoutubeDL

import config

class player(commands.Cog):

  def __init__(self, client):
    self.client = client
    self.YDL_OPTIONS = {'format': 'bestaudio', 'yesplaylist':'True'}
    self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}



  @commands.Cog.listener()
  async def on_ready(self):

    with open("./json/info.json", 'r') as f:
      info = json.load(f)
    
    with open("./json/info.json", 'w') as f:
      json.dump(info, f, indent=2)

    for i in info:
      voice_client = discord.utils.get(self.client.voice_clients, guild=self.client.get_guild(i['server_id']))
      if voice_client is not None:
        voice_client.disconnect()

      if i['songs'] != []:
        channel = self.client.get_channel(i['vc_id'])
        await channel.connect()
        await self.startplaying(i['server_id'])



  async def startplaying(self, server_id):

    # get server songs
    with open("./json/info.json", 'r') as f:
      info = json.load(f)

    for i in info:
      if i['server_id'] == server_id:
        server = i
        break

    # download all the songs
    songs = []
    for songs in server['songs']:
      with YoutubeDL(self.YDL_OPTIONS) as ydl:
        try:
          video_data = ydl.extract_info(url, download=False)
          _ = {
            "title": video_data['title'],
            "duration"
          }
        





  client = commands.Bot(command_prefix = config.prefixList, case_insensitive=True, intents = discord.Intents().all())







def setup(client):
  client.add_cog(player(client))