import json
import csv
import os
from src.db.backend.database import Game
from src.db.backend.memory import InMemoryDatabase
from src.db.backend.errors import InvalidStorageDataError

class JsonDatabase(InMemoryDatabase):
    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename
        self.load()

    def load(self):
        if not os.path.exists(self.filename):
            return
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                records = data.get("records", [])
                self.games = []
                for r in records:
                    g = Game(int(r[0]), str(r[1]), str(r[2]), int(r[3]), int(r[4]))
                    self.games.append(g)
                if self.games:
                    self.current_id = max(g.id for g in self.games) + 1
        except (json.JSONDecodeError, IOError, IndexError, ValueError) as e:
            self.games = []
            raise InvalidStorageDataError("Ошибка при чтении повреждённых данных из JSON файла.") from e

    def save(self):
        try:
            table_structure = {
                "columns": self.columns,
                "records": [[g.id, g.title, g.genre, g.year, g.studio_id] for g in self.games]
            }
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(table_structure, f, ensure_ascii=False, indent=4)
        except IOError:
            print("Ошибка записи в JSON файл!")

    def add_game(self, title, genre, year, studio_id) -> bool:
        success = super().add_game(title, genre, year, studio_id)
        if success:
            self.save()
        return success

    def delete_game(self, game_id) -> bool:
        success = super().delete_game(game_id)
        if success:
            self.save()
        return success

    def update_game(self, game_id, title, genre, year, studio_id) -> bool:
        success = super().update_game(game_id, title, genre, year, studio_id)
        if success:
            self.save()
        return success


class CsvDatabase(InMemoryDatabase):
    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename
        self.load()

    def load(self):
        if not os.path.exists(self.filename):
            return
        try:
            with open(self.filename, 'r', encoding='utf-8', newline='') as f:
                reader = csv.reader(f)
                header = next(reader, None)
                if not header:
                    return
                self.games = []
                for row in reader:
                    if len(row) < 5:
                        continue
                    g = Game(int(row[0]), str(row[1]), str(row[2]), int(row[3]), int(row[4]))
                    self.games.append(g)
                if self.games:
                    self.current_id = max(g.id for g in self.games) + 1
        except (IOError, IndexError, ValueError) as e:
            self.games = []
            raise InvalidStorageDataError("Ошибка при чтении повреждённых данных из CSV файла.") from e

    def save(self):
        try:
            with open(self.filename, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.columns)
                for g in self.games:
                    writer.writerow([g.id, g.title, g.genre, g.year, g.studio_id])
        except IOError:
            print("Ошибка записи в CSV файл!")

    def add_game(self, title, genre, year, studio_id) -> bool:
        success = super().add_game(title, genre, year, studio_id)
        if success:
            self.save()
        return success

    def delete_game(self, game_id) -> bool:
        success = super().delete_game(game_id)
        if success:
            self.save()
        return success

    def update_game(self, game_id, title, genre, year, studio_id) -> bool:
        success = super().update_game(game_id, title, genre, year, studio_id)
        if success:
            self.save()
        return success