from chess import Pawn, Rook, Knight, Bishop, Queen, King

def moveable_pieces(fen):
    positions, active_colour, castling, en_passant, halfmove, fullmove = fen.split(" ")
    board = convert_to_matrix(positions)

    return 



def valid_moves(fen, piece_pos):
    positions, active_colour, castling, en_passant, halfmove, fullmove = fen.split(" ")
    row, col = piece_pos
    board = convert_to_matrix(positions)
    
    # Get the piece
    piece = board[row][col].lower()
    piece_map = {
        "p":Pawn,
        "r":Rook,
        "n":Knight,
        "b":Bishop,
        "q":Queen,
        "k":King
    }

    # Get all the tiles the piece can move to according to its own pattern
    all_moves = []
    for i in range(8):
        for j in range(8):
            all_moves.append((i, j)) if piece_map[piece].can_move((row, col), (i, j)) else None
    
    opponents = "prnbqk" if active_colour == "w" else "PRNBQK"

    # Check if it collides with any other piece or if moving it would result in a check
    valid_moves = []
    for move in all_moves:
        r, c = move

        # Get the FEN of the board after the move
        new_state = new_fen(fen, (row, col), (r, c))
        if board[r][c] in opponents.split("").append(None) and not in_check(new_state):
            valid_moves.append(move)
        else:
            continue
    ### TODO: check for breaks in valid move to see if the piece is blocked





    

    print(all_moves)
    return all_moves



# Take a FEN's positions and converts it into a list of lists
def convert_to_matrix(positions):
    matrix = [[None] * 8 for _ in range(8)]

    row, col = 0, 0
    for char in positions:
        if char == "/":
            row += 1
            col = 0
        elif char.isdigit():
            col += int(char)
        else:
            matrix[row][col] = char
            col += 1

    return matrix



def new_fen(fen, old, new):
    positions, active_colour, castling, en_passant, halfmove, fullmove = fen.split(" ")
    board = convert_to_matrix(positions)

    old_row, old_col = old
    new_row, new_col = new

    board[new_row][new_col] = board[old_row][old_col]
    board[old_row][old_col] = None
    
    # Convert the board back into FEN
    positions = ""
    empty_tiles = 0
    for row in board:
        for tile in row:
            if tile is None:
                empty_tiles += 1
            else:
                if empty_tiles > 0:
                    positions += str(empty_tiles)
                    empty_tiles = 0
                positions += tile
        if empty_tiles > 0:
            positions += str(empty_tiles)
            empty_tiles = 0
        positions += "/"

    fen = " ".join([positions, active_colour, castling, en_passant, halfmove, fullmove])
    return fen



# Determines if the active king is in check:
def in_check(fen):
    positions, active_colour, castling, en_passant, halfmove, fullmove = fen.split(" ")
    board = convert_to_matrix(positions)

    king = "K" if active_colour == "w" else "k"

    # Get the king's position, 'None' if not found
    king_pos = next(((row, col) for row in range(8) for col in range(8) if board[row][col] == king), None)

    # Raise an error if the king was not found for the active colour
    if king_pos is None:
        raise ValueError(f"Invalid FEN: King not found for {'white' if active_colour == 'w' else 'black'}")
    
    # Get the opponents colour and pieces
    opponent_is_white = king.isupper()
    opponents = "kqprnb" if opponent_is_white else "KQPRNB"

    # Get all the pieces targeting the king
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece in opponents:
                if king_pos in valid_moves(fen, (row, col)):
                    return True
    return False
    


if __name__ == "__main__":
    fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    a = convert_to_matrix(fen.split()[0])
    for i in a:
        print(i)
    
    print(new_fen(fen, (1, 0), (2, 0)))
    for i in convert_to_matrix(new_fen(fen, (1, 0), (2, 0)).split()[0]):
        print(i)