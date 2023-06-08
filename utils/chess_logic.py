import chess


# Get the valid moves for a given square on a chessboard in a given FEN position.
def get_legal_moves(fen, square):
    # Create a chess board and get the piece at the given square
    board = chess.Board(fen)
    piece = board.piece_at(chess.parse_square(square))

    if piece is not None:
        # Find the valid moves for the piece on the given square
        valid_moves = [move.uci() for move in board.legal_moves if move.from_square == chess.parse_square(square)]
        return valid_moves
    else:
        # If there are no pieces on the given square, return an empty list
        return []


# Get the position of valid pieces that can make legal moves in a given FEN position.
def get_valid_pieces(fen):
    # Chess board object 
    board = chess.Board(fen)
    valid_pieces = []

    # Iterate over every piece and add their position to the list if legal moves exist
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            moves = board.legal_moves
            for move in moves:
                if move.from_square == square:
                    valid_pieces.append(chess.SQUARE_NAMES[square])
                    break
    return valid_pieces


# Get all legal moves in a given FEN position.
def get_all_moves(fen):
    pieces = get_valid_pieces(fen)
    all_moves = []
    for i in pieces:
        all_moves.append(get_legal_moves(fen, i))
    return all_moves