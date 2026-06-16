import pytest
from src.db.backend.memory import InMemoryDatabase


def test_add_game():
    db = InMemoryDatabase()
    assert db.add_game("Witcher 3", "RPG", 2015, 1) is True
    assert len(db.games) == 1
    assert db.games[0].title == "Witcher 3"


def test_add_game_validation():
    db = InMemoryDatabase()
    assert db.add_game("Game", "Action", 1900, 1) is False
    assert db.add_game("", "Action", 2020, 1) is False
    assert db.add_game("Game", "Action", 2020, 0) is False


def test_delete_game():
    db = InMemoryDatabase()
    db.add_game("Witcher 3", "RPG", 2015, 1)
    game_id = db.games[0].id

    assert db.delete_game(game_id) is True
    assert len(db.games) == 0
    assert db.delete_game(999) is False


def test_get_games_filtering():
    db = InMemoryDatabase()
    db.add_game("Cyberpunk 2077", "RPG", 2020, 1)
    db.add_game("GTA V", "Action", 2013, 2)

    rpg_games = db.get_games(genre="RPG")
    assert len(rpg_games) == 1
    assert rpg_games[0].title == "Cyberpunk 2077"

    gta_games = db.get_games(title="gta")
    assert len(gta_games) == 1