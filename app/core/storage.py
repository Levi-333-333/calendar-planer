from app.config import FILE_DIRECTORY
import json

class Storage:
    @staticmethod
    def load_events() -> dict:
        with open(FILE_DIRECTORY, 'r', encoding="utf-8") as infile:
            return json.load(infile)

    @staticmethod
    def save_events(events: dict) -> None:
        with open(FILE_DIRECTORY, 'w', encoding="utf-8") as outfile:
            json.dump(events, outfile, indent=4)
