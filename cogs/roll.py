import re
import discord
from random import randint
from discord.ext import commands


class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def roll(self, ctx, roll="1d6"):
        """- Rolls dice of the form [dice count]d[dice size] E.g. \"2d6\" to roll two six-sided dice"""

        # Search for the roll input with regex
        pattern = re.search("[0-9]+d[0-9]+", roll)
        
        # If the input is invalid, return an error message
        if pattern == None:
            embed = discord.Embed(
            title = "Invalid input",
            description = f"This command accepts inputs of the form [number]d[number], \nwhere the first number is the amound of dice you want to roll and the second number is the amound of sides on the dice."
            )
            embed.set_footer(text="E.g. 2d6 to roll two six-sided dice")
            await ctx.send(embed=embed)
            return
        
        # Isolate the roll input
        roll = pattern.group()

        # Split the roll input
        dice_count, dice_size = roll.split("d")

        # Convert to int values
        dice_count = int(dice_count)
        dice_size = int(dice_size)

        if dice_size * dice_count > 10000000:
            embed = discord.Embed(title = f"Input too large")
            await ctx.send(embed=embed)
            return

        # Determine roll values
        calculated_rolls = [randint(1, dice_size) for _ in range(dice_count)]
        total = sum(calculated_rolls)

        # If there is only 1 dice, roll only one
        if roll[0:1] == "1d" and roll[2:].isnumeric():
            embed = discord.Embed(title = f"{randint(1, int(roll[2:]))}")
            await ctx.send(embed=embed)
            return
        
        # Convert to string with formatted leading zeroes and join with an empty space
        individual_rolls = " ".join([str(f"%0{len(str(dice_size))}d" % i) for i in calculated_rolls])
        # Change format depending on dice count
        if dice_count == 1:
            embed = discord.Embed(title=f"{total}")
        elif dice_count * len(str(dice_size)) > 4000:
            embed = discord.Embed(
            title = f"Rolling {dice_count}x {dice_size}-sided dice",
            description=f"Total: **{total}**"
        )
        else:
            embed = discord.Embed(
                title = f"Rolling {dice_count}x {dice_size}-sided dice",
                description = f"```haskell\n{individual_rolls}```\nTotal: **{total}**",
            )
        
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Roll(bot))