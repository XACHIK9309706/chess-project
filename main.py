import tkinter as tk
from ui.tk_ui import ChessUI
from ui.splash import SplashScreen


def create_app(root):
    app = ChessUI(root)


def main():
    root = tk.Tk()
    root.withdraw()

    splash = SplashScreen(root, duration=2000)

    root.after(2000, lambda: [root.deiconify(), create_app(root)])

    root.mainloop()


if __name__ == "__main__":
    main()