import discord
from discord.ext import commands

class Framework(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def framework(self, ctx):
        embed = discord.Embed(
            title = 'Les meilleurs framework',
            colour = discord.Colour.purple()
        )
        embed.set_author(name='MxCommunity',icon_url='https://mxcommunity.xyz/src/MxCommunity_tr.png')
        embed.add_field(name='PHP', value='• Laravel\n• Symfony\n• CakePHP', inline=True)
        embed.add_field(name='JS', value='• Angular\n• React\n• Vue.js', inline=True)
        embed.add_field(name='CSS', value='• Bootstrap\n• Tailwind\n• Foundation', inline=True)
        embed.add_field(name='MOBILE', value='• Flutter\n• React Native\n• Ionic', inline=True)
        embed.add_field(name='PYTHON', value='• Django\n• Flask\n• Bottle', inline=True)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Framework(bot))