import discord
from discord.ext import commands

class Logiciel(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def logiciel(self, ctx):
        embed = discord.Embed(
            title = 'Les meilleurs logiciels pour développer',
            colour = discord.Colour.purple()
        )
        embed.set_author(name='MxCommunity',icon_url='https://mxcommunity.xyz/src/MxCommunity_tr.png')
        embed.add_field(name='Editeurs de textes', value='• Visual Studio Code (multi-langage)\n• Sublime Text (multi-langage)\n• pyCharm (Python)\n• Eclipse (Java)\n• IntelliJ (Java)\n• Android Studio (Java & Kotlin)\n• Aptana Studio 3 (HTML - CSS  - JS)\n• PhpStorm (PHP)\n• WebStorm (JavaScript)\n• RubyMine (Ruby)', inline=True)
        embed.add_field(name='Partage de projets', value='• GitHub\n• GitLab\n• Repl.it', inline=True)
        embed.add_field(name='Base de données', value='...', inline=True)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Logiciel(bot))