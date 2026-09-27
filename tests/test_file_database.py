import os
import json
import pytest
from src.db.backend.file import BaseFileDatabase, JsonDatabase, CsvDatabase
from src.db.backend.errors import InvalidStorageDataError


def test_base_file_database_abstract():
    base = BaseFileDatabase("test.db")
    with pytest.raises(NotImplementedError):
        base.save()
    with pytest.raises(NotImplementedError):
        base.load()


def test_json_persistence_across_instances(tmp_path):
    file_path = str(tmp_path / "storage.json")

    db1 = JsonDatabase(file_path)
    assert db1.add_game("Witcher 3", "RPG", 2015, 1) is True

    db2 = JsonDatabase(file_path)
    games = db2.get_games()
    assert len(games) == 1
    assert games[0].id == 1
    assert games[0].title == "Witcher 3"

    assert db2.update_game(1, "Witcher 3: Wild Hunt", "RPG", 2016, 2) is True

    db3 = JsonDatabase(file_path)
    updated_games = db3.get_games()
    assert len(updated_games) == 1
    assert updated_games[0].title == "Witcher 3: Wild Hunt"
    assert updated_games[0].year == 2016
    assert updated_games[0].studio_id == 2

    assert db3.delete_game(1) is True

    db4 = JsonDatabase(file_path)
    assert len(db4.get_games()) == 0


def test_json_validation_failures(tmp_path):
    file_path = str(tmp_path / "val.json")
    db = JsonDatabase(file_path)

    assert db.add_game("", "RPG", 2020, 1) is False
    assert db.add_game("Game", "", 2020, 1) is False
    assert db.add_game("Game", "RPG", 1900, 1) is False
    assert db.add_game("Game", "RPG", 2020, 0) is False
    assert db.update_game(999, "Title", "RPG", 2020, 1) is False
    assert db.delete_game(999) is False


def test_json_corrupted_files(tmp_path):
    file_path = tmp_path / "corrupted.json"

    file_path.write_text("{bad json syntax", encoding="utf-8")
    with pytest.raises(InvalidStorageDataError):
        JsonDatabase(str(file_path))

    file_path.write_text("[]", encoding="utf-8")
    with pytest.raises(InvalidStorageDataError):
        JsonDatabase(str(file_path))

    file_path.write_text(json.dumps({"records": None}), encoding="utf-8")
    with pytest.raises(InvalidStorageDataError):
        JsonDatabase(str(file_path))

    file_path.write_text(json.dumps({}), encoding="utf-8")
    with pytest.raises(InvalidStorageDataError):
        JsonDatabase(str(file_path))

    file_path.write_text(json.dumps({"columns": ["wrong"], "records": []}), encoding="utf-8")
    with pytest.raises(InvalidStorageDataError):
        JsonDatabase(str(file_path))

    bad_schema = {
        "columns": ["id", "title", "genre", "year", "studio_id"],
        "records": [[1, "Only two fields"]]
    }
    file_path.write_text(json.dumps(bad_schema), encoding="utf-8")
    with pytest.raises(InvalidStorageDataError):
        JsonDatabase(str(file_path))

    duplicate_id = {
        "columns": ["id", "title", "genre", "year", "studio_id"],
        "records": [
            [1, "Game 1", "RPG", 2020, 1],
            [1, "Game 2", "Action", 2021, 2]
        ]
    }
    file_path.write_text(json.dumps(duplicate_id), encoding="utf-8")
    with pytest.raises(InvalidStorageDataError):
        JsonDatabase(str(file_path))

    invalid_game_data = {
        "columns": ["id", "title", "genre", "year", "studio_id"],
        "records": [[1, "", "RPG", 2020, 1]]
    }
    file_path.write_text(json.dumps(invalid_game_data), encoding="utf-8")
    with pytest.raises(InvalidStorageDataError):
        JsonDatabase(str(file_path))


