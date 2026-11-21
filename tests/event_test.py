import unittest
from unittest.mock import patch
from uuid import UUID
from app.core.event import Event

class EventTest(unittest.TestCase):
    def test_invalid_time_raises_value_error(self):
        invalid_times = [
            "1:60",     # минуты > 59
            "1:-5",     # минуты < 0
            "24:47",    # часы > 23
            "-1:47",    # часы < 0
            "12-30",    # неверный разделитель
            "invalid",  # мусорная строка
            "",         # пустая строка
        ]
        for bad_time in invalid_times:
            with self.subTest(time=bad_time):
                with self.assertRaises(ValueError):
                    Event("2026:11:22", bad_time, "Test title")

    def test_boundary_valid_times(self):
        for valid_time in ["0:00", "00:00", "23:59"]:
            with self.subTest(time=valid_time):
                event = Event("2026:11:22", valid_time, "Boundary test")
                self.assertEqual(event.time, valid_time)

    def test_event_correct_creation(self):
        event = Event(
            "2026:11:22",
            "1:49",
            "test_event_correct_creation",
            id="228337",
            priority="McDonalds",
            is_reminded=True,
        )

        self.assertEqual(event.id, "228337")
        self.assertEqual(event.date, "2026:11:22")
        self.assertEqual(event.time, "1:49")
        self.assertEqual(event.title, "test_event_correct_creation")
        self.assertEqual(event.priority, "McDonalds")
        self.assertTrue(event.is_reminded)

    @patch("app.core.event.uuid4")
    def test_event_correct_creation_with_default_values(self, mock_uuid4):
        fake_uuid = UUID("12345678-1234-5678-1234-567812345678")
        mock_uuid4.return_value = fake_uuid

        event = Event("2026:11:22", "1:54", "Default test")

        self.assertEqual(event.id, "12345678-1234-5678-1234-567812345678")
        self.assertEqual(event.priority, "Medium")
        self.assertFalse(event.is_reminded)
        mock_uuid4.assert_called_once()

    def test_to_dict(self):
        event = Event("2026:11:22", "14:30", "Meeting", id="123", priority="High", is_reminded=True)
        expected = {
            "id": "123",
            "date": "2026:11:22",
            "time": "14:30",
            "title": "Meeting",
            "priority": "High",
            "is_reminded": True,
        }
        self.assertEqual(event.to_dict(), expected)

    def test_from_dict_success(self):
        data = {
            "id": "123",
            "date": "2026:11:22",
            "time": "14:30",
            "title": "Meeting",
            "priority": "High",
            "is_reminded": True,
        }
        event = Event.from_dict(**data)

        self.assertIsInstance(event, Event)
        self.assertEqual(event.to_dict(), data)

    def test_from_dict_invalid_time_raises_error(self):
        data = {"date": "2026:11:22", "time": "25:00", "title": "Bad event"}
        with self.assertRaises(ValueError):
            Event.from_dict(**data)
