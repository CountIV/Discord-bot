import discord
from discord.ext import commands
from utils.board_drawer import get_board


class Chess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def visualize(self, ctx, *, fen):
        """- Draw a board using FEN notation"""
        chessboard, embed = get_board(fen)
        await ctx.send(file=chessboard, embed=embed)



async def setup(bot):
    await bot.add_cog(Chess(bot))