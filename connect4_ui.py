# UI Class
# This class handles displaying the interface which the user will use to interact with the Connect 4 game

import tkinter as tk

class Connect4UI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Connect 4")
        self.root.geometry("700x600")
        self.root.mainloop()

ui = Connect4UI()
