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
        time = datetime.strptime(self.time, "%H:%M").time()
        if time.minute >= 60:
            raise ValueError("Слишком много минут. Максимум: 59")
        elif time.minute < 0:
            raise ValueError("Минуты не могут быть отрицательными")

        if time.hour > 23:
            raise ValueError("Слишком много часов. Максимум: 23")
        elif time.hour < 0:
            raise ValueError("Часы не могут быть отрицательными")