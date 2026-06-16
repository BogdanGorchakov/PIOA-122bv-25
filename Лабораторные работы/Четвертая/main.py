import json
import csv
import os
import unittest


class Game:
    def __init__(self, game_id, title, genre, year, studio_id):
        self.id = game_id
        self.title = title
        self.genre = genre
        self.year = year
        self.studio_id = studio_id

    def to_dict(self):
        return {"id": self.id, "title": self.title, "genre": self.genre, "year": self.year, "studio_id": self.studio_id}


class FileDatabaseBase:
    def __init__(self, filename):
        self.filename = filename
        self.games = []
        self.current_id = 1
        self.load()

    def load(self):
        pass

    def save(self):
        pass

    def add_game(self, title, genre, year, studio_id):
        if not title or not genre:
            return False
        game = Game(self.current_id, title, genre, year, studio_id)
        self.games.append(game)
        self.current_id += 1
        self.save()
        return True

    def delete_game(self, game_id):
        for i, g in enumerate(self.games):
            if g.id == game_id:
                del self.games[i]
                self.save()
                return True
        return False


class JsonDatabase(FileDatabaseBase):
    def load(self):
        if not os.path.exists(self.filename):
            self.games = []
            return
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.games = [Game(**g) for g in data]
                if self.games:
                    self.current_id = max(g.id for g in self.games) + 1
        except (json.JSONDecodeError, IOError):
            self.games = []

    def save(self):
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump([g.to_dict() for g in self.games], f, ensure_ascii=False, indent=4)
        except IOError:
            print("Ошибка записи в JSON файл!")


class CsvDatabase(FileDatabaseBase):
    def load(self):
        if not os.path.exists(self.filename):
            self.games = []
            return
        try:
            with open(self.filename, 'r', encoding='utf-8', newline='') as f:
                reader = csv.DictReader(f)
                self.games = []
                for row in reader:
                    g = Game(int(row['id']), row['title'], row['genre'], int(row['year']), int(row['studio_id']))
                    self.games.append(g)
                if self.games:
                    self.current_id = max(g.id for g in self.games) + 1
        except (IOError, KeyError, ValueError):
            self.games = []

    def save(self):
        try:
            with open(self.filename, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=["id", "title", "genre", "year", "studio_id"])
                writer.writeheader()
                for g in self.games:
                    writer.writerow(g.to_dict())
        except IOError:
            print("Ошибка записи в CSV файл!")


class ConsoleInterface:
    def __init__(self):
        print("Выберите формат хранения: 1 - JSON (Основное задание), 2 - CSV (Доп. задание)")
        choice = input("Выбор: ").strip()
        if choice == "2":
            self.db = CsvDatabase("database.csv")
            print("Запущена файловая СУБД (Формат: CSV)")
        else:
            self.db = JsonDatabase("database.json")
            print("Запущена файловая СУБД (Формат: JSON)")

    def run(self):
        while True:
            print("\n===== ФАЙЛОВАЯ СУБД (ВЕТКА TASK4) =====")
            print("1. Добавить игру | 2. Показать все игры | 3. Удалить игру | 4. Выйти")
            choice = input("Выберите действие (1-4): ").strip()

            if choice == "1":
                t = input("Название: ").strip()
                g = input("Жанр: ").strip()
                try:
                    y = int(input("Год: "))
                    s = int(input("ID студии: "))
                    if self.db.add_game(t, g, y, s):
                        print("Игра успешно сохранена на диск!")
                    else:
                        print("Ошибка: Заполните поля!")
                except ValueError:
                    print("Ошибка: Год и ID должны быть числами!")
            elif choice == "2":
                print("\nID | Название | Жанр | Год | ID Студии")
                print("-" * 45)
                for game in self.db.games:
                    print(f"{game.id} | {game.title} | {game.genre} | {game.year} | {game.studio_id}")
            elif choice == "3":
                try:
                    idx = int(input("ID для удаления: "))
                    if self.db.delete_game(idx):
                        print("Игра удалена и файл на диске обновлен!")
                    else:
                        print("Игра не найдена!")
                except ValueError:
                    print("Введите числовой ID!")
            elif choice == "4":
                print("Выход.")
                break


class TestFileDatabases(unittest.TestCase):
    def test_json_db(self):
        filename = "test_db.json"
        db = JsonDatabase(filename)
        self.assertTrue(db.add_game("Test JSON", "RPG", 2026, 1))
        self.assertEqual(len(db.games), 1)
        self.assertTrue(db.delete_game(1))
        if os.path.exists(filename): os.remove(filename)

    def test_csv_db(self):
        filename = "test_db.csv"
        db = CsvDatabase(filename)
        self.assertTrue(db.add_game("Test CSV", "Action", 2026, 2))
        self.assertEqual(len(db.games), 1)
        self.assertTrue(db.delete_game(1))
        if os.path.exists(filename): os.remove(filename)


if __name__ == "__main__":
    print("--- Запуск автоматических тестов файловых СУБД ---")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFileDatabases)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if result.wasSuccessful():
        print("\nВсе тесты пройдены! Файловые операции корректны.\n")
        ui = ConsoleInterface()
        ui.run()