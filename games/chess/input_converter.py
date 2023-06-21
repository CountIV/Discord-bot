# Convert an input to python form
def input_converter(move):
    # String length is less than 2 causes an error
    if len(move) < 2:
        return ValueError

    # Converts letter part of coord
    col = ord(move[0].upper()) - 65
    if col < 65 and col > 72:
        return ValueError

    # Converts number part of coord
    if not move[1].isdigit() or int(move[1]) < 1 or int(move[1]) > 8:
        return ValueError
    row = int(move[1]) - 1
    row = abs(row - 7)

    return row, col

# Convert python coordinates to chess coordinates
def coordinate_converter(move):
    if len(move) < 2:
        return ValueError

    # Converts letter part of coord
    col = chr(move[1] + 97)

    # Converts number part of coord
    row = str(abs(move[0] - 7) + 1)

    return col + row