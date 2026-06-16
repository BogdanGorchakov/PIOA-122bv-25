import json
import csv
import os
from src.models import Game

class InMemoryDatabase:
    def __init__(self):
        self.games = []
        self.current_id = 1
        self.columns = ["id", "title", "genre", "year", "studio_id"]

    def add_game(self, title: str, genre: str, year: int, studio_id: int) -> bool:
        if not title or not genre:
            return False
        if not (1950 <= year <= 2026):
            return False
        if studio_id <= 0:
            return False

        game = Game(self.current_id, title, genre, year, studio_id)
        self.games.append(game)
        self.current_id += 1
        return True

    def delete_game(self, game_id: int) -> bool:
        for i, g in enumerate(self.games):
            if g.id == game_id:
                del self.games[i]
                return True
        return False

    def get_games(self, title=None, genre=None, year=None):
        filtered = self.games
        if title:
            filtered = [g for g in filtered if title.lower() in g.title.lower()]
        if genre:
            filtered = [g for g in filtered if genre.lower() == g.genre.lower()]
        if year:
            filtered = [g for g in filtered if g.year == year]
        return filtered


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
                    g = Game(int(r[0]), r[1], r[2], int(r[3]), int(r[4]))
                    self.games.append(g)
                if self.games:
                    self.current_id = max(g.id for g in self.games) + 1
        except (json.JSONDecodeError, IOError, IndexError, ValueError):
            self.games = []

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
                    g = Game(int(row[0]), row[1], row[2], int(row[3]), int(row[4]))
                    self.games.append(g)
                if self.games:
                    self.current_id = max(g.id for g in self.games) + 1
        except (IOError, IndexError, ValueError):
            self.games = []

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
