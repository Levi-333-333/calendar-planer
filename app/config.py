from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1] # Найти путь к файлу и отступить на 1 (из папки app в папку-корень)
FILE_PATH = BASE_DIR / "data" / "events.json"
FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
