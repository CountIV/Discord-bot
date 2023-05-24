import requests
import discord
from utils.config import qr_code_generator

description = """Converts a given link to a QR code."""

async def main(message):
    api = qr_code_generator
    parameters = {"data":message.content[3:], "size":"300x300"}   

    response = requests.get(api, params=parameters)
    qr_code_image_url = response.url

    embed = discord.Embed(
        title = f"",
        description = f"",
    )
    embed.set_image(url=qr_code_image_url)

    await message.channel.send(embed=embed)

