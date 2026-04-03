import unittest

from connect4 import Connect4Game


class Connect4GameTests(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Connect4Game()

    def play_moves(self, columns: list[int]) -> None:
        for column in columns:
            self.game.apply_move(column)

    def test_empty_board_initialization(self) -> None:
        board = self.game.get_board()

        self.assertEqual(len(board), Connect4Game.ROWS)
        self.assertTrue(all(len(row) == Connect4Game.COLUMNS for row in board))
        self.assertTrue(
            all(cell == Connect4Game.EMPTY for row in board for cell in row)
        )
        self.assertEqual(self.game.get_current_player(), Connect4Game.PLAYER_ONE)
        self.assertFalse(self.game.is_terminal())
        self.assertIsNone(self.game.check_winner())
        self.assertEqual(self.game.get_legal_actions(), list(range(Connect4Game.COLUMNS)))

    def test_valid_piece_drop_behavior(self) -> None:
        first_row, first_column = self.game.apply_move(3)
        second_row, second_column = self.game.apply_move(3)
        board = self.game.get_board()

        self.assertEqual((first_row, first_column), (5, 3))
        self.assertEqual((second_row, second_column), (4, 3))
        self.assertEqual(board[5][3], Connect4Game.PLAYER_ONE)
        self.assertEqual(board[4][3], Connect4Game.PLAYER_TWO)
        self.assertTrue(
            all(
                board[row][column] == Connect4Game.EMPTY
                for row in range(Connect4Game.ROWS)
                for column in range(Connect4Game.COLUMNS)
                if (row, column) not in {(5, 3), (4, 3)}
            )
        )

    def test_alternating_turns(self) -> None:
        self.assertEqual(self.game.get_current_player(), Connect4Game.PLAYER_ONE)

        self.game.apply_move(0)
        self.assertEqual(self.game.get_current_player(), Connect4Game.PLAYER_TWO)

        self.game.apply_move(1)
        self.assertEqual(self.game.get_current_player(), Connect4Game.PLAYER_ONE)

    def test_rejecting_moves_in_full_columns(self) -> None:
        for _ in range(Connect4Game.ROWS):
            self.game.apply_move(0)

        board_before = self.game.get_board()
        current_player_before = self.game.get_current_player()

        self.assertNotIn(0, self.game.get_legal_actions())
        with self.assertRaisesRegex(ValueError, "Column is full"):
            self.game.apply_move(0)

        self.assertEqual(self.game.get_board(), board_before)
        self.assertEqual(self.game.get_current_player(), current_player_before)

    def test_horizontal_win_detection(self) -> None:
        self.play_moves([0, 0, 1, 1, 2, 2, 3])

        self.assertEqual(self.game.check_winner(), Connect4Game.PLAYER_ONE)
        self.assertTrue(self.game.is_terminal())
        self.assertFalse(self.game.is_draw())

    def test_vertical_win_detection(self) -> None:
        self.play_moves([0, 1, 0, 1, 0, 1, 0])

        self.assertEqual(self.game.check_winner(), Connect4Game.PLAYER_ONE)
        self.assertTrue(self.game.is_terminal())
        self.assertFalse(self.game.is_draw())

    def test_diagonal_rising_win_detection(self) -> None:
        self.play_moves([0, 1, 1, 2, 4, 2, 2, 3, 4, 3, 5, 3, 3])

        self.assertEqual(self.game.check_winner(), Connect4Game.PLAYER_ONE)
        self.assertTrue(self.game.is_terminal())

    def test_diagonal_falling_win_detection(self) -> None:
        self.play_moves([3, 2, 2, 1, 5, 1, 1, 0, 5, 0, 6, 0, 0])

        self.assertEqual(self.game.check_winner(), Connect4Game.PLAYER_ONE)
        self.assertTrue(self.game.is_terminal())

    def test_draw_detection(self) -> None:
        self.game.board = [
            [2, 2, 1, 1, 2, 2, 0],
            [1, 1, 2, 2, 1, 1, 2],
            [2, 2, 1, 1, 2, 2, 1],
            [1, 1, 2, 2, 1, 1, 2],
            [2, 2, 1, 1, 2, 2, 1],
            [1, 1, 2, 2, 1, 1, 2],
        ]
        self.game.current_player = Connect4Game.PLAYER_ONE
        self.game.terminal = False
        self.game.winner = None
        self.game.last_move = None

        self.game.apply_move(6)

        self.assertTrue(self.game.is_terminal())
        self.assertTrue(self.game.is_draw())
        self.assertIsNone(self.game.check_winner())
        self.assertEqual(self.game.get_legal_actions(), [])

    def test_rejecting_moves_after_terminal_state(self) -> None:
        self.play_moves([0, 0, 1, 1, 2, 2, 3])
        board_before = self.game.get_board()

        with self.assertRaisesRegex(ValueError, "game is over"):
            self.game.apply_move(4)

        self.assertEqual(self.game.get_board(), board_before)

        self.game.reset()
        self.game.board = [
            [2, 2, 1, 1, 2, 2, 0],
            [1, 1, 2, 2, 1, 1, 2],
            [2, 2, 1, 1, 2, 2, 1],
            [1, 1, 2, 2, 1, 1, 2],
            [2, 2, 1, 1, 2, 2, 1],
            [1, 1, 2, 2, 1, 1, 2],
        ]
        self.game.current_player = Connect4Game.PLAYER_ONE
        self.game.terminal = False
        self.game.winner = None
        self.game.last_move = None
        self.game.apply_move(6)
        board_before_draw_rejection = self.game.get_board()

        with self.assertRaisesRegex(ValueError, "game is over"):
            self.game.apply_move(0)

        self.assertEqual(self.game.get_board(), board_before_draw_rejection)

    def test_out_of_bounds_moves_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "out of bounds"):
            self.game.apply_move(-1)

        with self.assertRaisesRegex(ValueError, "out of bounds"):
            self.game.apply_move(Connect4Game.COLUMNS)

        self.assertEqual(self.game.get_board(), Connect4Game().get_board())
        self.assertEqual(self.game.get_current_player(), Connect4Game.PLAYER_ONE)

    def test_reset_behavior(self) -> None:
        self.play_moves([0, 1, 0, 1, 0])
        self.game.reset()

        board = self.game.get_board()
        self.assertTrue(
            all(cell == Connect4Game.EMPTY for row in board for cell in row)
        )
        self.assertEqual(self.game.get_current_player(), Connect4Game.PLAYER_ONE)
        self.assertIsNone(self.game.check_winner())
        self.assertFalse(self.game.is_terminal())
        self.assertEqual(self.game.get_legal_actions(), list(range(Connect4Game.COLUMNS)))

    def test_render_outputs_expected_symbols(self) -> None:
        self.play_moves([0, 1, 0])
        rendered_board = self.game.render().splitlines()

        self.assertEqual(rendered_board[-1], "0 1 2 3 4 5 6")
        self.assertEqual(rendered_board[-2], "X O . . . . .")
        self.assertEqual(rendered_board[-3], "X . . . . . .")


if __name__ == "__main__":
    unittest.main()