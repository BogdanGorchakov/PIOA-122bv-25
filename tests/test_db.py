import unittest
import os
from src.database import JsonDatabase, CsvDatabase


class TestFileDatabases(unittest.TestCase):
    def test_json_db(self):
        filename = "test_db.json"
        db = JsonDatabase(filename)
        self.assertTrue(db.add_game("Test JSON", "RPG", 2026, 1))
        self.assertEqual(len(db.games), 1)
        self.assertTrue(db.delete_game(1))
        if os.path.exists(filename):
            os.remove(filename)

    def test_csv_db(self):
        filename = "test_db.csv"
        db = CsvDatabase(filename)
        self.assertTrue(db.add_game("Test CSV", "Action", 2026, 2))
        self.assertEqual(len(db.games), 1)
        self.assertTrue(db.delete_game(1))
        if os.path.exists(filename):
            os.remove(filename)

    def test_validation(self):
        db = JsonDatabase("test_val.json")
        self.assertFalse(db.add_game("", "RPG", 2020, 1))
        self.assertFalse(db.add_game("Game", "RPG", 1900, 1))
        self.assertFalse(db.add_game("Game", "RPG", 2020, -5))
        if os.path.exists("test_val.json"):
            os.remove("test_val.json")

    def test_filtering(self):
        db = JsonDatabase("test_filter.json")
        db.add_game("Witcher", "RPG", 2015, 1)
        db.add_game("Doom", "Action", 2016, 2)

        r1 = db.get_games(title="Witcher")
        self.assertEqual(len(r1), 1)

        r2 = db.get_games(genre="Action")
        self.assertEqual(len(r2), 1)

        r3 = db.get_games(year=2020)
        self.assertEqual(len(r3), 0)
        if os.path.exists("test_filter.json"):
            os.remove("test_filter.json")


if __name__ == "__main__":
    unittest.main()
