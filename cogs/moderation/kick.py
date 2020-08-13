import discord
from discord.ext import commands

from paramsGetter import getParams
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
                            await member.kick(reason=reasonMsg)
                            await ctx.send("L'utilisateur " + str(member) + " a été kick avec succès." + ((" Raison: " + reasonMsg) if reasons else ''))
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
