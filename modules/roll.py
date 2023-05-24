import re
import discord
from random import randint

async def main(message):
    # Search for the roll input with regex
    roll = re.search("[0-9]+d[0-9]+", message.content)

    # If the input is invalid, return an error message
    if roll == None:
        embed = discord.Embed(
        title = "Invalid input",
        description = f"This command accepts inputs of the form [number]d[number], \nwhere the first number is the amound of dice you want to roll and the second number is the amound of sides on the dice.",
        color = 16777215
        )
        embed.set_footer(text="E.g. 2d6 to roll two six-sided dice")
        await message.channel.send(embed=embed)
        return
    
    # Isolate the roll input
    roll = roll.group()

    # Convert to int
    dice_count, dice_size = roll.split("d")
    dice_count = int(dice_count)
    dice_size = int(dice_size)

    rolls = [randint(1, dice_size) for _ in range(dice_count)]
    total = sum(rolls)

    _rolls = [str(i) for i in rolls]
    _rolls = " ".join(_rolls)
    embed = discord.Embed(
        title = "Polyhedral dice roll",
        description = f"Individual rolls: \n{_rolls}\nTotal: {total}",
        color = 16777215
    )

    await message.channel.send(embed=embed)



    