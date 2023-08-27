import discord
from discord.ext import commands
from games.chess.board_drawer import get_board
from games.chess.game import Game
from games.chess.board_transform import game_to_fen, fen_to_game


class Chess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def visualize(self, ctx, *, fen):
        """Draws a board using the FEN (Forsyth-Edwards Notation) representation."""
        chessboard, embed = get_board(fen)
        await ctx.send(file=chessboard, embed=embed)

    @commands.command()
    async def startchess(self, ctx):
        """Start a new chess a game"""
        chessboard, embed = get_board(game_to_fen(Game()))
        await ctx.send(file=chessboard, embed=embed)


async def setup(bot):
    await bot.add_cog(Chess(bot))