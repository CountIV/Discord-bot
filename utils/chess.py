class Pawn:
    movement_repeats = False
    movement_pattern = [
        (0, 1)
    ]
    attack_pattern = [
        (-1, 1), (1, 1)
    ]


    def can_move(self, old, new, initial_move=False):
        # Check if the new move is within bounds
        for i in new:
            if not 1 <= i <= 8:
                return False

        if initial_move:
            Pawn.movement_pattern = [
                (0, 1), (0, 2)
            ]
        else:
            Pawn.movement_pattern = [
                (0, 1)
            ]

        # Get the offset of the new move
        difference = tuple(map(lambda x, y: x - y, old, new))

        if difference in Pawn.movement_pattern:
            return True

        return False



class Knight:
    movement_repeats = False
    movement_pattern = [
        (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)
    ]
    attack_pattern = movement_pattern


    def can_move(self, old, new):
        # Check if the new move is within bounds
        for i in new:
            if not 1 <= i <= 8:
                return False

        # Get the offset of the new move
        difference = tuple(map(lambda x, y: x - y, old, new))

        if difference in Knight.movement_pattern:
            return True

        return False