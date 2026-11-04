"""
Модуль pieces.py
Иерархия шахматных фигур с реализацией правил движения.
Демонстрирует: наследование, полиморфизм, инкапсуляцию.
"""


class Piece:
    """Базовый класс для всех шахматных фигур."""

    def __init__(self, color: str, row: int, col: int):
        self._color = color
        self._row = row
        self._col = col
        self._symbol = "?"
        self._value = 0

    @property
    def color(self):
        return self._color

    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col

    @property
    def value(self):
        return self._value

    def move(self, new_row: int, new_col: int):
        self._row = new_row
        self._col = new_col

    def get_valid_moves(self, board) -> list:
        raise NotImplementedError("Метод должен быть переопределён в наследнике")

    def __str__(self):
        return self._symbol


class Pawn(Piece):
    """Пешка."""

    def __init__(self, color: str, row: int, col: int):
        super().__init__(color, row, col)
        self._symbol = '♙' if color == 'white' else '♟'
        self._value = 100
        self._has_moved = False

    def get_valid_moves(self, board) -> list:
        moves = []
        direction = -1 if self._color == 'white' else 1
        start_row = 6 if self._color == 'white' else 1

        if board.is_empty(self._row + direction, self._col):
            moves.append((self._row + direction, self._col))
            if self._row == start_row and board.is_empty(self._row + 2 * direction, self._col):
                moves.append((self._row + 2 * direction, self._col))

        for d_col in [-1, 1]:
            new_row, new_col = self._row + direction, self._col + d_col
            if board.is_valid_position(new_row, new_col):
                target = board.get_piece(new_row, new_col)
                if target and target.color != self._color:
                    moves.append((new_row, new_col))

        return moves


class Rook(Piece):
    """Ладья."""

    def __init__(self, color: str, row: int, col: int):
        super().__init__(color, row, col)
        self._symbol = '♖' if color == 'white' else '♜'
        self._value = 500

    def get_valid_moves(self, board) -> list:
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for d_row, d_col in directions:
            r, c = self._row + d_row, self._col + d_col
            while board.is_valid_position(r, c):
                target = board.get_piece(r, c)
                if target:
                    if target.color != self._color:
                        moves.append((r, c))
                    break
                moves.append((r, c))
                r += d_row
                c += d_col
        return moves


class Knight(Piece):
    """Конь."""

    def __init__(self, color: str, row: int, col: int):
        super().__init__(color, row, col)
        self._symbol = '♘' if color == 'white' else '♞'
        self._value = 320

    def get_valid_moves(self, board) -> list:
        moves = []
        jumps = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                 (1, -2), (1, 2), (2, -1), (2, 1)]
        for d_row, d_col in jumps:
            r, c = self._row + d_row, self._col + d_col
            if board.is_valid_position(r, c):
                target = board.get_piece(r, c)
                if not target or target.color != self._color:
                    moves.append((r, c))
        return moves


class Bishop(Piece):
    """Слон."""

    def __init__(self, color: str, row: int, col: int):
        super().__init__(color, row, col)
        self._symbol = '♗' if color == 'white' else '♝'
        self._value = 330

    def get_valid_moves(self, board) -> list:
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for d_row, d_col in directions:
            r, c = self._row + d_row, self._col + d_col
            while board.is_valid_position(r, c):
                target = board.get_piece(r, c)
                if target:
                    if target.color != self._color:
                        moves.append((r, c))
                    break
                moves.append((r, c))
                r += d_row
                c += d_col
        return moves


class Queen(Piece):
    """Ферзь."""

    def __init__(self, color: str, row: int, col: int):
        super().__init__(color, row, col)
        self._symbol = '♕' if color == 'white' else '♛'
        self._value = 900

    def get_valid_moves(self, board) -> list:
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for d_row, d_col in directions:
            r, c = self._row + d_row, self._col + d_col
            while board.is_valid_position(r, c):
                target = board.get_piece(r, c)
                if target:
                    if target.color != self._color:
                        moves.append((r, c))
                    break
                moves.append((r, c))
                r += d_row
                c += d_col
        return moves


class King(Piece):
    """Король."""

    def __init__(self, color: str, row: int, col: int):
        super().__init__(color, row, col)
        self._symbol = '♔' if color == 'white' else '♚'
        self._value = 20000

    def get_valid_moves(self, board) -> list:
        moves = []
        for d_row in [-1, 0, 1]:
            for d_col in [-1, 0, 1]:
                if d_row == 0 and d_col == 0:
                    continue
                r, c = self._row + d_row, self._col + d_col
                if board.is_valid_position(r, c):
                    target = board.get_piece(r, c)
                    if not target or target.color != self._color:
                        moves.append((r, c))
        return moves