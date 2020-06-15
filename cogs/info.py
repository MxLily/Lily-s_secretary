import discord
from discord.ext import commands

# Print Info

class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx):
        await ctx.send("<:info:718551227809660948> **Info** <:info:718551227809660948>")
        await ctx.send("__**Liste des commandes :**__")
        await ctx.send("\t**&github** : Lien vers mon github")


def setup(bot):
    bot.add_cog(Info(bot))