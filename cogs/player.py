import discord
from discord.ext import commands
import os, random
import json

import config

class player(commands.Cog):

  def __init__(self, client):
    self.client = client
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
    return






  client = commands.Bot(command_prefix = config.prefixList, case_insensitive=True, intents = discord.Intents().all())







def setup(client):
  client.add_cog(player(client))