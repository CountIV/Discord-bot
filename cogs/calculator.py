from random import choice
import discord
from discord.ext import commands

class Calculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["cal"])
    async def calculator(self, ctx, *, message):
        """Math calculator"""
        calc_list = []
        j = 0
        # Separates each element to a list
        for i, char in enumerate(message):
            if char == "+" or char == "-" or char == "*":
                calc_list.append(int(message[j:i]))
                calc_list.append(message[i])
                j = i+1
        calc_list.append(int(message[j:]))

        # Handles multiplication
        i = 0
        while i < len(calc_list):
            char = calc_list[i]
            if char == "*":
                calc_list[i-1] = calc_list[i-1] * calc_list[i+1]
                del calc_list[i], calc_list[i]
            else:
                i += 1

        # Handles addition and subtraction
        result = calc_list[0]
        for i, char in enumerate(calc_list):
            if i == 0:
                result = calc_list[0]
            elif char == "+":
                result += calc_list[i+1]
            elif char == "-":
                result -= calc_list[i+1]

        await ctx.send(result)


async def setup(bot):
    await bot.add_cog(Calculator(bot))