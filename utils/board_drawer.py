import discord
from io import BytesIO
from pathlib import Path
from PIL import ImageDraw, Image, ImageFont



# Create a new image with a white background
def generate_board(board_size, white_to_move=True):
    # Set the colours
    light_color = (240, 217, 181, 255)
    dark_color = (181, 136, 99, 255)

    # Set the square size and overall image size
    square_size = 128
    image_size = board_size * square_size

    image = Image.new('RGBA', (image_size + square_size, image_size + square_size), (155, 111, 74, 255))

    # Create a drawing object
    draw = ImageDraw.Draw(image)

    # Borders for the board
    draw.rectangle([0, 0, square_size * 8 + 3, square_size * 8 + 3], fill=(231, 195, 139, 255))

    # Iterate over the board squares and draw
    for row in range(board_size):
        for col in range(board_size):
            x = col * square_size
            y = row * square_size
            square_color = light_color if (row + col) % 2 == 0 else dark_color
            draw.rectangle([x, y, x + square_size, y + square_size], fill=square_color)

    # Define the font
    try:
        font = ImageFont.truetype('arialbd.ttf', 32)
    except:
        font = ImageFont.truetype('/usr/share/fonts/dejavu/DejaVuSansMono-Bold.ttf', 32)
    text_colour = (231, 195, 139, 255)

    # Draw coordinate labels on the right and bottom
    for i in range(board_size):
        x = image_size
        y = (i + 0.58) * square_size
        label = str(board_size - i) if white_to_move else str(i + 1)
        text_width, text_height = draw.textsize(label, font=font)
        draw.text((x + square_size // 3 // 2, y - text_height // 2),
                  label, fill=text_colour, font=font, anchor="mm")

    for i in range(board_size):
        x = (i + 0.58) * square_size
        y = image_size
        label = chr(97 + i) if white_to_move else chr(97 + board_size - i - 1)
        label = label.upper()
        text_width, text_height = draw.textsize(label, font=font)
        draw.text((x - text_width // 2, y + square_size // 3 // 2),
                  label, fill=text_colour, font=font, anchor="mm")
    
    # Trim the bottom and right corners
    trim = 90
    old_width, old_height = image.size
    new_width = old_width - trim
    new_height = old_height - trim

    image = image.crop((0, 0, new_width, new_height))

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
    board = generate_board(8, white_to_move)
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