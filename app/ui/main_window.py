import tkinter as tk
from tkcalendar import Calendar
import datetime

# Класс основного окна приложения
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Планировщик задач")
        self.geometry("800x600")

        self.current_year = datetime.date.today().year
        self.current_month = datetime.date.today().month
        self.calendar = None

        self.draw_window()

    def draw_window(self):
        if self.calendar is not None:
            self.calendar.destroy()
        self.calendar = Calendar(self, selectmode="day", year=self.current_year, month=self.current_month, firstweekday="monday", locale="ru_RU")
        self.calendar._l_month.pack_forget()
        self.calendar._r_month.pack_forget()
        self.calendar._l_year.pack_forget()
        self.calendar._r_year.pack_forget()

        prev_month_button = tk.Button(self, text="<", command=self.prev_month)
        prev_month_button.bind("<Button-1>", self.prev_month)

        next_month_button = tk.Button(self, text=">")
        next_month_button.bind("<Button-1>", self.next_month)

        prev_month_button.grid(row=0, column=1, padx=5, pady=5)
        self.calendar.grid(row=0, column=2, rowspan=5, columnspan=5, padx=5, pady=5)
        next_month_button.grid(row=0, column=8, padx=5, pady=5)

    def prev_month(self, event):
        self.current_month -= 1
        if self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.draw_window()

    def next_month(self, event):
        self.current_month += 1
        if self.current_month >= 12:
            self.current_month = 1
            self.current_year += 1
        self.draw_window()
