from PIL import ImageDraw
from utils.pieces import pieces
from utils.board import generate_board, board_size, square_size


def fen_visualizer(fen, white_to_move: bool):
    if white_to_move:
        fen = fen.split("/")
        fen = "/".join(reversed(fen))
    board = generate_board()
    draw = ImageDraw.Draw(board)
    row = board_size - 1
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

            x = col * square_size
            y = row * square_size

            # Determine the position of the chess piece image
            piece_x = x + (square_size - piece.size[0]) // 2
            piece_y = y + (square_size - piece.size[1]) // 2

            # Paste the chess piece image onto the chessboard
            board.alpha_composite(piece, (piece_x, piece_y))

            col += 1
    
    return board