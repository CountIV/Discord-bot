def moveable_pieces(fen):
    positions, active_colour, castling, en_passant, halfmove, fullmove = fen.split(" ")

    ### Determine if the active king is in check:

    board = convert_to_matrix(positions)
    checks = active_checks(fen, board, active_colour)



    pieces: list[str] = ...
    return pieces



def valid_moves(fen, piece):
    positions, active_colour, castling, en_passant, halfmove, fullmove = fen.split(" ")
    ...

    ...
    moves: list[str] = ...
    return moves



def convert_to_matrix(positions):
    matrix = [[None] * 8 for _ in range(8)]

    row, col = 0, 0
    for char in positions:
        if char == '/':
            row += 1
            col = 0
        elif char.isdigit():
            col += int(char)
        else:
            matrix[row][col] = char
            col += 1

    return matrix



def active_checks(fen, board, active_colour):
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
    threats = []
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece in opponents:
                if king_pos in valid_moves(fen, piece):
                    threats.append((piece, (row, col))) 
    
    if len(threats) > 0:
        return threats
    return None
    


if __name__ == "__main__":
    a = convert_to_matrix('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
    for i in a:
        print(i)