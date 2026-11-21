from datetime import datetime
from uuid import uuid4

class Event:
    def __init__(self,
                 date: str,
                 time: str,
                 title: str,
                 id: str = None,
                 priority: str = "Medium",
                 is_reminded: bool = False
                 ):
        self.id = id or str(uuid4())
        self.date = date # ГГГГ:ММ:ДД
        self.time = time # ЧЧ:мм
        self.title = title
        self.priority = priority
        self.is_reminded = is_reminded

        self.time_validation()

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, **data):
        return cls(**data)

    def time_validation(self):
        try:
            datetime.strptime(self.time, "%H:%M").time()
        except ValueError:
            raise ValueError("Неверный формат записи времени. Ожидается: 'Часы:Минуты', где 0 <= Часы <= 23 и 0 <= Минуты <= 59")
