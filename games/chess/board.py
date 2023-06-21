from input_converter import coordinate_converter
from game import Chess
import pieces as pieces

def display(board_pieces):
    # Generate an empty board
    board = []
    for i in range(8):
        board.append([])
        for _ in range(8):
            board[i].append("o")

    # Put pieces on the board
    for piece in board_pieces:
        row, col = piece.position
        board[row][col] = str(piece)

    # Prints letter on top of the board
    print("  A  B  C  D  E  F  G  H")

    # Prints numbers on the side of the board
    # There is two spaces between every piece
    coord_num = 8
    row_display = ""
    for row in board:
        row_display += str(coord_num)
        for square in row:
            row_display += " " + square + " "
        row_display += str(coord_num)
        coord_num -= 1
        if coord_num != 0:
            row_display += "\n"
        
    print(row_display)

    # Prints letter on top of the board
    print("  A  B  C  D  E  F  G  H")


# Shows Python coordinates instead of chess system
def dev_display(board_pieces):
    # Generate an empty board
    board = []
    for i in range(8):
        board.append([])
        for _ in range(8):
            board[i].append("o")

    # Put pieces on the board
    for piece in board_pieces:
        row, col = piece.position
        board[row][col] = str(piece)

    # Prints letter on top of the board
    print("  0  1  2  3  4  5  6  7")

    # Prints numbers on the side of the board
    # There is two spaces between every piece
    coord_num = 0
    row_display = ""
    for row in board:
        row_display += str(coord_num)
        for square in row:
            row_display += " " + square + " "
        row_display += str(coord_num)
        coord_num += 1
        if coord_num != 8:
            row_display += "\n"
        
    print(row_display)

    # Prints letter on top of the board
    print("  0  1  2  3  4  5  6  7")


def game_to_fen(game):
    # Generate an empty board
    board = []
    for i in range(8):
        board.append([])
        for _ in range(8):
            board[i].append("o")

    # Put pieces on the board
    for piece in game.board_pieces:
        row, col = piece.position
        board[row][col] = str(piece)
    
    # Create FEN from the board
    fen_str = ""
    # Board pieces
    loop = 0
    for row in board:
        loop += 1
        fen_number = 0
        for square in row:
            if square == "o":
                fen_number += 1
            else:
                if fen_number != 0:
                    fen_str += str(fen_number)
                    fen_number = 0
                fen_str += square
        if fen_number != 0:
            fen_str += str(fen_number)
        if loop != 8:
            fen_str += "/"
    # Turn
    fen_str += " " + game.turn
    # Castling rights
    castling = "".join(game.castling)
    fen_str += " " + (castling if castling != "" else "-")
    # Possible en passant targets
    en_passant = game.en_passant if game.en_passant == "-" else coordinate_converter(game.en_passant)
    fen_str += " " + en_passant
    # Halfmove clock and fullmove counter
    fen_str += " " + str(game.halfmove_clock)
    fen_str += " " + str(game.fullmove_number)

    return fen_str

def fen_to_game(fen):
    fen_list = fen.split()
    fen_board = fen_list[0].split("/")
    board = []

    count = 0
    for row in fen_board:
        for char in row:
            if char.isdigit():
                count += int(char)
            else:
                coords = (int(count / 8), count % 8)
                board.append(create_piece(char, coords))
                count += 1

    turn = fen_list[1]
    castling = [char for char in fen_list[2]]
    en_passant = fen_list[3]
    halfmove_clock = int(fen_list[4])
    fullmove_number = int(fen_list[5])

    return Chess(board_pieces=board, turn=turn, castling=castling, en_passant=en_passant, halfmove_clock=halfmove_clock, fullmove_number=fullmove_number)

def create_piece(letter, coords):
    if letter == "P":
        return pieces.Pawn("w", coords)
    elif letter == "p":
        return pieces.Pawn("b", coords)
    elif letter == "R":
        return pieces.Rook("w", coords)
    elif letter == "r":
        return pieces.Rook("b", coords)
    elif letter == "N":
        return pieces.Knight("w", coords)
    elif letter == "n":
        return pieces.Knight("b", coords)
    elif letter == "B":
        return pieces.Bishop("w", coords)
    elif letter == "b":
        return pieces.Bishop("b", coords)
    elif letter == "K":
        return pieces.King("w", coords)
    elif letter == "k":
        return pieces.King("b", coords)
    elif letter == "Q":
        return pieces.Queen("w", coords)
    elif letter == "q":
        return pieces.Queen("b", coords)
    else:
        print(ValueError)