def test_json_write_error_and_rollback():
    invalid_path = "/non_existent_folder_abc_123/database.json"
    db = JsonDatabase("dummy.json")
    db.filename = invalid_path

    with pytest.raises(Exception):
        db.add_game("Test", "RPG", 2020, 1)
    assert len(db.games) == 0

    valid_db = JsonDatabase("valid.json")
    valid_db.add_game("Init", "RPG", 2020, 1)
    valid_db.filename = invalid_path

    with pytest.raises(Exception):
        valid_db.update_game(1, "Updated", "RPG", 2021, 2)
    assert valid_db.games[0].title == "Init"

    with pytest.raises(Exception):
        valid_db.delete_game(1)
    assert len(valid_db.games) == 1

    if os.path.exists("dummy.json"):
        os.remove("dummy.json")
    if os.path.exists("valid.json"):
        os.remove("valid.json")


def test_csv_persistence_across_instances(tmp_path):
    file_path = str(tmp_path / "storage.csv")

    db1 = CsvDatabase(file_path)
    assert db1.add_game("Doom", "Action", 2016, 3) is True

    db2 = CsvDatabase(file_path)
    games = db2.get_games()
    assert len(games) == 1
    assert games[0].id == 1
    assert games[0].title == "Doom"

    assert db2.update_game(1, "Doom Eternal", "Action", 2020, 4) is True

    db3 = CsvDatabase(file_path)
    updated = db3.get_games()
    assert len(updated) == 1
    assert updated[0].title == "Doom Eternal"
    assert updated[0].year == 2020

    assert db3.delete_game(1) is True

    db4 = CsvDatabase(file_path)
    assert len(db4.get_games()) == 0


def test_csv_empty_file(tmp_path):
    file_path = tmp_path / "empty.csv"
    file_path.write_text("", encoding="utf-8")
    db = CsvDatabase(str(file_path))
    assert len(db.get_games()) == 0


def test_csv_corrupted_files(tmp_path):
    file_path = tmp_path / "corrupted.csv"

    file_path.write_text("wrong,header,schema\n", encoding="utf-8")
    with pytest.raises(InvalidStorageDataError):
        CsvDatabase(str(file_path))

    file_path.write_text("id,title,genre,year,studio_id\n1,Short row\n", encoding="utf-8")
    with pytest.raises(InvalidStorageDataError):
        CsvDatabase(str(file_path))

    file_path.write_text("id,title,genre,year,studio_id\nnot_int,Title,Genre,2020,1\n", encoding="utf-8")
    with pytest.raises(InvalidStorageDataError):
        CsvDatabase(str(file_path))

    file_path.write_text("id,title,genre,year,studio_id\n1,Title,Genre,2020,1\n1,Title2,Genre,2021,2\n", encoding="utf-8")
    with pytest.raises(InvalidStorageDataError):
        CsvDatabase(str(file_path))

    file_path.write_text("id,title,genre,year,studio_id\n1,,Genre,2020,1\n", encoding="utf-8")
    with pytest.raises(InvalidStorageDataError):
        CsvDatabase(str(file_path))


def test_csv_write_error_and_rollback():
    invalid_path = "/non_existent_folder_abc_123/database.csv"
    db = CsvDatabase("dummy.csv")
    db.filename = invalid_path

    with pytest.raises(Exception):
        db.add_game("Test", "RPG", 2020, 1)
    assert len(db.games) == 0

    valid_db = CsvDatabase("valid.csv")
    valid_db.add_game("Init", "RPG", 2020, 1)
    valid_db.filename = invalid_path

    with pytest.raises(Exception):
        valid_db.update_game(1, "Updated", "RPG", 2021, 2)
    assert valid_db.games[0].title == "Init"

    with pytest.raises(Exception):
        valid_db.delete_game(1)
    assert len(valid_db.games) == 1

    if os.path.exists("dummy.csv"):
        os.remove("dummy.csv")
    if os.path.exists("valid.csv"):
        os.remove("valid.csv")
