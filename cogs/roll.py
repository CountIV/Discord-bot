import re
import discord
from random import randint

description = """Rolls polyhedral dice. This command accepts inputs of the form [number]d[number], where the first number is the amound of dice you want to roll and the second number is the amound of sides on the dice."""


async def main(message):
    # Search for the roll input with regex
    roll = re.search("[0-9]+d[0-9]+", message.content)

    # If the input is empty, assume 1d6
    if message.content == "!roll":
        embed = discord.Embed(
        title = str(randint(1, 6)),
        description = f"",
        color = 16777215
        )
        await message.channel.send(embed=embed)
        return

    # If the input is invalid, return an error message
    if roll == None:
        embed = discord.Embed(
        title = "Invalid input",
        description = f"This command accepts inputs of the form [number]d[number], \nwhere the first number is the amound of dice you want to roll and the second number is the amound of sides on the dice.",
        color = 16711680
        )
        embed.set_footer(text="E.g. 2d6 to roll two six-sided dice")
        await message.channel.send(embed=embed)
        return
    
    
    # Isolate the roll input
    roll = roll.group()

    # Split the roll input
    dice_count, dice_size = roll.split("d")

    # Convert to int values
    dice_count = int(dice_count)
    dice_size = int(dice_size)

    # Determine roll values
    rolls = [randint(1, dice_size) for _ in range(dice_count)]
    total = sum(rolls)

    # Convert to string and join with an empty space for readability
    _rolls = [str(i) for i in rolls]
    _rolls = " ".join(_rolls)
    embed = discord.Embed(
        title = f"Rolling {dice_count} {dice_size}-sided dice",
        description = f"Individual rolls: \n{_rolls}\nTotal: {total}",
        color = 16777215
    )

    await message.channel.send(embed=embed)



    