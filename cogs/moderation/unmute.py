import discord
from discord.ext import commands
from discord.utils import find, get
import asyncio

from paramsGetter import getParams, getGuildId
from rolesHandler import hasAtLeastOneRole
from timeParser import TimeParser

async def unmuteMember(member: discord.Member, guild: discord.Guild):
    for channel in guild.text_channels:
        await asyncio.sleep(0)
        await channel.set_permissions(member, overwrite=None)

class Unmute(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.timeParser = TimeParser()

    @commands.command()
    async def unmute(self, ctx, member: discord.Member):
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
                        embed = discord.Embed(
                            colour = discord.Colour.purple()
                        )
                        embed.set_author(name=self.bot.user.display_name + ' • UnMute', icon_url=params['punishmentsAuthorImageUrl'])
                        # embed.set_thumbnail(url='https://mxcommunity.xyz/src/MxCommunity_tr.png')
                        embed.add_field(name='Membre unmute', value=member, inline=False)
                        embed.add_field(name='Unmute par', value=author, inline=False)

                        await unmuteMember(member, guild)

                        await ctx.send(embed=embed)
                        # TODO Verify if user is already muted and if so send a message to tell the author the target is already muted
                        # TODO Actually mute the user until endDate (i.e. mute now and unmute at the end of the punishment by making sure that shutting server won't break everything)

                        # # Send message to the punishments channel to have a record of the punishment
                        # if guild:
                        #     channel = find(lambda c: c.id == params['punishmentsChannelId'], guild.channels)
                        #     if channel:
                        #         await channel.send(embed=embed)
                        # # Send message to the user so that he knows he got unmuted
                        # await member.send(embed=embed)
                    else:
                        await ctx.send("Vous ne pouvez pas unmute un bot. Veuillez réessayer avec un utilisateur valide.")
                else:
                    await ctx.send("Vous n'avez pas les permissions pour effectuer cette commande. Si vous pensez que c'est une erreur, veuillez contacter un administrateur.")
            else:
                await ctx.send("Cette commande ne peut être effectuée par un bot.")
        except KeyError as error:
            print(error)
        except Exception as error:
            print(error)


def setup(bot):
    bot.add_cog(Unmute(bot))
