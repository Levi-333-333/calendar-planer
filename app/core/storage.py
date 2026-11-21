from app.config import FILE_PATH
from .event import Event
import json

class Storage:
    @staticmethod
    def load_events(file:str = FILE_PATH) -> list:
        with open(file, 'r', encoding="utf-8") as infile:
            return json.load(infile)

    @staticmethod
    def save_events(events: list[Event],
                    file:str = FILE_PATH) -> None:
        with open(file, 'w', encoding="utf-8") as outfile:
            json.dump([event.to_dict() for event in events], outfile, indent=4)
