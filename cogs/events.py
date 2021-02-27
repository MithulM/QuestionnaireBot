import discord
from discord.ext import commands


class Refresh(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_read(self):
        print("Bot is online!")

def setup(client):
    client.add_cog(Refresh(client))
