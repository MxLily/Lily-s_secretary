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

async def addPermissions(destination: discord.PermissionOverwrite, overwrite: discord.PermissionOverwrite):
    for perm, value in overwrite:
        if getattr(destination, perm) is not True and (value is not None):
            setattr(destination, perm, value)

async def muteMember(member: discord.Member, guild: discord.Guild):
    roles = member.roles
    mutePermissions = await setMutedPermissions(discord.PermissionOverwrite())

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

                                await muteMember(member, guild)

                                # await ctx.send(embed=embed)
                                # TODO Verify if user is already muted and if so send a message to tell the author the target is already muted
                                # TODO Actually mute the user until endDate (i.e. mute now and unmute at the end of the punishment by making sure that shutting server won't break everything)

                                await ctx.send(embed=embed)
                                # # Send message to the punishments channel to have a record of the punishment
                                # if guild:
                                #     channel = find(lambda c: c.id == params['punishmentsChannelId'], guild.channels)
                                #     if channel:
                                #         await channel.send(embed=embed)
                                # # Send message to the user so that he knows why he got muted
                                # await member.send(embed=embed)
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
