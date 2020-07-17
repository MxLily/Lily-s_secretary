import discord
from discord.ext import commands

class Logiciel(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def logiciel(self, ctx):
        embed = discord.Embed(
            title = 'Les meilleurs logiciels pour développer',
            colour = discord.Colour.red()
        )
        embed.set_footer(text='MxCommunity')
        embet.set_author(name='Name', icon_url='https://cdn.shortpixel.ai/client/q_glossy,ret_img/https://lilydieudonne.com/wp-content/uploads/2019/10/cropped-MG_4684-small.jpg')
        embed.add_field(name='Editeurs de textes', value='• Visual Studio Code (multi-langage)\n• Sublime Text (multi-langage)\n• pyCharm (Python)\n• Eclipse (Java)\n• IntelliJ (Java)\n• Android Studio (Java & Kotlin)\n• Aptana Studio 3 (HTML - CSS  - JS)\n• PhpStorm (PHP)\n• WebStorm (JavaScript)\n• RubyMine (Ruby)', inline=True)
        embed.add_field(name='Partage de projets', value='• GitHub\n• GitLab\n• Repl.it', inline=True)
        embed.add_field(name='Base de données', value='...', inline=True)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Logiciel(bot))