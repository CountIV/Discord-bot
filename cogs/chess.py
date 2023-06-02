import discord
from io import BytesIO
from discord.ext import commands
from utils.fen_visualizer import fen_visualizer



class Chess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.command()
    async def visualize(self, ctx, fen, white_to_move=True):
        """- Draw a board using FEN notation"""

        chessboard = fen_visualizer(fen, white_to_move)

        # Conver the image object into a format compatible with discord.py
        image_stream = BytesIO()
        chessboard.save(image_stream, format="PNG")
        image_stream.seek(0)
        chessboard = discord.File(image_stream, filename='chessboard.png')

        embed = discord.Embed()
        embed.set_image(url="attachment://chessboard.png")

        await ctx.send(file=chessboard, embed=embed)



async def setup(bot):
    await bot.add_cog(Chess(bot))