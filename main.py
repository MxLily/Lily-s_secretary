# Importation
import discord
import os
import dotenv
from discord.utils import get
from discord.ext import commands
from dotenv import load_dotenv

# Start Message
print("Start...")

# Creation BOT
bot = discord.Client()

# Creation préfix
bot = commands.Bot(command_prefix='&')

load_dotenv()

# Bot On
@bot.event
async def on_ready():
    print("Lily's Secretary :  ON")
    print("Version : 1.0.1")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Secrétaire Officiel De Lily"))

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

# Installation du token de connection
jeton = os.getenv('DISCORD_TOKEN')

# Connection au serveur
bot.run(jeton)