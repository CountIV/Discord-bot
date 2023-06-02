from PIL import Image, ImageDraw


# Set the size of the chessboard
board_size = 8

# Set the square size and overall image size
square_size = 128
image_size = board_size * square_size

# Set the colours
light_color = (240, 217, 181, 255)
dark_color = (181, 136, 99, 255)

# Create a new image with a white background
def generate_board():
    image = Image.new('RGBA', (image_size, image_size), light_color)

    # Create a drawing object
    draw = ImageDraw.Draw(image)

    # Iterate over the chessboard squares and draw
    for row in range(board_size):
        for col in range(board_size):
            x = col * square_size
            y = row * square_size
            square_color = light_color if (row + col) % 2 == 0 else dark_color
            draw.rectangle([x, y, x + square_size, y + square_size], fill=square_color)

    return image