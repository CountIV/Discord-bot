import discord
from discord.ext import commands
import requests
import datetime

class Clash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help='- Informs when the next Clash starts')
    async def clash(self, ctx):
        api_key = open(".env/riot_api_key", "r").read()
        api_url = "https://euw1.api.riotgames.com/lol/clash/v1/tournaments" + "?api_key=" + api_key

        response = requests.get(api_url)
        data = response.json()


        min_startTime = float("inf")
        for item in data:
            startTime = item['schedule'][0]['startTime']

            if startTime < min_startTime:
                min_startTime = startTime
        
        date = datetime.datetime.fromtimestamp(min_startTime / 1000)

        await ctx.send(f"Next Clash starts at {date}")

async def setup(bot):
    await bot.add_cog(Clash(bot))