import discord
import os
import dotenv
from discord.utils import get
from discord.ext import commands
from dotenv import load_dotenv

from fileFinder import FileFinder

print("Start...")

bot = discord.Client()
bot = commands.Bot(command_prefix='&')
load_dotenv()

@bot.event
async def on_ready():
    print("Lily's Secretary :  ON")
    print("Version : 1.0.2")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Secrétaire Officiel De Lily"))

@bot.event
async def on_command_error(ctx, exception):
    await ctx.send(str(exception))

@bot.command()
@commands.is_owner()
async def logout(ctx):
    await ctx.send("Bot logged out.")
    await bot.logout()

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

fileExtension = '.py'
finder = FileFinder()
files = finder.find('cogs', fileExtension)

for filename in files:
    toLoad = filename[:(len(fileExtension) * -1)].replace('/', '.')
    bot.load_extension(toLoad)

jeton = os.getenv('DISCORD_TOKEN')
bot.run(jeton)