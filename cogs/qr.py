import discord
import requests
from discord.ext import commands


class QR(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def qr(self, ctx, *, link):
        """- Converts a given link to a QR code."""
        # Set API endpoint and parameters
        api = "https://api.qrserver.com/v1/create-qr-code/"
        parameters = {"data":link, "size":"300x300"}

        # Send a GET request to the generator API
        response = requests.get(api, params=parameters)
        qr_code_image_url = response.url

        # Creates an embed object with the QR code as the image
        embed = discord.Embed()
        embed.set_image(url=qr_code_image_url)
        await ctx.send(embed=embed)



async def setup(bot):
    await bot.add_cog(QR(bot))