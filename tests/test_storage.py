import json
import unittest
from unittest.mock import patch, mock_open
from app.core.event import Event
from app.core.storage import Storage
from app.config import FILE_PATH


class TestStorage(unittest.TestCase):
    def test_load_events_success(self):
        fake_data = [
            {
                "id": "1",
                "date": "2026:11:22",
                "time": "10:00",
                "title": "Test",
                "priority": "High",
                "is_reminded": False,
            }
        ]
        fake_json = json.dumps(fake_data)

        with patch("builtins.open", mock_open(read_data=fake_json)) as mocked_file:
            result = Storage.load_events("custom_path.json")

            mocked_file.assert_called_once_with("custom_path.json", "r", encoding="utf-8")
            self.assertEqual(result, fake_data)

    def test_load_events_uses_default_file_path(self):
        with patch("builtins.open", mock_open(read_data="[]")) as mocked_file:
            Storage.load_events()
            mocked_file.assert_called_once_with(FILE_PATH, "r", encoding="utf-8")

    def test_load_events_file_not_found(self):
        with patch("builtins.open", side_effect=FileNotFoundError):
            with self.assertRaises(FileNotFoundError):
                Storage.load_events("missing.json")

    def test_load_events_invalid_json(self):
        with patch("builtins.open", mock_open(read_data="{broken json")):
            with self.assertRaises(json.JSONDecodeError):
                Storage.load_events("broken.json")

    def test_save_events_success(self):
        events = [
            Event("2026:11:22", "12:00", "Lunch", id="101", priority="Low", is_reminded=False),
            Event("2026:11:22", "18:00", "Gym", id="102", priority="High", is_reminded=True),
        ]

        m = mock_open()
        with patch("builtins.open", m):
            Storage.save_events(events, "output.json")

            m.assert_called_once_with("output.json", "w", encoding="utf-8")

            handle = m()
            written_data = "".join(call.args[0] for call in handle.write.call_args_list)

            parsed_data = json.loads(written_data)
            self.assertEqual(len(parsed_data), 2)
            self.assertEqual(parsed_data[0]["title"], "Lunch")
            self.assertEqual(parsed_data[1]["id"], "102")

    def test_save_empty_events_list(self):
        m = mock_open()
        with patch("builtins.open", m):
            Storage.save_events([], "empty.json")

            handle = m()
            written_data = "".join(call.args[0] for call in handle.write.call_args_list)
            self.assertEqual(json.loads(written_data), [])

    def test_save_and_load_cyrillic_without_escaping(self):
        events = [
            Event("2026:11:22", "15:00", "Встреча с командой", id="1", priority="Высокий")
        ]

        m = mock_open()
        with patch("builtins.open", m):
            Storage.save_events(events, "cyrillic.json")

            handle = m()
            written_data = "".join(call.args[0] for call in handle.write.call_args_list)

            self.assertIn("Встреча с командой", written_data)
            self.assertIn("Высокий", written_data)
            self.assertNotIn("\\u0412", written_data)

        with patch("builtins.open", mock_open(read_data=written_data)):
            loaded_data = Storage.load_events("cyrillic.json")

            self.assertEqual(loaded_data[0]["title"], "Встреча с командой")
            self.assertEqual(loaded_data[0]["priority"], "Высокий")


if __name__ == "__main__":
    unittest.main()
