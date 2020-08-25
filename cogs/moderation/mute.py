import discord
from discord.ext import commands
from discord.utils import find, get
import asyncio
from datetime import datetime
from os.path import exists, isfile

from paramsGetter import getParams, getGuildId
from rolesHandler import hasAtLeastOneRole
from timeParser import TimeParser
from cogs.moderation.unmute import unmuteMember

async def setMutedPermissions(permissions):
    permissions.send_messages = False
    permissions.send_tts_messages = False
    permissions.add_reactions = False

async def addPermissions(destination: discord.PermissionOverwrite, overwrite: discord.PermissionOverwrite):
    for perm, value in overwrite:
        if getattr(destination, perm) is not True and (value is not None):
            setattr(destination, perm, value)

async def muteMember(member: discord.Member, guild: discord.Guild, endDate: datetime, params):
    roles = member.roles
    mutePermissions = await setMutedPermissions(discord.PermissionOverwrite())

    # MemberId;GuildId;EndDate;MemberRolesId;ActualEndDate
    saveLine = ';'.join((str(member.id), str(guild.id), str(endDate) if endDate else '', ','.join(str(role.id) for role in roles), '')) + '\n'
    if 'savePunishments' in params and 'mute' in params['savePunishments']:
        saveFile = params['savePunishments']['mute']
        with open(saveFile, 'a+') as f:
            f.write(saveLine)

    for channel in guild.text_channels:
        await asyncio.sleep(0)

        # Resulting overwrite
        newOverwrite = discord.PermissionOverwrite()

        # Gather all permissions and restrictions
        memberOverwrite = channel.overwrites_for(member)
        channelOverwrites = []
        for role in roles:
            channelOverwrites.append(channel.overwrites_for(role))

        # Add all permissions and restrictions to the resulting overwrite
        for channelOverwrite in channelOverwrites:
            await addPermissions(newOverwrite, channelOverwrite)
        await addPermissions(newOverwrite, memberOverwrite)

        # Set restrictions so that user is being muted
        await setMutedPermissions(newOverwrite)
        await channel.set_permissions(member, overwrite=newOverwrite)

    await member.edit(roles=[])

    if endDate:
        delta = (endDate - datetime.now()).total_seconds()
        await asyncio.sleep(delta)
        await unmuteMember(member, guild, params)

async def alreadyMuted(member: discord.Member, guild: discord.Guild, params):
    saveFile = params['savePunishments']['mute']
    if not exists(saveFile) or not isfile(saveFile):
        return False
    index = -1
    with open(saveFile, 'r') as f:
        lines = f.readlines()
        i = 0
        for line in lines:
            elements = line.rstrip().split(';')
            memberId = int(elements[0])
            guildId = int(elements[1])
            actualEndDate = elements[4]
            if memberId == member.id and guildId == guild.id and not actualEndDate:
                index = i
            i += 1
    if index >= 0:
        return True
    return False

class Mute(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.timeParser = TimeParser()

    @commands.command()
    async def mute(self, ctx, member: discord.Member, *args):
        try:
            author = ctx.author
            guild = ctx.message.guild
            # Check if author is a user (i.e. not a bot)
            if not author.bot:
                params = getParams()
                roles = params['rolesThatCanMute']
                # Check if author has permissions to perform this command
                if await hasAtLeastOneRole(author, roles):
                    # Check if the target is a user (i.e. not a bot)
                    if not member.bot:
                        rolesToAvoid = params['rolesThatCannotBeMuted']
                        # Check if the target can receive this command
                        if not await hasAtLeastOneRole(member, rolesToAvoid):
                            # Check if target is already being muted
                            if not await alreadyMuted(member, guild, params):
                                embed = discord.Embed(
                                    colour = discord.Colour.purple()
                                )
                                embed.set_author(name=self.bot.user.display_name + ' • Mute', icon_url=params['punishmentsAuthorImageUrl'])
                                # embed.set_thumbnail(url='https://mxcommunity.xyz/src/MxCommunity_tr.png')
                                embed.add_field(name='Membre mute', value=member, inline=False)
                                embed.add_field(name='Mute par', value=author, inline=False)

                                endDate = None
                                endMessage = 'Indéfini'
                                if args:
                                    endDate, index = self.timeParser.endDate(args)
                                    if endDate:
                                        endMessage = '{} {} {} à {}'.format(endDate.day, self.timeParser.getMonthName(endDate.month), endDate.year, endDate.strftime("%H:%M:%S"))
                                    embed.add_field(name='Fin de la sanction', value=endMessage, inline=False)

                                    reasons = args[index:]
                                    if reasons:
                                        reasonMsg = reasonMsg = ' '.join(reasons) if reasons else ''
                                        embed.add_field(name='Raison', value=reasonMsg, inline=False)
                                else:
                                    embed.add_field(name='Fin de la sanction', value=endMessage, inline=False)

                                # await ctx.send(embed=embed)
                                # TODO Verify if user is already muted and if so send a message to tell the author the target is already muted
                                # TODO Actually mute the user until endDate (i.e. mute now and unmute at the end of the punishment by making sure that shutting server won't break everything)

                                # Send message to the punishments channel to have a record of the punishment
                                if guild:
                                    channel = find(lambda c: c.id == params['punishmentsChannelId'], guild.channels)
                                    if channel:
                                        await channel.send(embed=embed)
                                # Send message to the user so that he knows why he got muted
                                await member.send(embed=embed)

                                # Actually mute the member
                                await muteMember(member, guild, endDate, params)
                            else:
                                await ctx.send("Cet utilisateur est déjà mute. Vous ne pouvez donc pas effectuer cette commande.")
                        else:
                            await ctx.send("Vous ne pouvez pas mute cet utilisateur à cause des rôles qui lui sont attribués.")
                    else:
                        await ctx.send("Vous ne pouvez pas mute un bot. Veuillez réessayer avec un utilisateur valide.")
                else:
                    await ctx.send("Vous n'avez pas les permissions pour effectuer cette commande. Si vous pensez que c'est une erreur, veuillez contacter un administrateur.")
            else:
                await ctx.send("Cette commande ne peut être effectuée par un bot.")
        except KeyError as error:
            print(error)
        except Exception as error:
            print(error)


def setup(bot):
    bot.add_cog(Mute(bot))
