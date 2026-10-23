import os
import sys
import unittest
from datetime import datetime
from types import SimpleNamespace
from unittest.mock import Mock

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "frontend", "flet", "src"))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from events import EventEditView


class TestEventCreation(unittest.TestCase):
    def setUp(self):
        self.page = Mock()
        self.page.session.get.return_value = SimpleNamespace(id=42, language="en")
        self.db = Mock()

    def test_new_event_form_opens_and_saves(self):
        view = EventEditView(self.page, self.db, Mock(), 0)

        self.assertEqual(view.route, "/eventEdit/0")
        self.assertEqual(view.controls[1].value, "")
        self.assertEqual(view.event_date.value, datetime.now().strftime("%d.%m.%Y"))
        self.assertEqual(view.controls[4].value, "")
        self.db.getEvent.assert_not_called()
        self.db.insertEvent.assert_not_called()

        view.controls[1].value = "  Summer competition  "
        view.event_date.value = "15.06.2027"
        view.controls[4].value = "goldThres = 30"
        view.controls[5].controls[0].on_click(None)

        self.db.insertEvent.assert_called_once_with(
            "Summer competition", 42, datetime(2027, 6, 15), "goldThres = 30"
        )
        self.db.updateEvent.assert_not_called()
        self.page.go.assert_called_once_with("/events")


if __name__ == "__main__":
    unittest.main()
