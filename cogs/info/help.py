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
            description = 'Bienvenue sur MxCommuity, voici un résumé des commandes disponible sur le Discord',
            colour = discord.Colour.purple()
        )
        embed.set_footer(text='MxCommunity')
        embed.add_field(name='Info', value='• &info\n• &help\n• &mxlily\n• &brokeos\n', inline=True)
        embed.add_field(name='Dev', value='• &framework\n', inline=True)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))