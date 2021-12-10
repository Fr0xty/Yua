import discord
from discord.ext import commands
import os, random

import config

class nonstop_music(commands.Cog):

  def __init__(self, client):
    self.client = client
    self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}








  client = commands.Bot(command_prefix = config.prefixList, case_insensitive=True, intents = discord.Intents().all())







def setup(client):
  client.add_cog(nonstop_music(client))