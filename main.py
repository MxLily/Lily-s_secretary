import discord
import os
import dotenv
from discord.utils import get, find
from discord.ext import commands
from dotenv import load_dotenv

from fileFinder import FileFinder

print("Start...")

bot = discord.Client()
bot = commands.Bot(command_prefix='!')
load_dotenv()

GUILD = os.getenv('DISCORD_GUILD_ID')
if GUILD:
    GUILD = int(GUILD)



@bot.event
async def on_ready():
    print("Lily's Secretary :  ON")
    print("Version : 1.0.3")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Secrétaire Officiel De la MxCommunity"))

@bot.event
async def on_command_error(ctx, exception):
    await ctx.send(str(exception))

@bot.event
async def on_member_join(member):
    guild = find(lambda g: g.id == GUILD, bot.guilds)
    if guild:
        role = get(guild.roles, name=">> Invité <<")
        if role:
            await member.add_roles(role)

@bot.event
async def on_raw_reaction_add(payload):
    message = payload.message_id
    member = payload.member
    emoji = payload.emoji
    if message == 742853196841615421 and emoji.name == "valide":
        currentRole = get(member.roles, name=">> Invité <<")
        if currentRole:
            guild = find(lambda g: g.id == GUILD, bot.guilds)
            if guild:
                roleToAdd = get(guild.roles, name=">> Membre <<")
                if roleToAdd:
                    await member.add_roles(roleToAdd)
                roleToRemove = get(guild.roles, name=">> Invité <<")
                if roleToRemove:
                    await member.remove_roles(roleToRemove)

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

currentFolder = os.path.realpath(__file__)[:(len(__file__) * -1)]
folderToFind = 'cogs'
fileExtension = '.py'

finder = FileFinder()
files = finder.find(currentFolder + folderToFind, fileExtension)


for filename in files:
    toLoad = filename[len(currentFolder):(len(fileExtension) * -1)].replace('/', '.')
    bot.load_extension(toLoad)

jeton = os.getenv('DISCORD_TOKEN')
bot.run(jeton)