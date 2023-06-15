from discord.ext import commands
import requests

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["w"])
    async def weather(self, ctx, *, city):
        """Gives current temperature and weather of given city"""
        # API configuration
        api_key = open(".env/weather_api_key", "r").read()
        base_url = "http://api.openweathermap.org/"

        # Get location coordinates first
        geo_url = base_url + "geo/1.0/direct" + "?q=" + city + "&appid=" + api_key
        response1 = requests.get(geo_url).json()[0]
        lat = str(response1["lat"])
        lon = str(response1["lon"])
        unit = "metric"

        # Weather api call
        weather_url = base_url + "data/2.5/weather" + "?lat=" + lat + "&lon=" + lon + "&units=" + unit + "&appid=" + api_key
        response2 = requests.get(weather_url).json()

        # Get relevant data from requested json
        temp = response2["main"]["temp"]
        weather = response2["weather"][0]["description"]

        await ctx.send(f"Temperature is {temp} and weather is {weather}")

async def setup(bot):
    await bot.add_cog(Weather(bot))