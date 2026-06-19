import os
import sys
import unittest
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "frontend", "flet", "src"))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from live_event import ratingAsRow
from shared.database import Athlete, Gender, Rating, User, Restrictions


class TestLiveEvent(unittest.TestCase):
    def test_rating_row_handles_missing_attendance(self):
        athlete = Athlete(1, "Ada", "Lovelace", 2, "2010-01-01", Gender.FEMALE, 0)
        user = User(2, "trainer", "", "", "Analytical Engines", datetime.now(), datetime.now(), Restrictions.TRAINER, False, False, "", "en")
        rating = Rating(3, datetime.now(), athlete.id, 4, 5, "Floor", 4.0, 5.5)

        row = ratingAsRow(user, athlete, None, None, rating)

        self.assertEqual(row.cells[0].content.value, "Ada Lovelace")
        self.assertEqual(row.cells[1].content.value, "Analytical Engines")
        self.assertEqual(row.cells[2].content.value, "")
        self.assertEqual(row.cells[3].content.value, "Floor")
        self.assertEqual(row.cells[4].content.value, "9.50")


if __name__ == "__main__":
    unittest.main()
