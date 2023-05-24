from random import choice
import discord

description = """Flips a coin."""

async def main(message):
    # Random Choice
    flip = choice(["Heads", "Tails"])
    
    # Builds Embed
    embed = discord.Embed(
        title = flip
    )
    if flip == "Heads":
        embed.set_image(url="https://cdn.discordapp.com/attachments/1087535765954777180/1110984570066714745/Heads.png")
    elif flip == "Tails":
        embed.set_image(url="https://cdn.discordapp.com/attachments/1087535765954777180/1110985253205573672/Tails.png")

    await message.channel.send(embed=embed)