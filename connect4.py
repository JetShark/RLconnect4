from __future__ import annotations


class Connect4Game:
    ROWS = 6
    COLUMNS = 7
    EMPTY = 0
    PLAYER_ONE = 1
    PLAYER_TWO = 2

    def __init__(self) -> None:
        self.board: list[list[int]] = []
        self.current_player = self.PLAYER_ONE
        self.terminal = False
        self.winner: int | None = None
        self.last_move: tuple[int, int] | None = None
        self.reset()

    def reset(self) -> list[list[int]]:
        self.board = [
            [self.EMPTY for _ in range(self.COLUMNS)]
            for _ in range(self.ROWS)
        ]
        self.current_player = self.PLAYER_ONE
        self.terminal = False
        self.winner = None
        self.last_move = None
        return self.get_board()

    def get_board(self) -> list[list[int]]:
        return [row.copy() for row in self.board]

    def get_current_player(self) -> int:
        return self.current_player

    def get_legal_actions(self) -> list[int]:
        if self.terminal:
            return []
        return [
            column
            for column in range(self.COLUMNS)
            if self.board[0][column] == self.EMPTY
        ]

    def apply_move(self, column: int) -> tuple[int, int]:
        if self.terminal:
            raise ValueError("Cannot apply a move after the game is over.")
        if not isinstance(column, int):
            raise ValueError("Column must be an integer.")
        if column < 0 or column >= self.COLUMNS:
            raise ValueError("Column is out of bounds.")

        row = self._get_drop_row(column)
        if row is None:
            raise ValueError("Column is full.")

        player = self.current_player
        self._place_piece(row, column, player)
        self.last_move = (row, column)

        if self._check_win_from_position(row, column, player):
            self.winner = player
            self.terminal = True
        elif self._is_board_full():
            self.winner = None
            self.terminal = True
        else:
            self.current_player = self._next_player(player)

        return row, column

    def check_winner(self) -> int | None:
        return self.winner

    def is_draw(self) -> bool:
        return self.terminal and self.winner is None

    def is_terminal(self) -> bool:
        return self.terminal

    def render(self) -> str:
        token_map = {
            self.EMPTY: ".",
            self.PLAYER_ONE: "X",
            self.PLAYER_TWO: "O",
        }
        rows = [" ".join(token_map[cell] for cell in row) for row in self.board]
        rows.append(" ".join(str(column) for column in range(self.COLUMNS)))
        return "\n".join(rows)

    def _is_in_bounds(self, row: int, column: int) -> bool:
        return 0 <= row < self.ROWS and 0 <= column < self.COLUMNS

    def _get_drop_row(self, column: int) -> int | None:
        for row in range(self.ROWS - 1, -1, -1):
            if self.board[row][column] == self.EMPTY:
                return row
        return None

    def _place_piece(self, row: int, column: int, player: int) -> None:
        self.board[row][column] = player

    def _check_direction(
        self,
        row: int,
        column: int,
        row_delta: int,
        column_delta: int,
        player: int,
    ) -> int:
        connected_count = 0
        current_row = row + row_delta
        current_column = column + column_delta

        while self._is_in_bounds(current_row, current_column):
            if self.board[current_row][current_column] != player:
                break
            connected_count += 1
            current_row += row_delta
            current_column += column_delta

        return connected_count

    def _check_win_from_position(self, row: int, column: int, player: int) -> bool:
        directions = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1),
        ]

        for row_delta, column_delta in directions:
            connected_count = 1
            connected_count += self._check_direction(
                row,
                column,
                row_delta,
                column_delta,
                player,
            )
            connected_count += self._check_direction(
                row,
                column,
                -row_delta,
                -column_delta,
                player,
            )
            if connected_count >= 4:
                return True

        return False

    def _is_board_full(self) -> bool:
        return all(self.board[0][column] != self.EMPTY for column in range(self.COLUMNS))

    def _next_player(self, player: int) -> int:
        if player == self.PLAYER_ONE:
            return self.PLAYER_TWO
        return self.PLAYER_ONE