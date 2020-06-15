import discord
from discord.ext import commands

class Github(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def github(self, ctx):
        await ctx.send("**Mon profil Github : https://github.com/MxLily **")
        await ctx.send("_N'hésite pas à mettre des étoiles sur mes divers projets_ <:Eevee_Shrug:718551270243434617>")

def setup(bot):
    bot.add_cog(Github(bot))