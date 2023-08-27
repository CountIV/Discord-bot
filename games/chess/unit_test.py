import unittest
import board as board
from game import Game
import pieces as pieces

class tests(unittest.TestCase):
    def test_fen(self):
        # FEN to board works
        fen_game = board.fen_to_game("4n1k1/3R4/8/7K/8/8/8/8 w - - 4 30")
        # Set up Chess state manually
        board_state = [pieces.Knight("b", (0, 4)), pieces.King("b", (0, 6)), pieces.Rook("w", (1, 3)), pieces.King("w", (3, 7))]
        game = Game(board_state, "w", "-", "-", 4, 30)
        # Compare objects
        self.assertEqual(fen_game.board_pieces[0].letter, game.board_pieces[0].letter)
        self.assertEqual(fen_game.board_pieces[1].position, game.board_pieces[1].position)
        self.assertEqual(fen_game.board_pieces[2].color, game.board_pieces[2].color)
        self.assertEqual(fen_game.board_pieces[3].letter, "K")
        self.assertEqual(fen_game.turn, "w")
        self.assertEqual(fen_game.en_passant, game.en_passant)
        self.assertEqual(fen_game.fullmove_number, 30)

        # New board returns correct FEN
        self.assertEqual(board.game_to_fen(Game()), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    def test_validity_check(self):
        game = board.fen_to_game("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        print("Valid moves")
        for piece in game.board_pieces:
            print(piece, piece.position, game.get_valid_moves(piece.position))
        print("")
        print("Valid pieces")
        for piece in game.get_valid_pieces():
            print(piece, piece.position)
        print("")
        print("All valid moves")
        print(game.get_all_moves())
        print("")

        # Castling validity test
        game = board.fen_to_game("4k3/8/8/8/8/8/8/R3K2R w KQ - 1 1")
        for piece in game.board_pieces:
            if isinstance(piece, pieces.King) and piece.color == "w":
                self.assertEqual(game.get_valid_moves(piece.position), [(6, 3), (6, 4), (6, 5), (7, 2), (7, 3), (7, 5), (7, 6)])
        game = board.fen_to_game("4k3/8/8/8/8/8/8/R3K2R b KQ - 1 1")
        for piece in game.board_pieces:
            if isinstance(piece, pieces.King) and piece.color == "b":
                self.assertEqual(game.get_valid_moves(piece.position), [(0, 3), (0, 5), (1, 3), (1, 4), (1, 5)])

        # Check validity test
        game = board.fen_to_game("rnbqkb1r/pppp1Qpp/5n2/4p3/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3")
        print("Valid moves")
        for piece in game.board_pieces:
            print(piece, piece.position, game.get_valid_moves(piece.position))
        print("")
        print("Valid pieces")
        for piece in game.get_valid_pieces():
            print(piece, piece.position)
        print("")


if __name__ == '__main__':
    unittest.main()