import discord
from discord.ext import commands

# Print Site

class MxLily(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mxlily(self, ctx):
        embed = discord.Embed(
            title = '<:info:718551227809660948>  MxLily  <:info:718551227809660948>',
            description= 'Fondatrice de la MxCommunity',
            colour = discord.Colour.purple()
        )
        embed.set_image(url='https://avatars0.githubusercontent.com/u/66841164?s=460&u=de5f8d56913b1e7b18e0109c527cf49b0af1d483&v=4')
        embed.set_author(name='MxCommunity', icon_url='https://mxcommunity.xyz/src/MxCommunity_tr.png')
        embed.add_field(name='Twitter', value='https://twitter.com/MxLily_dev')
        embed.add_field(name='GitHub', value='https://github.com/MxLily')
        embed.add_field(name='Discord', value='𝑴𝒙𝑳𝒊𝒍𝒚#6666')

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(MxLily(bot))