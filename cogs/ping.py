import discord
from discord.ext import commands

class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx, *, user: discord.Member=None):
        """- Tests server ping"""
        if user == None:
            await ctx.send(f"Ping is {round(self.bot.latency * 1000)}ms")
            return
        
        """- Alternative: Ping someone"""
        await ctx.send(user.mention)

async def setup(bot):
    await bot.add_cog(ping(bot))