import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from app.core import Event

class EventDialog(tk.Toplevel):
    def __init__(self,
                 parent: tk.Tk,
                 callback,
                 title: str,
                 date: str,
                 event_data: dict = None):
        super().__init__(parent)
        self.title(title)
        self.geometry("300x200")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.date = date
        self.callback = callback
        self.event_data = event_data # None для добавление, dict для редактирования

        self.draw_window()
        if self.event_data:
            self.fill_data()

    def draw_window(self):
        # Дата
        ttk.Label(self, text="Дата:").grid(row=0, column=0, sticky='w', padx=15, pady=(15, 5))
        self.date_label = ttk.Label(self, text=self.date, font=("Arial", 10, "bold"))
        self.date_label.grid(row=0, column=1, sticky="w", padx=15, pady=(15, 5))

        # Название
        ttk.Label(self, text="Название события:").grid(row=1, column=0, sticky='w', padx=15, pady=5)
        self.name_entry = ttk.Entry(self, width=30)
        self.name_entry.grid(row=1, column=1, sticky='w', padx=15, pady=5)

        # Время
        ttk.Label(self, text="Время (ЧЧ:ММ):").grid(row=2, column=0, sticky='w', padx=15, pady=5)
        time_frame = ttk.Frame(self)
        time_frame.grid(row=2, column=1, sticky='w', padx=15, pady=5)

        self.hour_spin = ttk.Spinbox(time_frame, from_=0, to=23, width=3, format="%02.0f")
        self.hour_spin.pack(side=tk.LEFT)
        self.hour_spin.set("12")

        ttk.Label(time_frame, text=" : ").pack(side=tk.LEFT)

        self.minute_spin = ttk.Spinbox(time_frame, from_=0, to=59, width=3, format="%02.0f")
        self.minute_spin.pack(side=tk.LEFT)
        self.minute_spin.set("00")

        # Приоритет
        ttk.Label(self, text="Приоритет:").grid(row=3, column=0, sticky='w', padx=15, pady=5)
        self.priority_combo = ttk.Combobox(self, values=["Low", "Medium", "High"], state="readonly")
        self.priority_combo.grid(row=3, column=1, sticky='w', padx=15, pady=5)

        # Кнопки
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=4, column=0, sticky='w', columnspan=2, pady=20)

        ttk.Button(btn_frame, text="Сохранить", command=self.save).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Отмена", command=self.destroy).pack(side=tk.LEFT, padx=10)

    def fill_data(self):
        self.name_entry.insert(0, self.event_data["title"])
        self.hour_spin.set(self.event_data["time"][:2])
        self.minute_spin.set(self.event_data["time"][3:])
        self.priority_combo.set(self.event_data["priority"])

    def save(self) -> None:
        id = self.event_data["id"] if self.event_data is not None else None

        if (name := self.name_entry.get().strip()) == "":
            messagebox.showerror("Ошибка", "Название события не может быть пустым", parent=self)
            return

        try:
            h = int(self.hour_spin.get())
            m = int(self.minute_spin.get())
            if not (0 <= h <= 23 and 0 <= m <= 59):
                raise ValueError("Время вне диапозона")
        except ValueError:
            messagebox.showerror("Ошибка", "Время вне диапозона или введено некореектно", parent=self)
            return

        time_str = f"{h:02d}:{m:02d}"
        priority = self.priority_combo.get()

        result = Event(self.date, time_str, name, id=id, priority=priority).to_dict()

        self.callback(result, self.event_data)
        self.destroy()
