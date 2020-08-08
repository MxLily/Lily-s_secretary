import discord
import sys
from discord.ext import commands

class Langage(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def langage(self, ctx, arg):
        lg = arg
        if lg == "java":
            embed = discord.Embed(
            title = 'Apprendre de Java',
            colour = discord.Colour.red()
            )
            embed.set_footer(text='MxCommunity')
            embed.add_field(name='Pourquoi apprendre le Java', value='• Visual Studio Code (multi-langage)\n• Sublime Text (multi-langage)\n• pyCharm (Python)\n• Eclipse (Java)\n• IntelliJ (Java)\n• Android Studio (Java & Kotlin)\n• Aptana Studio 3 (HTML - CSS  - JS)\n• PhpStorm (PHP)\n• WebStorm (JavaScript)\n• RubyMine (Ruby)', inline=True)
            embed.add_field(name='Ou apprendre le Java', value='• GitHub\n• GitLab\n• Repl.it', inline=True)
            await ctx.send(embed=embed)
        elif lg == "pyhton":
            print("2")
        else:
            print("&info")


def setup(bot):
    bot.add_cog(Langage(bot))