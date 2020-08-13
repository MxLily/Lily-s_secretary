import discord
import dotenv
import os
import sys

from discord.utils import get, find
from discord.ext import commands
from dotenv import load_dotenv

from fileFinder import FileFinder
from paramsGetter import getParams
from rolesHandler import hasRoles, addRoles, removeRoles

print("Start...")

bot = discord.Client()
bot = commands.Bot(command_prefix='&')
load_dotenv()
params = getParams()

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
    try:
        await addRoles(bot, member, params['onJoinRolesToAdd'])
    except KeyError as error:
        print(error)
    except Exception as error:
        print(error)

# TODO <=> ON MEMBER LEAVE / ban / kick  =>  Remove reaction on rules for member so that he reads them again if he rejoins
# TODO <=> Raise exceptions for better understanding (may be long)

@bot.event
async def on_raw_reaction_add(payload):
    message = payload.message_id
    member = payload.member
    emoji = payload.emoji
    try:
        if message == params['rulesMessageId'] and emoji.name == params['emojiNameToAcceptRules']:
            if await hasRoles(member, params['onAcceptRulesRolesToRemove']):
                await removeRoles(bot, member, params['onAcceptRulesRolesToRemove'])
                await addRoles(bot, member, params['onAcceptRulesRolesToAdd'])
    except KeyError as error:
        print(error)
    except Exception as error:
        print(error)

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

@bot.command()
async def reload(ctx):
    unloadCogs()
    loadCogs()
    await ctx.send("Reload completed.")

folderToFind = 'cogs'
fileExtension = '.py'
finder = FileFinder()
currentFolder = os.path.realpath(__file__)[:(len(__file__) * -1)]

sys.path.append(currentFolder)
files = finder.find(currentFolder + folderToFind, fileExtension)

def handleCogs(fct):
    for filename in files:
        toHandle = filename[len(currentFolder):(len(fileExtension) * -1)].replace('/', '.')
        fct(toHandle)

def loadCogs():
    handleCogs(bot.load_extension)

def unloadCogs():
    handleCogs(bot.unload_extension)

loadCogs()
jeton = os.getenv('DISCORD_TOKEN')
bot.run(jeton)