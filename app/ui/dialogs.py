import tkinter as tk

class EventDialog(tk.Toplevel):
    def __init__(self, date: str):
        super().__init__()

        self.title = str()
        self.date = date
        self.time = str()
        self.priority = str()

        
