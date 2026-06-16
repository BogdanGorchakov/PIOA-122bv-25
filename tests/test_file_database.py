import os
from src.db.backend.file import JsonDatabase, CsvDatabase


def test_json_db():
    filename = "test_db.json"
    db = JsonDatabase(filename)
    assert db.add_game("Test JSON", "RPG", 2026, 1) is True
    assert len(db.games) == 1
    assert db.delete_game(1) is True
    if os.path.exists(filename):
        os.remove(filename)


def test_csv_db():
    filename = "test_db.csv"
    db = CsvDatabase(filename)
    assert db.add_game("Test CSV", "Action", 2026, 2) is True
    assert len(db.games) == 1
    assert db.delete_game(1) is True
    if os.path.exists(filename):
        os.remove(filename)


def test_validation():
    filename = "test_val.json"
    db = JsonDatabase(filename)
    assert db.add_game("", "RPG", 2020, 1) is False
    assert db.add_game("Game", "RPG", 1900, 1) is False
    assert db.add_game("Game", "RPG", 2020, -5) is False
    if os.path.exists(filename):
        os.remove(filename)


def test_filtering():
    filename = "test_filter.json"
    db = JsonDatabase(filename)
    db.add_game("Witcher", "RPG", 2015, 1)
    db.add_game("Doom", "Action", 2016, 2)

    r1 = db.get_games(title="Witcher")
    assert len(r1) == 1

    r2 = db.get_games(genre="Action")
    assert len(r2) == 1

    r3 = db.get_games(year=2020)
    assert len(r3) == 0

    if os.path.exists(filename):
        os.remove(filename)