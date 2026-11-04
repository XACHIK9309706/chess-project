"""
Модуль save_manager.py
Сохранение и загрузка партий в формате JSON.
Демонстрирует работу со стандартным модулем json (Лекция 3).
"""
import json
import os


# Маппинг: код фигуры ↔ класс
# Важно: N = Knight (конь), K = King (король) — разные буквы!
PIECE_CODES = {
    'P': 'Pawn',
    'R': 'Rook',
    'N': 'Knight',
    'B': 'Bishop',
    'Q': 'Queen',
    'K': 'King',
}

CODE_TO_PIECE = {v: k for k, v in PIECE_CODES.items()}


class SaveManager:
    """Менеджер сохранений шахматных партий."""

    def __init__(self, save_dir="saves"):
        self._save_dir = save_dir
        if not os.path.exists(self._save_dir):
            os.makedirs(self._save_dir)

    def save_game(self, board_state: list, history: list, filename: str = "last_save.json"):
        """Сохраняет состояние доски и историю в JSON файл."""
        serializable_grid = []
        for row in board_state:
            serializable_row = []
            for piece in row:
                if piece:
                    color_code = 'w' if piece.color == 'white' else 'b'
                    # Используем правильный код из маппинга
                    type_name = type(piece).__name__
                    type_code = CODE_TO_PIECE.get(type_name, '?')
                    serializable_row.append(f"{color_code}{type_code}")
                else:
                    serializable_row.append(None)
            serializable_grid.append(serializable_row)

        data = {
            "grid": serializable_grid,
            "history": history
        }

        filepath = os.path.join(self._save_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return filepath

    def load_game(self, filename: str = "last_save.json"):
        """Загружает состояние доски и историю из JSON файла."""
        filepath = os.path.join(self._save_dir, filename)
        if not os.path.exists(filepath):
            return None

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data