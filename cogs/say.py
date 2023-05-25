from discord.ext import commands


description = """Repeats the provided message."""


class Repeat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *, message):
        await ctx.send(message)


async def setup(bot):
    # Add the Repeat cog to the bot when called from bot.py
    await bot.add_cog(Repeat(bot))