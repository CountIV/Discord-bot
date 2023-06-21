class Piece:
    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.letter = "?" # Gets replaced in subclass

    # When printing, only show letter
    # White is uppercase, black is lowercase
    def __str__(self):
        if self.color == "w":
            return self.letter
        if self.color == "b":
            return self.letter.lower()

    # How far is current square to destination square
    def coord_distance(self, destination):
        row_distance = destination[0] - self.position[0]
        col_distance = destination[1] - self.position[1]
        return row_distance, col_distance

    # Checks whether there is obstacles in piece's path
    def obstacle_check(self, row, col, game_state):
        for i in range(1, 8):
            current_row = row - i if row > 0 else row + i if row < 0 else row
            current_col = col - i if col > 0 else col + i if col < 0 else col
            check_position = ((self.position[0] + current_row), (self.position[1] + current_col))

            if current_row == 0 and current_col == 0:
                return True
            for piece in game_state.board_pieces:
                if piece.position == check_position:
                    return False

    # Checks whether destination can be moved into
    def destination_check(self, destination, game_state):
        for piece in game_state.board_pieces:
            if piece.position == destination:
                # Doesn't capture ally piece
                if self.color == piece.color:
                    return False
                # Do capture enemy piece
                elif self.color == "w" and piece.color == "b" or self.color == "b" and piece.color == "w":
                    # Pawn doesn't capture if capturing is not on
                    if isinstance(self, Pawn) and self.capturing == False:
                        return False
                    # Returns the piece to be captured
                    return piece
        # Pawn doesn't move to empty position, it is capturing
        if isinstance(self, Pawn) and self.capturing == True:
            # Unless it's legal en passant
            if destination == game_state.en_passant:
                move_direction = 1 if self.color == "w" else -1
                for piece in game_state.board_pieces:
                    if piece.position == (destination[0] + move_direction, destination[1]):
                        # Returns the piece to be captured
                        return piece
            return False
        return None


class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.letter = "R"

    def movement(self, row_distance, col_distance):
        if row_distance == 0 or col_distance == 0:
            return True
        else:
            return False

class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.letter = "B"

    def movement(self, row_distance, col_distance):
        if abs(row_distance) == abs(col_distance):
            return True
        else:
            return False

class Queen(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.letter = "Q"

    def movement(self, row_distance, col_distance):
        if row_distance == 0 or col_distance == 0 or abs(row_distance) == abs(col_distance):
            return True
        else:
            return False

class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.letter = "N"

    def movement(self, row_distance, col_distance):
        if abs(row_distance) == 2 and abs(col_distance) == 1 or abs(row_distance) == 1 and abs(col_distance) == 2:
            return True
        else:
            return False

class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.letter = "K"

    def movement(self, row_distance, col_distance):
        if abs(row_distance) <= 1 and abs(col_distance) <= 1:
            return True
        elif row_distance == 0 and abs(col_distance) == 2:
            return "castling"
        else:
            return False

class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.letter = "P"
        if position[0] == 6 and self.color == "w" or position[0] == 1 and self.color == "b":
            self.first_move = True
        else:
            self.first_move = False
        self.capturing = False

    def movement(self, row_distance, col_distance):
        self.capturing = False
        move_distance = 1
        if self.first_move:
            move_distance = 2

        if self.color == "w":
            if row_distance > 0:
                return False
        elif self.color == "b":
            if row_distance < 0:
                return False

        if abs(col_distance) <= 1 and abs(row_distance) <= move_distance:
            # If pawn moves diagonally
            if abs(row_distance) == 1 and abs(col_distance) == 1:
                self.capturing = True
            if abs(row_distance) != 1 and abs(col_distance) == 1: #TODO
                return False
            return True
        else:
            return False