"""
Модуль splash.py
Заставка при запуске приложения.
"""
import tkinter as tk


class SplashScreen:
    """Окно заставки, показываемое при запуске."""

    def __init__(self, root, duration=2000):
        self.root = root
        self.duration = duration

        self.splash = tk.Toplevel(root)
        self.splash.title("Загрузка...")
        self.splash.configure(bg='#2C3E50')
        self.splash.resizable(False, False)
        self.splash.overrideredirect(True)

        width = 400
        height = 300
        x = (self.splash.winfo_screenwidth() // 2) - (width // 2)
        y = (self.splash.winfo_screenheight() // 2) - (height // 2)
        self.splash.geometry(f"{width}x{height}+{x}+{y}")

        tk.Label(
            self.splash, text="♔",
            font=("Arial", 80), bg='#2C3E50', fg='#ECF0F1'
        ).pack(pady=20)

        tk.Label(
            self.splash, text="ШАХМАТЫ С ИИ",
            font=("Arial", 18, "bold"), bg='#2C3E50', fg='#ECF0F1'
        ).pack()

        tk.Label(
            self.splash, text="Итоговый проект по ОАП",
            font=("Arial", 10), bg='#2C3E50', fg='#95A5A6'
        ).pack(pady=5)

        tk.Label(
            self.splash, text="Загрузка...",
            font=("Arial", 9), bg='#2C3E50', fg='#3498DB'
        ).pack(pady=30)

        self.root.after(duration, self.close_splash)

    def close_splash(self):
        """Закрывает окно заставки."""
        if hasattr(self, 'splash') and self.splash.winfo_exists():
            self.splash.destroy()