import discord
from discord.ext import commands
from discord.utils import find

from paramsGetter import getParams, getGuildId
from rolesHandler import hasAtLeastOneRole

class Clear(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def clear(self, ctx, number: int = 10):
        try:
            author = ctx.author
            guild = ctx.message.guild
            channel = ctx.channel

            # Check if author is a user (i.e. not a bot)
            if not author.bot:
                params = getParams()
                roles = params['rolesThatCanClear']
                # Check if author has permissions to perform this command
                if await hasAtLeastOneRole(author, roles):
                    if number > 0:
                        deleted = await channel.purge(limit=number)
                        logsChannel = find(lambda c: c.id == params['logsChannelId'], guild.channels)
                        if logsChannel:
                            await logsChannel.send('{} a supprimé {} message(s) du channel "{}".'.format(author.name, len(deleted), channel.name))

                else:
                    await ctx.send("Vous n'avez pas les permissions pour effectuer cette commande. Si vous pensez que c'est une erreur, veuillez contacter un administrateur.")
            else:
                await ctx.send("Cette commande ne peut être effectuée par un bot.")
        except KeyError as error:
            print(error)
        except Exception as error:
            print(error)


def setup(bot):
    bot.add_cog(Clear(bot))
