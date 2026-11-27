import tkinter as tk
from tkcalendar import Calendar
import datetime
from app.core import Storage
from .dialogs import EventDialog

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Планировщик задач")
        self.geometry("800x600")

        self.current_year = datetime.date.today().year
        self.current_month = datetime.date.today().month
        self.calendar = None
        self.events_list = Storage.load_events()
        self.selected_date_for_menu = None

        self.context_menu = self.init_context_menu()
        self.draw_window()

    def draw_window(self):
        if self.calendar is not None:
            self.calendar.destroy()
            
        self.calendar = Calendar(
            self, 
            selectmode="day", 
            year=self.current_year, 
            month=self.current_month, 
            firstweekday="monday", 
            locale="ru_RU",
            date_pattern="yyyy:mm:dd"
        )
        
        self.calendar._l_month.pack_forget()
        self.calendar._r_month.pack_forget()
        self.calendar._l_year.pack_forget()
        self.calendar._r_year.pack_forget()

        # --- Привязка к каждому дню через _calendar ---
        print(f"DEBUG: _calendar содержит {len(self.calendar._calendar)} строк")
        bound_count = 0
        for week in self.calendar._calendar:
            for day_label in week:
                day_label.bind("<Button-3>", self.draw_context_menu)
                bound_count += 1
        print(f"DEBUG: Привязано событий к {bound_count} ярлыкам")
        # -----------------------------------------------

        prev_month_button = tk.Button(self, text="<", command=self.prev_month)
        next_month_button = tk.Button(self, text=">", command=self.next_month)

        prev_month_button.grid(row=0, column=1, padx=5, pady=5)
        self.calendar.grid(row=0, column=2, rowspan=5, columnspan=5, padx=5, pady=5)
        next_month_button.grid(row=0, column=8, padx=5, pady=5)

    def init_context_menu(self) -> tk.Menu:
        context_menu = tk.Menu(self, tearoff=0)
        context_menu.add_command(label="➕ Добавить событие", command=self.add_event)
        context_menu.add_command(label="✏️ Редактировать", command=self.edit_event)
        context_menu.add_command(label="❌ Удалить", command=self.delete_event)
        return context_menu

    def draw_context_menu(self, event):
        widget = event.widget
        print(f"\n=== DEBUG: ПКМ по виджету: {widget} ===")
        
        # Проверяем, что клик пришелся именно по дню (по числу)
        try:
            text = widget.cget("text")
            print(f"DEBUG: Текст виджета: '{text}'")
            if not text.isdigit():
                print("DEBUG: Это не число (шапка), выходим")
                return
        except Exception as e:
            print(f"DEBUG: Ошибка получения текста: {e}")
            return

        # Симулируем левый клик, чтобы tkcalendar обновил выбор
        try:
            widget.event_generate("<ButtonPress-1>")
            widget.event_generate("<ButtonRelease-1>")
            self.update_idletasks()  # Ждем, пока tkcalendar обновит состояние
            print("DEBUG: Симуляция левого клика выполнена")
        except Exception as e:
            print(f"DEBUG: Ошибка симуляции клика: {e}")

        # get_date() должен вернуть дату нажатого дня
        selected_date = self.calendar.get_date()
        print(f"DEBUG: get_date() вернул: {selected_date}")
        self.selected_date_for_menu = selected_date

        # Проверяем наличие событий
        try:
            has_events = any(e["date"] == selected_date for e in self.events_list)
        except (TypeError, KeyError):
            has_events = any(e.date == selected_date for e in self.events_list)
        print(f"DEBUG: Событий на эту дату: {has_events}")

        if has_events:
            self.context_menu.entryconfig("✏️ Редактировать", state="normal")
            self.context_menu.entryconfig("❌ Удалить", state="normal")
        else:
            self.context_menu.entryconfig("✏️ Редактировать", state="disabled")
            self.context_menu.entryconfig("❌ Удалить", state="disabled")

        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
            print("DEBUG: Меню вызвано!")
        finally:
            self.context_menu.grab_release()

    def prev_month(self):
        self.current_month -= 1
        if self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.draw_window()

    def next_month(self):
        self.current_month += 1
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        self.draw_window()

    def on_event_save(self, new_data, old_data):
        if old_data is None:
            self.events_list.append(new_data)
            Storage.save_events(self.events_list)
        else:
            index = self.events_list.index(old_data)
            self.events_list[index] = new_data

        Storage.save_events(self.events_list)
        self.draw_window()

    def add_event(self):
        print(f"Добавление события на {self.selected_date_for_menu}")
        EventDialog(self, self.on_event_save, "Создание события", self.selected_date_for_menu)

    def edit_event(self):
        print(f"Редактирование события на {self.selected_date_for_menu}")

        events_on_day = [e for e in self.events_list if e["date"] == self.selected_date_for_menu]
        if not events_on_day:
            return

        event_to_edit = events_on_day[0]
        EventDialog(self, self.on_event_save, "Редактирование события", self.selected_date_for_menu, event_data=event_to_edit)

    def delete_event(self):
        print(f"Удаление события на {self.selected_date_for_menu}")

        events_on_day = [e for e in self.events_list if e["date"] == self.selected_date_for_menu]
        if not events_on_day:
            return

        self.events_list.remove(events_on_day[0])
        Storage.save_events(self.events_list)
