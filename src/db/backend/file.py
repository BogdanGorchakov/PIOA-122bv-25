import json
import csv
import os
from typing import List
from src.db.backend.database import Game
from src.db.backend.memory import InMemoryDatabase
from src.db.backend.errors import InvalidStorageDataError, ValidationError


class BaseFileDatabase(InMemoryDatabase):
    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename

    def save(self):
        raise NotImplementedError

    def load(self):
        raise NotImplementedError

    def add_game(self, title: str, genre: str, year: int, studio_id: int) -> bool:
        prev_games = [g.clone() for g in self.games]
        prev_id = self.current_id

        if not super().add_game(title, genre, year, studio_id):
            return False

        try:
            self.save()
            return True
        except Exception:
            self.games = prev_games
            self.current_id = prev_id
            raise

    def delete_game(self, game_id: int) -> bool:
        prev_games = [g.clone() for g in self.games]
        prev_id = self.current_id

        if not super().delete_game(game_id):
            return False

        try:
            self.save()
            return True
        except Exception:
            self.games = prev_games
            self.current_id = prev_id
            raise

    def update_game(self, game_id: int, title: str, genre: str, year: int, studio_id: int) -> bool:
        prev_games = [g.clone() for g in self.games]

        if not super().update_game(game_id, title, genre, year, studio_id):
            return False

        try:
            self.save()
            return True
        except Exception:
            self.games = prev_games
            raise


class JsonDatabase(BaseFileDatabase):
    def __init__(self, filename: str):
        super().__init__(filename)
        self.load()

    def load(self):
        if not os.path.exists(self.filename):
            return

        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            self.games = []
            raise InvalidStorageDataError("Невозможно прочитать JSON файл.") from e

        if not isinstance(data, dict):
            self.games = []
            raise InvalidStorageDataError("Корневой элемент JSON должен быть объектом.")

        if "columns" not in data or "records" not in data:
            self.games = []
            raise InvalidStorageDataError("Отсутствуют обязательные поля columns или records.")

        if data["columns"] != self.columns:
            self.games = []
            raise InvalidStorageDataError("Схема колонок не совпадает с ожидаемой.")

        if not isinstance(data["records"], list):
            self.games = []
            raise InvalidStorageDataError("Поле records должно быть списком.")

        loaded_games: List[Game] = []
        seen_ids = set()

        for idx, row in enumerate(data["records"]):
            if not isinstance(row, list) or len(row) != len(self.columns):
                self.games = []
                raise InvalidStorageDataError(f"Запись #{idx} имеет неверный формат.")

            g_id, title, genre, year, studio_id = row

            if not isinstance(g_id, int) or g_id <= 0 or g_id in seen_ids:
                self.games = []
                raise InvalidStorageDataError(f"Запись #{idx} содержит недопустимый или дублирующийся ID.")

            try:
                game = Game(g_id, title, genre, year, studio_id)
            except (ValidationError, TypeError, ValueError) as err:
                self.games = []
                raise InvalidStorageDataError(f"Запись #{idx} не прошла валидацию.") from err

            seen_ids.add(g_id)
            loaded_games.append(game)

        self.games = loaded_games
        if self.games:
            self.current_id = max(g.id for g in self.games) + 1
        else:
            self.current_id = 1

    def save(self):
        table_structure = {
            "columns": self.columns,
            "records": [[g.id, g.title, g.genre, g.year, g.studio_id] for g in self.games]
        }
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(table_structure, f, ensure_ascii=False, indent=4)


class CsvDatabase(BaseFileDatabase):
    def __init__(self, filename: str):
        super().__init__(filename)
        self.load()

    def load(self):
        if not os.path.exists(self.filename):
            return

        try:
            with open(self.filename, "r", encoding="utf-8", newline="") as f:
                reader = csv.reader(f)
                header = next(reader, None)
                if header is None:
                    return

                if header != self.columns:
                    self.games = []
                    raise InvalidStorageDataError("Заголовок CSV не совпадает со схемой таблицы.")

                loaded_games: List[Game] = []
                seen_ids = set()

                for line_num, row in enumerate(reader, start=2):
                    if len(row) != len(self.columns):
                        self.games = []
                        raise InvalidStorageDataError(
                            f"Повреждённая строка {line_num}: ожидалось {len(self.columns)} полей, получено {len(row)}."
                        )

                    try:
                        g_id = int(row[0])
                        title = str(row[1])
                        genre = str(row[2])
                        year = int(row[3])
                        studio_id = int(row[4])
                    except (ValueError, TypeError) as err:
                        self.games = []
                        raise InvalidStorageDataError(f"Ошибка типов в строке {line_num}.") from err

                    if g_id <= 0 or g_id in seen_ids:
                        self.games = []
                        raise InvalidStorageDataError(f"Недопустимый или дублирующийся ID в строке {line_num}.")

                    try:
                        game = Game(g_id, title, genre, year, studio_id)
                    except (ValidationError, TypeError, ValueError) as err:
                        self.games = []
                        raise InvalidStorageDataError(f"Ошибка валидации данных в строке {line_num}.") from err

                    seen_ids.add(g_id)
                    loaded_games.append(game)

                self.games = loaded_games
                if self.games:
                    self.current_id = max(g.id for g in self.games) + 1
                else:
                    self.current_id = 1
        except OSError as e:
            self.games = []
            raise InvalidStorageDataError("Ошибка при чтении файла CSV.") from e

    def save(self):
        with open(self.filename, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(self.columns)
            for g in self.games:
                writer.writerow([g.id, g.title, g.genre, g.year, g.studio_id])
