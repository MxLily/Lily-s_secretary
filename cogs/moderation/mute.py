import discord
from discord.ext import commands
from discord.utils import find, get
import asyncio

from paramsGetter import getParams, getGuildId
from rolesHandler import hasAtLeastOneRole
from timeParser import TimeParser

async def setMutedPermissions(permissions):
    permissions.send_messages = False
    permissions.send_tts_messages = False
    permissions.add_reactions = False

async def createMuteRole(guild: discord.Guild, roleToCopyPermissionsFrom: discord.Role, muteRoleName: str):
    muteRole = get(guild.roles, name=muteRoleName)

    if not muteRole:
        await guild.create_role(name=muteRoleName)
        muteRole = get(guild.roles, name=muteRoleName)

    for channel in guild.text_channels:
        await asyncio.sleep(0)

        mutePermissions = discord.PermissionOverwrite()
        await setMutedPermissions(mutePermissions)

        if roleToCopyPermissionsFrom:
            overwrites = channel.overwrites_for(roleToCopyPermissionsFrom)
            if overwrites.is_empty():
                await channel.set_permissions(muteRole, overwrite=mutePermissions)
            else:
                await setMutedPermissions(overwrites)
                await channel.set_permissions(muteRole, overwrite=overwrites)

    return muteRole

class Mute(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.timeParser = TimeParser()

    @commands.command()
    async def mute(self, ctx, member: discord.Member, *args):
        try:
            author = ctx.author
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
                            if True:
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

                                guild = ctx.message.guild
                                roleToRemoveAndCopyPermissionsFrom = get(guild.roles, name=params['roleNameToRemoveAndCopyPermissionsFromToMute'])
                                muteRole = await createMuteRole(guild, roleToRemoveAndCopyPermissionsFrom, params['muteRoleName'])

                                # Mute user by removing a role and replacing it by a muted version of this role
                                await member.remove_roles(roleToRemoveAndCopyPermissionsFrom)
                                await member.add_roles(muteRole)

                                # await ctx.send(embed=embed)
                                # TODO Verify if user is already muted and if so send a message to tell the author the target is already muted
                                # TODO Actually mute the user until endDate (i.e. mute now and unmute at the end of the punishment by making sure that shutting server won't break everything)

                                # Send message to the punishments channel to have a record of the punishment
                                guildId = await getGuildId()
                                guild = find(lambda g: g.id == guildId, self.bot.guilds)
                                if guild:
                                    channel = find(lambda c: c.id == params['punishmentsChannelId'], guild.channels)
                                    if channel:
                                        await channel.send(embed=embed)
                                # Send message to the user so that he knows why he got muted
                                await member.send(embed=embed)
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
