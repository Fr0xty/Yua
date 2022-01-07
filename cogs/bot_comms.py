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
    client.remove_command('help')                                 #remove default built-in help command
    





    @commands.command()
    async def rename(self, ctx, name):
        if ctx.author.id == 395587171601350676:
            await self.client.user.edit(username=name)



    @commands.command()
    async def help(self, ctx):

        helpEmbed = config.helpEmbed(self.client, ctx.author)
        current=0
        msg = await ctx.send(embed=helpEmbed[current],
        components=[
            [Button(style=ButtonStyle.gray, label="🢀"),
            Button(style=ButtonStyle.gray, label="🢂")]
        ])
        def check(interaction):
            return interaction.message.id == msg.id
        while True:
            try:
                interaction = await self.client.wait_for("button_click", timeout=300, check=check)
                
                if interaction.component.label == "🢀":
                    if current > 0:
                        current -= 1
                        await msg.edit(embed=helpEmbed[current])
                        await interaction.defer(edit_origin=True)
                    else:
                        await interaction.defer(edit_origin=True)

                if interaction.component.label == "🢂":
                    if current < 1:
                        current += 1
                        await msg.edit(embed=helpEmbed[current])
                        await interaction.defer(edit_origin=True)
                    else:
                        await interaction.defer(edit_origin=True)
            
            except asyncio.TimeoutError:
                await msg.delete()
                return




def setup(client):
    client.add_cog(command(client))