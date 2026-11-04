"""
Модуль board.py
Управление шахматной доской 8x8.
Отвечает за состояние игры, генерацию ходов и проверку правил.
Демонстрирует принцип модульности и композиции.
"""
import copy
from .pieces import Pawn, Rook, Knight, Bishop, Queen, King


class Board:
    """Шахматная доска (матрица 8x8)."""

    def __init__(self):
        self._grid = [[None for _ in range(8)] for _ in range(8)]
        self._setup_initial_position()
        self._state_stack = []  # Стек для отмены ходов
        self._history = []      # История ходов

    def _setup_initial_position(self):
        """Начальная расстановка фигур."""
        for col in range(8):
            self._grid[6][col] = Pawn('white', 6, col)
            self._grid[1][col] = Pawn('black', 1, col)

        self._grid[7][0] = Rook('white', 7, 0)
        self._grid[7][7] = Rook('white', 7, 7)
        self._grid[0][0] = Rook('black', 0, 0)
        self._grid[0][7] = Rook('black', 0, 7)

        self._grid[7][1] = Knight('white', 7, 1)
        self._grid[7][6] = Knight('white', 7, 6)
        self._grid[0][1] = Knight('black', 0, 1)
        self._grid[0][6] = Knight('black', 0, 6)

        self._grid[7][2] = Bishop('white', 7, 2)
        self._grid[7][5] = Bishop('white', 7, 5)
        self._grid[0][2] = Bishop('black', 0, 2)
        self._grid[0][5] = Bishop('black', 0, 5)

        self._grid[7][3] = Queen('white', 7, 3)
        self._grid[0][3] = Queen('black', 0, 3)

        self._grid[7][4] = King('white', 7, 4)
        self._grid[0][4] = King('black', 0, 4)

    def is_valid_position(self, row: int, col: int) -> bool:
        return 0 <= row < 8 and 0 <= col < 8

    def is_empty(self, row: int, col: int) -> bool:
        if self.is_valid_position(row, col):
            return self._grid[row][col] is None
        return False

    def get_piece(self, row: int, col: int):
        if self.is_valid_position(row, col):
            return self._grid[row][col]
        return None

    def get_legal_moves_for_piece(self, piece) -> list:
        """
        АЛГОРИТМИЧЕСКАЯ ЗАДАЧА №2: Генерация и валидация легальных ходов.
        Фильтрует псевдолегальные ходы, оставляя только те, после которых
        король не оказывается под шахом.
        """
        pseudo_moves = piece.get_valid_moves(self)
        legal_moves = []

        for move in pseudo_moves:
            to_row, to_col = move
            original_target = self._grid[to_row][to_col]
            original_piece_row, original_piece_col = piece.row, piece.col

            # Симуляция хода
            self._grid[to_row][to_col] = piece
            self._grid[original_piece_row][original_piece_col] = None
            piece._row, piece._col = to_row, to_col

            if not self.is_king_in_check(piece.color):
                legal_moves.append(move)

            # Откат симуляции
            self._grid[original_piece_row][original_piece_col] = piece
            self._grid[to_row][to_col] = original_target
            piece._row, piece._col = original_piece_row, original_piece_col

        return legal_moves

    def is_king_in_check(self, color: str) -> bool:
        """Проверяет, находится ли король под атакой."""
        king_pos = None
        for r in range(8):
            for c in range(8):
                p = self._grid[r][c]
                if isinstance(p, King) and p.color == color:
                    king_pos = (r, c)
                    break
            if king_pos:
                break

        if not king_pos:
            return False

        opponent_color = 'black' if color == 'white' else 'white'
        for r in range(8):
            for c in range(8):
                piece = self._grid[r][c]
                if piece and piece.color == opponent_color:
                    if king_pos in piece.get_valid_moves(self):
                        return True
        return False

    def has_legal_moves(self, color: str) -> bool:
        for r in range(8):
            for c in range(8):
                piece = self._grid[r][c]
                if piece and piece.color == color:
                    if self.get_legal_moves_for_piece(piece):
                        return True
        return False

    def get_game_status(self, current_color: str) -> str:
        in_check = self.is_king_in_check(current_color)
        has_moves = self.has_legal_moves(current_color)

        if in_check and not has_moves:
            return 'checkmate'
        elif not in_check and not has_moves:
            return 'stalemate'
        elif in_check:
            return 'check'
        return 'playing'

    def move_piece(self, from_row: int, from_col: int, to_row: int, to_col: int) -> dict:
        """
        Выполняет ход. Возвращает словарь с результатом:
        {
            'success': bool,
            'needs_promotion': bool,
            'pawn_row': int,
            'pawn_col': int,
            'color': str
        }
        """
        piece = self.get_piece(from_row, from_col)
        if not piece:
            return {'success': False, 'needs_promotion': False}

        legal_moves = self.get_legal_moves_for_piece(piece)
        if (to_row, to_col) not in legal_moves:
            return {'success': False, 'needs_promotion': False}

        # Сохраняем состояние в стек
        self._state_stack.append(copy.deepcopy(self._grid))

        # Выполняем ход
        self._grid[to_row][to_col] = piece
        self._grid[from_row][from_col] = None
        piece.move(to_row, to_col)

        # Запись в историю
        cols = "abcdefgh"
        move_text = f"{cols[from_col]}{8-from_row} -> {cols[to_col]}{8-to_row}"
        self._history.append(move_text)

        # Проверяем превращение пешки
        needs_promotion = False
        if isinstance(piece, Pawn):
            if (piece.color == 'white' and to_row == 0) or \
               (piece.color == 'black' and to_row == 7):
                needs_promotion = True

        return {
            'success': True,
            'needs_promotion': needs_promotion,
            'pawn_row': to_row,
            'pawn_col': to_col,
            'color': piece.color
        }

    def promote_pawn(self, row: int, col: int, piece_type: str):
        """
        Заменяет пешку на выбранную фигуру (ферзь/ладья/слон/конь).
        piece_type: 'Q', 'R', 'B', 'N'
        """
        piece_classes = {
            'Q': Queen,
            'R': Rook,
            'B': Bishop,
            'N': Knight,
        }
        pawn = self._grid[row][col]
        if not isinstance(pawn, Pawn):
            return False

        color = pawn.color
        new_piece = piece_classes[piece_type](color, row, col)
        self._grid[row][col] = new_piece

        cols = "abcdefgh"
        self._history.append(f"  = {piece_type} ({cols[col]}{8-row})")
        return True

    def undo_move(self) -> bool:
        if self._state_stack:
            self._grid = self._state_stack.pop()
            if self._history:
                self._history.pop()
            return True
        return False

    def get_history(self) -> list:
        return self._history

    def load_from_serialized(self, grid_data: list, history: list):
        """Загружает состояние доски из сериализованных данных."""
        piece_classes = {
            'P': Pawn,
            'R': Rook,
            'N': Knight,
            'B': Bishop,
            'Q': Queen,
            'K': King,
        }

        self._grid = [[None for _ in range(8)] for _ in range(8)]
        self._state_stack = []
        self._history = list(history)

        for r in range(8):
            for c in range(8):
                code = grid_data[r][c]
                if code is None:
                    continue

                color_code = code[0]
                type_code = code[1]

                color = 'white' if color_code == 'w' else 'black'
                piece_class = piece_classes.get(type_code)

                if piece_class:
                    self._grid[r][c] = piece_class(color, r, c)

    def display(self):
        print("\n  a b c d e f g h")
        for r in range(8):
            row_str = f"{8-r} "
            for c in range(8):
                piece = self._grid[r][c]
                row_str += (str(piece) if piece else ".") + " "
            print(row_str + f"{8-r}")
        print("  a b c d e f g h\n")