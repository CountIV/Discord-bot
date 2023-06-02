from PIL import Image
from pathlib import Path

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

    # Determine the color based on the file name prefix
    if file_name.startswith(black):
        color = "black"
    elif file_name.startswith(white):
        color = "white"
    else:
        continue  # Skip files that don't match the expected naming convention

    # Remove the color prefix from the file name
    piece = file_name[1:].lower()

    # Add the image to the corresponding dictionary
    pieces[color][piece] = image