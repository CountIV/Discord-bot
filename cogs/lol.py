import discord
from discord.ext import commands
import requests
from datetime import datetime

class Lol(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = open(".env/riot_api_key", "r").read()

    @commands.command()
    async def clash(self, ctx):
        """Provides information on the start time of the next clash event."""
        # API configuration
        api_url = "https://euw1.api.riotgames.com/lol/clash/v1/tournaments" + "?api_key=" + self.api_key

        # Response body gets saved in data variable
        response = requests.get(api_url)
        data = response.json()

        # If no to data is sent back
        if data == []:
            await ctx.send("No upcoming Clash found, stay tuned!")
            return

        # Get the smallest, which also means the nearest clash, start and end date
        min_start_time = float("inf")
        min_end_time = float("inf")
        for item in data:
            start_time = item['schedule'][0]['registrationTime']
            end_time = item['schedule'][0]['startTime'] # Yes, startTime is actually ending time

            if start_time < min_start_time:
                min_start_time = start_time
                min_end_time = end_time

        # TierIV starts at start_time, every other tier later in a time not present in data
        # TODO: Implement the other tiers and don't hardcode it in the code
        tierIII_adjustment = 8100000 # 2h15m

        # Get datetime objects
        clash_start_time = datetime.fromtimestamp((min_start_time + tierIII_adjustment) / 1000)
        clash_end_time = datetime.fromtimestamp(min_end_time / 1000)
        current_time = datetime.now()
        time_until_clash_start = clash_start_time - current_time

        # Respond with appropriate message depending on the current time
        bot_response = None
        if clash_end_time < current_time:
            bot_response = "Registration has ended, may your Clash be victorious!"
        elif clash_start_time < current_time:
            bot_response = "Clash is open right now, @everyone all aboard!"
        else:
            days = time_until_clash_start.days
            hours = time_until_clash_start.seconds // 3600
            minutes = (time_until_clash_start.seconds // 60) % 60
            seconds = time_until_clash_start.seconds % 60
            bot_response = f"Next Clash starts in {days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

        await ctx.send(bot_response)


    @commands.command()
    async def online(self, ctx, *, user):
        """Online"""
        api_url = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + user + "?api_key=" + self.api_key

        response = requests.get(api_url).json()
        date = datetime.fromtimestamp(response["revisionDate"] // 1000).strftime("%Y-%m-%d %H:%M")
        name = response["name"]

        embed = discord.Embed(title=f"{name} | Last seen", description=date)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Lol(bot))