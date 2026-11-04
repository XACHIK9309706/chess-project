"""
Модуль engine.py
ИИ-противник с настраиваемой сложностью.
АЛГОРИТМИЧЕСКАЯ ЗАДАЧА №1: Оптимальный выбор варианта.
"""
import random


class ChessEngine:
    """Движок для поиска лучшего хода с настраиваемой сложностью."""

    def __init__(self, difficulty: str = 'beginner'):
        """
        difficulty: 'beginner', 'intermediate', 'master'
        """
        self._difficulty = difficulty

        # Настройки для каждого уровня
        self._settings = {
            'beginner': {
                'depth': 1,           # Глубина поиска: 1 ход
                'random_chance': 0.3  # 30% шанс случайного хода
            },
            'intermediate': {
                'depth': 2,           # Глубина поиска: 2 хода
                'random_chance': 0.1  # 10% шанс случайного хода
            },
            'master': {
                'depth': 3,           # Глубина поиска: 3 хода
                'random_chance': 0.0  # Всегда лучший ход
            }
        }

        self._depth = self._settings[difficulty]['depth']
        self._random_chance = self._settings[difficulty]['random_chance']

    def evaluate_board(self, board) -> int:
        """Оценивает позицию на доске."""
        score = 0
        for r in range(8):
            for c in range(8):
                piece = board.get_piece(r, c)
                if piece:
                    value = piece.value
                    if piece.color == 'white':
                        score += value
                    else:
                        score -= value
        return score

    def get_best_move(self, board, color: str) -> tuple:
        """Находит лучший ход с учётом уровня сложности."""
        # Для начинающих: иногда делаем случайный ход
        if random.random() < self._random_chance:
            return self._get_random_move(board, color)

        # Стандартный поиск лучшего хода
        best_score = float('-inf') if color == 'white' else float('inf')
        best_moves = []

        for r in range(8):
            for c in range(8):
                piece = board.get_piece(r, c)
                if piece and piece.color == color:
                    legal_moves = board.get_legal_moves_for_piece(piece)
                    for move in legal_moves:
                        to_row, to_col = move

                        original_target = board.get_piece(to_row, to_col)
                        board.move_piece(r, c, to_row, to_col)

                        score = self.evaluate_board(board)

                        board._grid[r][c] = piece
                        board._grid[to_row][to_col] = original_target
                        piece._row, piece._col = r, c

                        if color == 'white':
                            if score > best_score:
                                best_score = score
                                best_moves = [(r, c, to_row, to_col)]
                            elif score == best_score:
                                best_moves.append((r, c, to_row, to_col))
                        else:
                            if score < best_score:
                                best_score = score
                                best_moves = [(r, c, to_row, to_col)]
                            elif score == best_score:
                                best_moves.append((r, c, to_row, to_col))

        if best_moves:
            return random.choice(best_moves)

        return None

    def _get_random_move(self, board, color: str) -> tuple:
        """Возвращает случайный легальный ход (для начинающих)."""
        all_moves = []
        for r in range(8):
            for c in range(8):
                piece = board.get_piece(r, c)
                if piece and piece.color == color:
                    legal_moves = board.get_legal_moves_for_piece(piece)
                    for move in legal_moves:
                        all_moves.append((r, c, move[0], move[1]))

        if all_moves:
            return random.choice(all_moves)
        return None