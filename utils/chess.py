class Piece:
    movement_pattern = [
        (0, 0)
    ]


    @classmethod
    def can_move(cls, old, new):
        # Check if the new move is within bounds
        for i in new:
            if not 0 <= i <= 7:
                return False

        # Get the offset of the new move
        difference = tuple(map(lambda x, y: y - x, old, new))

        if difference in cls.movement_pattern:
            return True

        return False



class King(Piece):
    movement_repeats = False
    movement_pattern = [
        (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)    
    ]



class Queen(Piece):
    movement_repeats = True
    movement_pattern = [
        (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1) 
    ]


class Rook(Piece):
    movement_repeats = True
    movement_pattern = [
        (1, 0), (0, 1), (-1, 0), (0, -1)
    ]



class Bishop(Piece):
    movement_repeats = True
    movement_pattern = [
        (1, 1), (1, -1), (-1, 1), (-1, -1)
    ]



class Knight(Piece):
    movement_repeats = False
    movement_pattern = [
        (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)
    ]



class Pawn(Piece):
    movement_repeats = False
    movement_pattern = [
        (0, 1)
    ]
    attack_pattern = [
        (-1, 1), (1, 1)
    ]


    @classmethod
    def can_move(self, old, new, initial_move=False):
        movement_pattern = [(0, 1), (0, 2)] if initial_move else self.movement_pattern
        # Check if the new move is within bounds
        for i in new:
            if not 0 <= i <= 7:
                return False
        
        # Get the offset of the new move
        difference = tuple(map(lambda x, y: y - x, old, new))

        if difference in movement_pattern:
            return True

        return False