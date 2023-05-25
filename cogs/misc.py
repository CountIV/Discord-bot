import re
import discord
import requests
from random import randint
from discord.ext import commands
from utils.config import qr_code_generator


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = """- This category contains small, miscellaneous commands"""


    @commands.command()
    async def say(self, ctx, *, message):
        """- Repeats the provided message."""
        await ctx.send(message)


    @commands.command()
    async def roll(self, ctx, *, roll):
        """- Rolls dice of the form [number]d[number]"""
        # Search for the roll input with regex
        roll = re.search("[0-9]+d[0-9]+", roll)
        
        # If the input is invalid, return an error message
        if roll == None:
            embed = discord.Embed(
            title = "Invalid input",
            description = f"This command accepts inputs of the form [number]d[number], \nwhere the first number is the amound of dice you want to roll and the second number is the amound of sides on the dice.",
            color = 16711680
            )
            embed.set_footer(text="E.g. 2d6 to roll two six-sided dice")
            await ctx.send(embed=embed)
            return
        
        # Isolate the roll input
        roll = roll.group()

        # Split the roll input
        dice_count, dice_size = roll.split("d")

        # Convert to int values
        dice_count = int(dice_count)
        dice_size = int(dice_size)

        # Determine roll values
        calculated_rolls = [randint(1, dice_size) for _ in range(dice_count)]
        total = sum(calculated_rolls)

        # Convert to string and join with an empty space for readability
        individual_rolls = " ".join([str(i) for i in calculated_rolls])
        embed = discord.Embed(
            title = f"Rolling {dice_count} {dice_size}-sided dice",
            description = f"Individual rolls: \n{individual_rolls}\nTotal: {total}",
            color = 16777215
        )

        await ctx.send(embed=embed)


    @commands.command()
    async def qr(self, ctx, *, link):
        """- Converts a given link to a QR code."""
        # Set API endpoint and parameters
        api = qr_code_generator
        parameters = {"data":link, "size":"300x300"}

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
    # Add the Misc cog to the bot when called from bot.py
    await bot.add_cog(Misc(bot))