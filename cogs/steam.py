from discord.ext import commands
import requests

class Steam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Sends the newest Hollow Knight news
    @commands.command()
    async def hk(self, ctx):
        response = requests.get("https://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=367520&count=3&maxlength=300&format=json")
        data = response.json()
        newstitle = data["appnews"]["newsitems"][0]["title"]
        await ctx.send(newstitle)


async def setup(bot):
    await bot.add_cog(Steam(bot))