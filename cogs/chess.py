import discord
from discord.ext import commands
from games.chess.board_drawer import get_board
from games.chess.game import Game
from games.chess.board_transform import game_to_fen, fen_to_game
from games.chess.input_converter import input_converter


class Chess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game_state = None

    @commands.command()
    async def visualize(self, ctx, *, fen):
        """Draws a board using the FEN (Forsyth-Edwards Notation) representation."""
        chessboard, embed = get_board(fen)
        await ctx.send(file=chessboard, embed=embed)

    @commands.command(aliases=["cs"])
    async def startchess(self, ctx):
        """Start a new chess a game"""
        self.game_state = Game()
        fen_state = game_to_fen(self.game_state)
        chessboard, embed = get_board(fen_state)
        await ctx.send(file=chessboard, embed=embed)

    @commands.command(aliases=["cp"])
    async def playchess(self, ctx, *, move):
        """Move a chess piece i.e \"E2E4\", promotion \"E7E8Q\""""
        # Change user input for game to read
        str_coord = input_converter(move[:2])
        dest_coord = input_converter(move[2:])
        if str_coord == ValueError or dest_coord == ValueError:
            await ctx.send("Invalid input!")
            return
        # Fifth character tells which piece Pawn promotes to
        promotion = False
        if len(move) >= 5:
            promotion = move[4]

        # game_state.move tries to move a piece with according to user's input
        # move_result stores whether the move was successful in form of strings
        move_result = self.game_state.move(str_coord, dest_coord, promotion)

        # Send embed/message to discord depending on move_result
        if move_result == True or move_result == "check" or move_result == "checkmate" or move_result == "draw":
            fen_state = game_to_fen(self.game_state)
            chessboard, embed = get_board(fen_state)
            await ctx.send(file=chessboard, embed=embed)

            if move_result == "checkmate":
                if self.game_state.turn == "b":
                    await ctx.send("Checkmate!\nWhite wins!")
                else:
                    await ctx.send("Checkmate!\nBlack wins!")
            elif move_result == "draw":
                await ctx.send("Draw!")
        else:
            await ctx.send(f"Invalid move! Explaination: {move_result}")

async def setup(bot):
    await bot.add_cog(Chess(bot))