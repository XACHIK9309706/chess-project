"""
Модуль tk_ui.py
Графический интерфейс шахматного приложения на tkinter.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from core.board import Board
from core.engine import ChessEngine
from storage.save_manager import SaveManager


class ChessUI:
    def __init__(self, root):
        self.root = root
        self.root.title("♔ Шахматы с ИИ | Python Project")
        self.root.resizable(False, False)
        self.root.configure(bg='#2C3E50')

        # Заголовок
        title_frame = tk.Frame(root, bg='#2C3E50')
        title_frame.pack(pady=5)

        tk.Label(
            title_frame, text="♔ ШАХМАТЫ С ИИ ♚",
            font=("Arial", 18, "bold"), bg='#2C3E50', fg='#ECF0F1'
        ).pack()

        # Состояние игры
        self.board = Board()
        self.difficulty = 'beginner'
        self.engine = ChessEngine(self.difficulty)
        self.save_manager = SaveManager()
        self.current_player = 'white'
        self.selected_cell = None
        self.legal_moves = []
        self.is_game_over = False

        # ВЕРХНЯЯ ПАНЕЛЬ: История ходов (узкая полоса на всю ширину)
        history_frame = tk.Frame(root, bg='#34495E', relief=tk.RAISED, borderwidth=2)
        history_frame.pack(fill=tk.X, padx=15, pady=5)

        tk.Label(
            history_frame, text="📋 История:",
            font=("Arial", 10, "bold"), bg='#34495E', fg='#ECF0F1'
        ).pack(side=tk.LEFT, padx=10)

        self.history_listbox = tk.Listbox(
            history_frame, height=3,
            font=("Courier", 9), bg='#ECF0F1', fg='#2C3E50',
            selectbackground='#3498DB', selectforeground='white',
            relief=tk.SUNKEN, borderwidth=1
        )
        self.history_listbox.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

        scrollbar = tk.Scrollbar(self.history_listbox)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.history_listbox.yview)

        # НИЖНЯЯ ЧАСТЬ: Доска + Управление
        main_frame = tk.Frame(root, bg='#2C3E50')
        main_frame.pack(padx=15, pady=10)

        # ДОСКА (слева)
        board_frame = tk.Frame(main_frame, bg='#34495E', relief=tk.RAISED, borderwidth=3)
        board_frame.pack(side=tk.LEFT, padx=(0, 15))

        self.canvas_size = 480
        self.cell_size = self.canvas_size // 8
        self.canvas = tk.Canvas(
            board_frame, width=self.canvas_size, height=self.canvas_size,
            bg="white", highlightthickness=0
        )
        self.canvas.pack(padx=5, pady=5)

        # УПРАВЛЕНИЕ (справа)
        control_frame = tk.Frame(main_frame, width=200, bg='#34495E', relief=tk.RAISED, borderwidth=3)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)
        control_frame.pack_propagate(False)

        # Статус
        self.status_label = tk.Label(
            control_frame, text="🎯 Ход белых",
            font=("Arial", 11, "bold"), bg='#34495E', fg='#2ECC71', pady=5
        )
        self.status_label.pack(pady=5)

        tk.Frame(control_frame, height=2, bg='#7F8C8D').pack(fill=tk.X, padx=5, pady=3)

        # Сложность
        difficulty_frame = tk.Frame(control_frame, bg='#34495E')
        difficulty_frame.pack(fill=tk.X, padx=5, pady=3)

        tk.Label(
            difficulty_frame, text="🎚️ Сложность:",
            font=("Arial", 9, "bold"), bg='#34495E', fg='#ECF0F1'
        ).pack(anchor=tk.W)

        self.difficulty_var = tk.StringVar(value='Начинающий')
        self.difficulty_combo = ttk.Combobox(
            difficulty_frame,
            textvariable=self.difficulty_var,
            values=['Начинающий', 'Средний', 'Мастер'],
            state='readonly',
            width=12,
            font=("Arial", 8)
        )
        self.difficulty_combo.pack(fill=tk.X, pady=3)
        self.difficulty_combo.bind('<<ComboboxSelected>>', self.on_difficulty_change)

        tk.Frame(control_frame, height=2, bg='#7F8C8D').pack(fill=tk.X, padx=5, pady=3)

        # Кнопки
        button_style = {
            'font': ('Arial', 9, 'bold'), 'pady': 5,
            'relief': tk.RAISED, 'borderwidth': 2, 'cursor': 'hand2'
        }

        tk.Button(control_frame, text="🎮 Новая игра", command=self.new_game,
                  bg='#3498DB', fg='white', **button_style).pack(fill=tk.X, pady=2, padx=5)
        tk.Button(control_frame, text="↩️ Отменить", command=self.undo_move,
                  bg='#9B59B6', fg='white', **button_style).pack(fill=tk.X, pady=2, padx=5)
        tk.Button(control_frame, text="💾 Сохранить", command=self.save_game,
                  bg='#27AE60', fg='white', **button_style).pack(fill=tk.X, pady=2, padx=5)
        tk.Button(control_frame, text="📂 Загрузить", command=self.load_game,
                  bg='#E67E22', fg='white', **button_style).pack(fill=tk.X, pady=2, padx=5)
        tk.Button(control_frame, text="🤝 Ничья", command=self.offer_draw,
                  bg='#F39C12', fg='white', **button_style).pack(fill=tk.X, pady=2, padx=5)

        # Подвал
        tk.Label(
            root, text="Python 3.12 | tkinter | OOP",
            font=("Arial", 8), bg='#2C3E50', fg='#7F8C8D'
        ).pack(pady=5)

        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)

    def draw_board(self):
        """Отрисовка доски, фигур и подсветки ходов."""
        self.canvas.delete("all")

        for r in range(8):
            for c in range(8):
                color = "#F0D9B5" if (r + c) % 2 == 0 else "#B58863"
                if self.selected_cell == (r, c):
                    color = "#7B61FF"

                x1, y1 = c * self.cell_size, r * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

        for r in range(8):
            for c in range(8):
                piece = self.board.get_piece(r, c)
                if piece:
                    x1, y1 = c * self.cell_size, r * self.cell_size
                    self.canvas.create_text(
                        x1 + self.cell_size // 2, y1 + self.cell_size // 2,
                        text=str(piece), font=("Arial", 36), fill="black"
                    )

        for move in self.legal_moves:
            r, c = move
            x1, y1 = c * self.cell_size, r * self.cell_size
            x2, y2 = x1 + self.cell_size, y1 + self.cell_size
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            target_piece = self.board.get_piece(r, c)
            if target_piece:
                self.canvas.create_oval(
                    x1 + 4, y1 + 4, x2 - 4, y2 - 4,
                    outline="#E74C3C", width=4
                )
            else:
                radius = self.cell_size // 6
                self.canvas.create_oval(
                    cx - radius, cy - radius,
                    cx + radius, cy + radius,
                    fill="#27AE60", outline=""
                )

    def update_history_panel(self):
        self.history_listbox.delete(0, tk.END)
        for i, move in enumerate(self.board.get_history()):
            num = (i // 2) + 1
            prefix = f"{num}. " if i % 2 == 0 else ""
            self.history_listbox.insert(tk.END, f"{prefix}{move}")
        self.history_listbox.see(tk.END)

    def on_click(self, event):
        if self.is_game_over:
            return

        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if not (0 <= row < 8 and 0 <= col < 8):
            return

        piece = self.board.get_piece(row, col)

        if self.selected_cell is not None:
            if (row, col) in self.legal_moves:
                from_row, from_col = self.selected_cell
                result = self.board.move_piece(from_row, from_col, row, col)
                self.selected_cell = None
                self.legal_moves = []
                self.draw_board()

                if result['success'] and result['needs_promotion']:
                    self.show_promotion_dialog(
                        result['pawn_row'], result['pawn_col'], result['color']
                    )
                else:
                    self.update_history_panel()
                    self.check_game_status()
                    if self.current_player == 'black':
                        self.root.after(500, self.ai_move)
                return

            if (row, col) == self.selected_cell:
                self.selected_cell = None
                self.legal_moves = []
                self.draw_board()
                return

            if piece and piece.color == self.current_player:
                self.selected_cell = (row, col)
                self.legal_moves = self.board.get_legal_moves_for_piece(piece)
                self.draw_board()
                return

            self.selected_cell = None
            self.legal_moves = []
            self.draw_board()
            return

        if piece and piece.color == self.current_player:
            self.selected_cell = (row, col)
            self.legal_moves = self.board.get_legal_moves_for_piece(piece)
            self.draw_board()

    def show_promotion_dialog(self, row: int, col: int, color: str):
        dialog = tk.Toplevel(self.root)
        dialog.title("Превращение пешки")
        dialog.resizable(False, False)
        dialog.configure(bg='#2C3E50')
        dialog.transient(self.root)
        dialog.grab_set()

        dialog.update_idletasks()
        width = 320
        height = 180
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (width // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")

        tk.Label(
            dialog, text="Выберите фигуру:",
            font=("Arial", 14, "bold"), bg='#2C3E50', fg='#ECF0F1'
        ).pack(pady=15)

        btn_frame = tk.Frame(dialog, bg='#2C3E50')
        btn_frame.pack(pady=10)

        button_style = {
            'font': ('Arial', 28), 'width': 3, 'pady': 5,
            'relief': tk.RAISED, 'borderwidth': 2, 'cursor': 'hand2',
            'bg': '#34495E', 'fg': '#ECF0F1',
            'activebackground': '#3498DB', 'activeforeground': 'white'
        }

        def on_select(piece_type):
            self.board.promote_pawn(row, col, piece_type)
            self.selected_cell = None
            self.legal_moves = []
            self.draw_board()
            self.update_history_panel()
            self.check_game_status()
            dialog.destroy()

            if self.current_player == 'black':
                self.root.after(500, self.ai_move)

        pieces = [('Q', '♕', 'Ферзь'), ('R', '♖', 'Ладья'), ('B', '♗', 'Слон'), ('N', '♘', 'Конь')]
        for piece_type, symbol, name in pieces:
            btn = tk.Button(
                btn_frame, text=symbol,
                command=lambda pt=piece_type: on_select(pt),
                **button_style
            )
            btn.pack(side=tk.LEFT, padx=8)
            btn.bind("<Enter>", lambda e, n=name: dialog.title(f"Выбрать: {n}"))

        dialog.protocol("WM_DELETE_WINDOW", lambda: None)

    def check_game_status(self):
        status = self.board.get_game_status(self.current_player)

        if status == 'checkmate':
            winner = 'Чёрные' if self.current_player == 'white' else 'Белые'
            messagebox.showinfo("Игра окончена", f"🏆 Мат! Победили {winner}.")
            self.is_game_over = True
            return
        elif status == 'stalemate':
            messagebox.showinfo("Игра окончена", "🤝 Пат! Ничья.")
            self.is_game_over = True
            return

        self.current_player = 'black' if self.current_player == 'white' else 'white'

        if status == 'check':
            self.status_label.config(
                text=f"⚠️ ШАХ! Ход {'белых' if self.current_player == 'white' else 'чёрных'}",
                fg='#E74C3C'
            )
        else:
            self.status_label.config(
                text=f"🎯 Ход {'белых' if self.current_player == 'white' else 'чёрных'}",
                fg='#2ECC71'
            )

    def ai_move(self):
        self.status_label.config(text="🤖 ИИ думает...", fg='#F39C12')
        self.root.update()

        best_move = self.engine.get_best_move(self.board, self.current_player)
        if best_move:
            fr, fc, tr, tc = best_move
            result = self.board.move_piece(fr, fc, tr, tc)

            if result['success'] and result['needs_promotion']:
                self.board.promote_pawn(result['pawn_row'], result['pawn_col'], 'Q')

            self.draw_board()
            self.update_history_panel()
            self.check_game_status()
        else:
            messagebox.showinfo("Ошибка", "ИИ не может сделать ход.")

    def new_game(self):
        if messagebox.askyesno("Новая игра", "Начать новую партию? Текущий прогресс будет потерян."):
            self.board = Board()
            self.current_player = 'white'
            self.selected_cell = None
            self.legal_moves = []
            self.is_game_over = False
            self.engine = ChessEngine(self.difficulty)
            self.draw_board()
            self.update_history_panel()
            self.status_label.config(text="🎯 Ход белых", fg='#2ECC71')

    def undo_move(self):
        if self.is_game_over:
            return
        if self.board.undo_move():
            self.current_player = 'black' if self.current_player == 'white' else 'white'
            self.selected_cell = None
            self.legal_moves = []
            self.draw_board()
            self.update_history_panel()
            self.status_label.config(
                text=f"↩️ Ход отменен. Ход {'белых' if self.current_player == 'white' else 'чёрных'}",
                fg='#3498DB'
            )
        else:
            messagebox.showinfo("Отмена", "Нечего отменять — игра только началась.")

    def save_game(self):
        filepath = self.save_manager.save_game(self.board._grid, self.board.get_history())
        messagebox.showinfo("Сохранение", f"✅ Игра успешно сохранена в:\n{filepath}")

    def load_game(self):
        data = self.save_manager.load_game()
        if data is None:
            messagebox.showwarning("Загрузка", "Файл сохранения не найден. Сначала сохраните партию.")
            return

        try:
            self.board.load_from_serialized(data["grid"], data["history"])

            moves_count = len(data["history"])
            self.current_player = 'white' if moves_count % 2 == 0 else 'black'

            self.selected_cell = None
            self.legal_moves = []
            self.is_game_over = False
            self.draw_board()
            self.update_history_panel()

            status_text = f"📂 Партия загружена. Ход {'белых' if self.current_player == 'white' else 'чёрных'}"
            self.status_label.config(text=status_text, fg='#3498DB')

            messagebox.showinfo("Загрузка", "✅ Партия успешно загружена!")
        except Exception as e:
            messagebox.showerror("Ошибка загрузки", f"Не удалось загрузить партию:\n{e}")

    def offer_draw(self):
        if self.is_game_over:
            return

        if messagebox.askyesno("Предложение ничьей",
                               "Вы уверены, что хотите предложить ничью?\n"
                               "(В режиме против ИИ компьютер согласится)"):
            self.is_game_over = True
            self.board._history.append("Ничья (по соглашению)")
            self.update_history_panel()
            self.status_label.config(text="🤝 Ничья!", fg='#F39C12')

            messagebox.showinfo("Игра окончена",
                                "🤝 Соперник принял предложение.\nИгра завершена вничью!")

    def on_difficulty_change(self, event):
        difficulty_map = {
            'Начинающий': 'beginner',
            'Средний': 'intermediate',
            'Мастер': 'master'
        }
        selected_text = self.difficulty_var.get()
        self.difficulty = difficulty_map.get(selected_text, 'beginner')

        self.engine = ChessEngine(self.difficulty)

        self.status_label.config(
            text=f"🎚️ {selected_text}",
            fg='#3498DB'
        )