import discord
from discord.ext import commands

# Print Info

class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx):
        embed = discord.Embed(
            title = '<:info:718551227809660948> Liste des commandes <:info:718551227809660948>',
            colour = discord.Colour.red()
        )
        embed.set_author(name='MxCommunity',icon_url='https://mxcommunity.xyz/src/MxCommunity_tr.png')
        embed.add_field(name='Help', value='• &info\n', inline=True)
        embed.add_field(name='Lily', value='• &github\n', inline=True)
        embed.add_field(name='Dev', value='• &framework\n', inline=True)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))