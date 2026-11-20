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

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, **data):
        return cls(**data)