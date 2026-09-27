import pytest
from src.db.backend.memory import InMemoryDatabase
from src.db.backend.database import Game
from src.db.backend.errors import ValidationError, TableNotFoundError, TableAlreadyExistsError, MissingColumnError, UnknownColumnError
from src.db.backend import table


def test_errors_and_table_coverage():
    assert issubclass(table.InvalidStorageDataError, Exception)
    assert issubclass(TableNotFoundError, Exception)
    assert issubclass(TableAlreadyExistsError, Exception)
    assert issubclass(MissingColumnError, Exception)
    assert issubclass(UnknownColumnError, Exception)


def test_game_model():
    g = Game(1, "Witcher", "RPG", 2015, 10)
    assert g.id == 1
    assert g.title == "Witcher"
    assert g.to_dict()["year"] == 2015
    assert g == Game(1, "Witcher", "RPG", 2015, 10)
    assert g != "not a game"
    assert g != Game(2, "Witcher", "RPG", 2015, 10)

    clone = g.clone()
    assert clone == g
    assert clone is not g

    with pytest.raises(ValidationError):
        Game(0, "Witcher", "RPG", 2015, 10)

    with pytest.raises(ValidationError):
        Game("1", "Witcher", "RPG", 2015, 10)

    with pytest.raises(ValidationError):
        Game(1, "", "RPG", 2015, 10)

    with pytest.raises(ValidationError):
        Game(1, "Witcher", "", 2015, 10)

    with pytest.raises(ValidationError):
        Game(1, "Witcher", "RPG", 1940, 10)

    with pytest.raises(ValidationError):
        Game(1, "Witcher", "RPG", 2030, 10)

    with pytest.raises(ValidationError):
        Game(1, "Witcher", "RPG", 2015, -1)


def test_add_game():
    db = InMemoryDatabase()
    assert db.add_game("Witcher 3", "RPG", 2015, 1) is True
    assert len(db.games) == 1
    assert db.games[0].title == "Witcher 3"


def test_add_game_validation():
    db = InMemoryDatabase()
    assert db.add_game("Game", "Action", 1900, 1) is False
    assert db.add_game("", "Action", 2020, 1) is False
    assert db.add_game("Game", "", 2020, 1) is False
    assert db.add_game("Game", "Action", 2020, 0) is False
    assert db.add_game("Game", "Action", 2020, -5) is False
    assert len(db.games) == 0


def test_delete_game():
    db = InMemoryDatabase()
    db.add_game("Witcher 3", "RPG", 2015, 1)
    game_id = db.games[0].id

    assert db.delete_game("bad_id") is False
    assert db.delete_game(999) is False
    assert db.delete_game(game_id) is True
    assert len(db.games) == 0


def test_update_game_success():
    db = InMemoryDatabase()
    db.add_game("Old Title", "Action", 2010, 1)
    assert db.update_game(1, "New Title", "RPG", 2015, 2) is True
    assert db.games[0].title == "New Title"
    assert db.games[0].genre == "RPG"
    assert db.games[0].year == 2015
    assert db.games[0].studio_id == 2


def test_update_game_invalid_and_preservation():
    db = InMemoryDatabase()
    db.add_game("Original", "Action", 2010, 1)

    assert db.update_game("bad_id", "New", "Action", 2010, 1) is False
    assert db.update_game(999, "No Game", "Classic", 2020, 1) is False

    assert db.update_game(1, "", "Action", 2010, 1) is False
    assert db.update_game(1, "Original", "", 2010, 1) is False
    assert db.update_game(1, "Original", "Action", 1900, 1) is False
    assert db.update_game(1, "Original", "Action", 2030, 1) is False
    assert db.update_game(1, "Original", "Action", 2010, 0) is False
    assert db.update_game(1, "Original", "Action", 2010, -10) is False

    stored = db.games[0]
    assert stored.title == "Original"
    assert stored.genre == "Action"
    assert stored.year == 2010
    assert stored.studio_id == 1


def test_get_games_filtering_and_immutability():
    db = InMemoryDatabase()
    db.add_game("Cyberpunk 2077", "RPG", 2020, 1)
    db.add_game("GTA V", "Action", 2013, 2)

    all_games = db.get_games()
    assert len(all_games) == 2

    all_games.clear()
    assert len(db.get_games()) == 2

    first_game = db.get_games()[0]
    first_game.title = "Hacked Title"
    assert db.get_games()[0].title == "Cyberpunk 2077"

    rpg_games = db.get_games(genre="RPG")
    assert len(rpg_games) == 1
    assert rpg_games[0].title == "Cyberpunk 2077"

    gta_games = db.get_games(title="gta")
    assert len(gta_games) == 1

    year_2013 = db.get_games(year=2013)
    assert len(year_2013) == 1
    assert year_2013[0].title == "GTA V"

    zero_year = db.get_games(year=0)
    assert zero_year == []

    invalid_year = db.get_games(year="not_a_year")
    assert invalid_year == []
