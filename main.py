import tkinter as tk
from app_controller import AppController
from gui_view import GUIView

def main():
    controller = AppController()
    root = tk.Tk()
    app = GUIView(root, controller)
    root.mainloop()

if __name__ == "__main__":
    main()