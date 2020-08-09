import discord
from discord.ext import commands

class Brokeos(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def brokeos(self, ctx):
        embed = discord.Embed(
            title = '<:info:718551227809660948>  Brokeos  <:info:718551227809660948>',
            description= 'Administrateur de la MxCommunity',
            colour = discord.Colour.purple()
        )
        embed.set_image(url='https://avatars1.githubusercontent.com/u/8388746?s=460&u=10ad7500f7efcbbeeeba45f829ef941c4be1c16f&v=4')
        embed.set_author(name='MxCommunity', icon_url='https://mxcommunity.xyz/src/MxCommunity_tr.png')
        embed.add_field(name='Twitter', value='https://twitter.com/brokeosmc')
        embed.add_field(name='GitHub', value='https://github.com/Brokeos')
        embed.add_field(name='Discord', value='Brokeos#2292')

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Brokeos(bot))