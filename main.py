import discord
import dotenv
import json
import os

from discord.utils import get, find
from discord.ext import commands
from dotenv import load_dotenv

from fileFinder import FileFinder

print("Start...")

bot = discord.Client()
bot = commands.Bot(command_prefix='&')
load_dotenv()

GUILD = int(os.getenv('DISCORD_GUILD_ID', '0'))

params = {}
with open('params.json', 'r', encoding='utf-8') as f:
    params = json.load(f)

@bot.event
async def on_ready():
    print("Lily's Secretary :  ON")
    print("Version : 1.0.3")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Secrétaire Officiel De la MxCommunity"))

@bot.event
async def on_command_error(ctx, exception):
    await ctx.send(str(exception))

async def handleRoles(roles, fct):
    guild = find(lambda g: g.id == GUILD, bot.guilds)
    if guild:
        if isinstance(roles, str):
            role = get(guild.roles, name=roles)
            if role:
                await fct(role)
        elif isinstance(roles, list):
            rolesToSend = []
            for it in roles:
                role = get(guild.roles, name=it)
                if role:
                    rolesToSend.append(role)
            await fct(*rolesToSend)

async def addRoles(member, roles):
    await handleRoles(roles, member.add_roles)

async def removeRoles(member, roles):
    await handleRoles(roles, member.remove_roles)

async def hasRoles(member, roles):
    if isinstance(roles, str):
        return get(member.roles, name=roles)
    elif isinstance(roles, list):
        containsAll = True
        for role in roles:
            if isinstance(role, str) and not get(member.roles, name=role):
                containsAll = None
                break
        return containsAll
    return None

@bot.event
async def on_member_join(member):
    try:
        await addRoles(member, params['onJoinRolesToAdd'])
    except KeyError as error:
        print(error)
    except Exception as error:
        print(error)

# TODO <=> ON MEMBER LEAVE  =>  Remove reaction on rules for member so that he reads them again if he rejoins

@bot.event
async def on_raw_reaction_add(payload):
    message = payload.message_id
    member = payload.member
    emoji = payload.emoji
    try:
        if message == params['rulesMessageId'] and emoji.name == params['emojiNameToAcceptRules']:
            if await hasRoles(member, params['onAcceptRulesRolesToRemove']):
                await removeRoles(member, params['onAcceptRulesRolesToRemove'])
                await addRoles(member, params['onAcceptRulesRolesToAdd'])
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