import tkinter as tk

# Класс основного окна приложения
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Планировщик задач")
        self.geometry("800x600")
