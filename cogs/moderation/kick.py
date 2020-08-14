import discord
from discord.ext import commands
from discord.utils import find

from paramsGetter import getParams, getGuildId
from rolesHandler import hasAtLeastOneRole

class Kick(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *reasons):
        try:
            author = ctx.author
            # Check if author is a user (i.e. not a bot)
            if not author.bot:
                params = getParams()
                roles = params['rolesThatCanKick']
                # Check if author has permissions to perform this command
                if await hasAtLeastOneRole(author, roles):
                    # Check if the target is a user (i.e. not a bot)
                    if not member.bot:
                        rolesToAvoid = params['rolesThatCannotBeKicked']
                        # Check if the target can receive this command
                        if not await hasAtLeastOneRole(member, rolesToAvoid):
                            reasonMsg = reasonMsg = ' '.join(reasons) if reasons else ''

                            embed = discord.Embed(
                                colour = discord.Colour.purple()
                            )
                            embed.set_author(name=self.bot.user.display_name + ' • Kick', icon_url=params['punishmentsAuthorImageUrl'])
                            # embed.set_author(name=self.bot.user.display_name + ' • Kick ✅', icon_url=params['punishmentsAuthorImageUrl'])
                            # embed.set_thumbnail(url='https://mxcommunity.xyz/src/MxCommunity_tr.png')
                            embed.add_field(name='Membre kick', value=member, inline=False)
                            embed.add_field(name='Kick par', value=author, inline=False)
                            if reasons:
                                embed.add_field(name='Raison', value=reasonMsg, inline=False)

                            # Send message to the punishments channel to have a record of the punishment
                            guildId = await getGuildId()
                            guild = find(lambda g: g.id == guildId, self.bot.guilds)
                            if guild:
                                channel = find(lambda c: c.id == params['punishmentsChannelId'], guild.channels)
                                if channel:
                                    await channel.send(embed=embed)
                            # Send message to the user so that he knows why he got kicked
                            await member.send(embed=embed)
                            # Actually kick him
                            await member.kick(reason=reasonMsg)
                        else:
                            await ctx.send("Vous ne pouvez pas kick cet utilisateur à cause des rôles qui lui sont attribués.")
                    else:
                        await ctx.send("Vous ne pouvez pas kick un bot. Veuillez réessayer avec un utilisateur valide.")
                else:
                    await ctx.send("Vous n'avez pas les permissions pour effectuer cette commande. Si vous pensez que c'est une erreur, veuillez contacter un administrateur.")
            else:
                await ctx.send("Cette commande ne peut être effectuée par un bot.")
        except KeyError as error:
            print(error)
        except Exception as error:
            print(error)


def setup(bot):
    bot.add_cog(Kick(bot))
