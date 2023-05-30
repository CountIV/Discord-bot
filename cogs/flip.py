from random import choice
import discord
from discord.ext import commands

class Flip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help='- Flips a coin')
    async def flip(self, ctx):
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

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Flip(bot))