import requests
import discord
from discord.ext import commands
from utils.config import qr_code_generator

description = """Converts a given link to a QR code."""

class QRCodeGenerator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def qr(self, ctx, *, message):
        # Set API endpoint and parameters
        api = qr_code_generator
        parameters = {"data":message, "size":"300x300"}

        # Send a GET request to the generator API
        response = requests.get(api, params=parameters)
        qr_code_image_url = response.url

        # Creates an embed object with the QR code as the image
        embed = discord.Embed(
            title = f"",
            description = f"",
        )
        embed.set_image(url=qr_code_image_url)

        await ctx.send(embed=embed)


async def setup(bot):
    # Add the QRCodeGenerator cog to the bot when called from bot.py
    await bot.add_cog(QRCodeGenerator(bot))