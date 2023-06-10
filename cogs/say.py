from discord.ext import commands

class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def repeat(self, ctx, *, message):
        """Repeats the provided message."""
        await ctx.send(message)



async def setup(bot):
    await bot.add_cog(Say(bot))