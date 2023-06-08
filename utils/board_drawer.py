import discord
from io import BytesIO
from pathlib import Path
from PIL import ImageDraw, Image



# Create a new image with a white background
def generate_board(board_size):
    # Set the colours
    light_color = (240, 217, 181, 255)
    dark_color = (181, 136, 99, 255)

    # Set the square size and overall image size
    square_size = 128
    image_size = board_size * square_size

    image = Image.new('RGBA', (image_size, image_size), light_color)

    # Create a drawing object
    draw = ImageDraw.Draw(image)

    # Iterate over the board squares and draw
    for row in range(board_size):
        for col in range(board_size):
            x = col * square_size
            y = row * square_size
            square_color = light_color if (row + col) % 2 == 0 else dark_color
            draw.rectangle([x, y, x + square_size, y + square_size], fill=square_color)

    return image



# Get the images of each piece
def get_pieces():
    pieces = {
        'black': {},
        'white': {}
    }

    # Prefixes for black and white pieces
    black = 'b'
    white = 'w'

    # Iterate over the image files in the folder
    folder = Path("resources/chess")
    for file_path in folder.glob("*.png"):
        file_name = file_path.stem
        image = Image.open(file_path)
        image = image.resize((160, 160))

        # Determine the color based on the file name prefix
        if file_name.startswith(black):
            colour = "black"
        elif file_name.startswith(white):
            colour = "white"
        else:
            continue  # Skip files that don't match the expected naming convention

        # Remove the color prefix from the file name
        if "Knight" in file_name:
            piece = "N" if colour == 'white' else "n"
        else:
            piece = file_name[1] if colour == 'white' else file_name[1].lower()

        # Add the image to the corresponding dictionary
        pieces[colour][piece] = image
    
    return pieces



# Combine the board and pieces into one image
def draw(fen, white_to_move: bool):
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
            piece = get_pieces()[colour][char]

            x = col * 128
            y = row * 128

            # Determine the position of the chess piece image
            piece_x = x + (128 - piece.size[0]) // 2
            piece_y = y + (128 - piece.size[1]) // 2

            # Paste the chess piece image onto the chessboard
            board.alpha_composite(piece, (piece_x, piece_y))

            col += 1

    return board



def get_board(fen):
        """- Draw a board using FEN notation"""

        positions, active_colour, castling, en_passant, halfmove, fullmove = fen.split(" ")

        # assigns values depending on if it is white's turn to move
        active_colour = False if active_colour == "b" else True

        chessboard = draw(positions, active_colour)

        # Conver the image object into a format compatible with discord.py
        image_stream = BytesIO()
        chessboard.save(image_stream, format="PNG")
        image_stream.seek(0)
        file = discord.File(image_stream, filename='chessboard.png')

        embed = discord.Embed(title=f"{'White' if active_colour else 'Black'} to move")
        embed.set_image(url="attachment://chessboard.png")

        # await ctx.send(file=file, embed=embed)
        return file, embed