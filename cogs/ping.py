import discord
from discord.ext import commands

class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help='- Tests server ping')
    async def ping(self, ctx):
        await ctx.send(f"Ping is {round(self.bot.latency * 1000)}ms")

async def setup(bot):
    await bot.add_cog(ping(bot))