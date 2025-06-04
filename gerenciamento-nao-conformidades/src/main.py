# gerenciamento-nao-conformidades/src/main.py

import tkinter as tk
from gui.interface import AppInterface

def main():
    root = tk.Tk()
    root.title("Gerenciamento de Não Conformidades")
    app = AppInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()