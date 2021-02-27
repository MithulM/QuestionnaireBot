import os
import discord
from discord.ext import commands

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = '!', intents = intents)

@client.event
async def on_ready():
    print("Bot ready")

for extension in os.listdir('./cogs'):
    if extension.endswith('.py'):
        client.load_extension(f'cogs.{extension[:-3]}')
        print(f"{extension[:-3]} cog loaded")

@client.command()
async def reload(ctx, ext="all"):
    if ext == "all":
        for exts in os.listdir('./cogs'):
            if exts.endswith('.py'):
                client.unload_extension(f'cogs.{exts[:-3]}')
        for exts in os.listdir('./cogs'):
            if exts.endswith('.py'):
                client.load_extension(f'cogs.{exts[:-3]}')
        await ctx.send(f'Reloaded all cogs')
    else:
        client.unload_extension(f'cogs.{ext}')
        client.load_extension(f'cogs.{ext}')
        await ctx.send(f'Reloaded {ext}')

@client.command()
async def ping(ctx):
    await ctx.send(f"Pong {client.latency}")

@client.command()
async def load(ctx, ext):
    client.load_extension(f'cogs.{ext}')
    await ctx.send(f'Reloaded {ext}')

@load.error
async def load_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify a cog to load.')


tokenFile = open("token.txt", "r")
client.run(tokenFile.read())
tokenFile.close()