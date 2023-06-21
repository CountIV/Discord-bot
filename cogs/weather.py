import discord
from discord.ext import commands
import requests
from datetime import datetime

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["w"])
    async def weather(self, ctx, *, message):
        """Gives current temperature and weather of given city"""
        # API configuration
        api_key = open(".env/weather_api_key", "r").read()
        base_url = "http://api.openweathermap.org/"

        # Get location coordinates first
        geo_url = base_url + "geo/1.0/direct" + "?q=" + message + "&appid=" + api_key
        response1 = requests.get(geo_url).json()[0]
        city = response1["name"]
        lat = str(response1["lat"])
        lon = str(response1["lon"])
        unit = "metric"

        # Weather api call
        weather_url = base_url + "data/2.5/weather" + "?lat=" + lat + "&lon=" + lon + "&units=" + unit + "&appid=" + api_key
        response2 = requests.get(weather_url).json()

        # Get relevant data from requested json
        weather = response2["weather"][0]["main"]
        temperature = str(int(response2["main"]["temp"])) + "°C"

        utc_offset = (datetime.now() - datetime.utcnow()).seconds
        local_time_offset = response2["timezone"]
        sunrise = datetime.fromtimestamp(response2["sys"]["sunrise"] - utc_offset + local_time_offset).strftime("%H:%M")
        sunset = datetime.fromtimestamp(response2["sys"]["sunset"] - utc_offset + local_time_offset).strftime("%H:%M")

        embed = discord.Embed(title=city, color=0x1aa9cd)
        embed.add_field(name="Weather", value=weather)
        embed.add_field(name="Temperature", value=temperature)
        embed.add_field(name="", value="")
        embed.add_field(name="Sunrise", value=sunrise)
        embed.add_field(name="Sunset", value=sunset)
        embed.add_field(name="", value="")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Weather(bot))