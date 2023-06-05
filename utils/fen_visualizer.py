import discord
from io import BytesIO
from PIL import ImageDraw
from utils.pieces import pieces
from utils.board import generate_board



def fen_visualizer(fen, white_to_move: bool):
    if white_to_move:
        fen = fen.split("/")
        fen = "/".join(reversed(fen))
    board = generate_board(8)
    draw = ImageDraw.Draw(board)
    row = 8 - 1
    col = 0

    for char in fen:
        if char == '/':
            row -= 1
            col = 0
        elif char.isdigit():
            col += int(char)
        else:
            colour = "white" if char == char.upper() else "black"
            piece = pieces[colour][char]

            x = col * 8
            y = row * 8

            # Determine the position of the chess piece image
            piece_x = x + (8 - piece.size[0]) // 2
            piece_y = y + (8 - piece.size[1]) // 2

            # Paste the chess piece image onto the chessboard
            board.alpha_composite(piece, (piece_x, piece_y))

            col += 1

    return board



def get_board(fen):
        """- Draw a board using FEN notation"""

        positions, active_colour, castling, en_passant, halfmove, fullmove = fen.split(" ")

        # assigns values depending on if it is white's turn to move
        active_colour = False if active_colour == "b" else True

        chessboard = fen_visualizer(positions, active_colour)

        # Conver the image object into a format compatible with discord.py
        image_stream = BytesIO()
        chessboard.save(image_stream, format="PNG")
        image_stream.seek(0)
        file = discord.File(image_stream, filename='chessboard.png')

        embed = discord.Embed(title=f"{'White' if active_colour else 'Black'} to move")
        embed.set_image(url="attachment://chessboard.png")

        # await ctx.send(file=file, embed=embed)
        return file, embed