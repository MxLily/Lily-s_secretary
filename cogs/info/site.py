import discord
from discord.ext import commands

# Print Site

class Site(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def site(self, ctx):
        embed = discord.Embed(
            title = '<:info:718551227809660948>  Site web  <:info:718551227809660948>',
            description= 'https://mxcommunity.xyz',
            colour = discord.Colour.purple()
        )
        embed.set_author(name='MxCommunity',icon_url='https://mxcommunity.xyz/src/MxCommunity_tr.png')
        embed.set_thumbnail(url='https://mxcommunity.xyz')

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Site(bot))