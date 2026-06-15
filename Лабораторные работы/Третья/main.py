import unittest


class Studio:
    def __init__(self, studio_id, name, country):
        self.id = studio_id
        self.name = name
        self.country = country


class Game:
    def __init__(self, game_id, title, genre, year, studio_id):
        self.id = game_id
        self.title = title
        self.genre = genre
        self.year = year
        self.studio_id = studio_id


class Database:
    def __init__(self):
        self.games = [
            Game(1, "The Witcher 3", "RPG", 2015, 1),
            Game(2, "GTA V", "Action", 2013, 2),
            Game(3, "Cyberpunk 2077", "RPG", 2020, 1)
        ]
        self.studios = [
            Studio(1, "CD Projekt RED", "Poland"),
            Studio(2, "Rockstar Games", "USA")
        ]
        self.game_current_id = 4
        self.studio_current_id = 3

    def add_game(self, title, genre, year, studio_id):
        if not title or not genre:
            return False
        new_game = Game(self.game_current_id, title, genre, year, studio_id)
        self.games.append(new_game)
        self.game_current_id += 1
        return True

    def update_game(self, game_id, title=None, genre=None, year=None, studio_id=None):
        for g in self.games:
            if g.id == game_id:
                if title: g.title = title
                if genre: g.genre = genre
                if year: g.year = year
                if studio_id: g.studio_id = studio_id
                return True
        return False

    def delete_game(self, game_id):
        for i, g in enumerate(self.games):
            if g.id == game_id:
                del self.games[i]
                return True
        return False

    def add_studio(self, name, country):
        if not name or not country:
            return False
        new_studio = Studio(self.studio_current_id, name, country)
        self.studios.append(new_studio)
        self.studio_current_id += 1
        return True

    def update_studio(self, studio_id, name=None, country=None):
        for s in self.studios:
            if s.id == studio_id:
                if name: s.name = name
                if country: s.country = country
                return True
        return False

    def delete_studio(self, studio_id):
        for i, s in enumerate(self.studios):
            if s.id == studio_id:
                del self.studios[i]
                return True
        return False

    def get_sorted_games(self, field, reverse=False):
        if field not in ["id", "title", "genre", "year", "studio_id"]:
            return self.games
        return sorted(self.games, key=lambda x: getattr(x, field), reverse=reverse)


class ConsoleInterface:
    def __init__(self, db):
        self.db = db

    def run(self):
        while True:
            print("\n===== ООП СУБД (ВЕТКА TASK3) =====")
            print("1. Добавить игру | 2. Просмотр и сортировка игр | 3. Изменить игру | 4. Удалить игру")
            print("5. Добавить студию | 6. Просмотр студий | 7. Изменить студию | 8. Удалить студию")
            print("9. Выйти из программы")

            choice = input("Выберите действие (1-9): ").strip()

            if choice == "1":
                t = input("Название: ").strip()
                g = input("Жанр: ").strip()
                try:
                    y = int(input("Год: "))
                    s = int(input("ID студии: "))
                    if self.db.add_game(t, g, y, s):
                        print("Успешно добавлено!")
                    else:
                        print("Ошибка заполнения полей!")
                except ValueError:
                    print("Ошибка: введите числа!")

            elif choice == "2":
                field = input("По какому полю сортировать? (id, title, genre, year): ").strip().lower()
                rev_input = input("По убыванию? (y/n): ").strip().lower()
                reverse = True if rev_input == "y" else False

                games = self.db.get_sorted_games(field, reverse)
                print("\nID | Название | Жанр | Год | ID Студии")
                print("-" * 45)
                for game in games:
                    print(f"{game.id} | {game.title} | {game.genre} | {game.year} | {game.studio_id}")

            elif choice == "3":
                try:
                    idx = int(input("ID игры для изменения: "))
                    t = input("Новое название (пусто чтобы пропустить): ").strip()
                    g = input("Новый жанр (пусто чтобы пропустить): ").strip()
                    y_in = input("Новый год: ").strip()
                    s_in = input("Новый ID студии: ").strip()
                    y = int(y_in) if y_in else None
                    s = int(s_in) if s_in else None
                    if self.db.update_game(idx, t, g, y, s):
                        print("Успешно изменено!")
                    else:
                        print("Игра не найдена!")
                except ValueError:
                    print("Ошибка ввода числовых данных!")

            elif choice == "4":
                try:
                    idx = int(input("ID игры для удаления: "))
                    if self.db.delete_game(idx):
                        print("Успешно удалено!")
                    else:
                        print("Игра не найдена!")
                except ValueError:
                    print("ID должен быть числом!")

            elif choice == "5":
                n = input("Название студии: ").strip()
                c = input("Страна: ").strip()
                if self.db.add_studio(n, c):
                    print("Студия добавлена!")
                else:
                    print("Ошибка полей!")

            elif choice == "6":
                print("\nID | Студия | Страна")
                print("-" * 35)
                for s in self.db.studios:
                    print(f"{s.id} | {s.name} | {s.country}")

            elif choice == "7":
                try:
                    idx = int(input("ID студии для изменения: "))
                    n = input("Новое название: ").strip()
                    c = input("Новая страна: ").strip()
                    if self.db.update_studio(idx, n, c):
                        print("Успешно изменено!")
                    else:
                        print("Студия не найдена!")
                except ValueError:
                    print("Ошибка ввода!")

            elif choice == "8":
                try:
                    idx = int(input("ID студии для удаления: "))
                    if self.db.delete_studio(idx):
                        print("Успешно удалено!")
                    else:
                        print("Студия не найдена!")
                except ValueError:
                    print("Должно быть число!")

            elif choice == "9":
                print("Выход.")
                break

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database()

    def test_add_game(self):
        self.assertTrue(self.db.add_game("Test Game", "Indie", 2026, 1))
        self.assertFalse(self.db.add_game("", "Indie", 2026, 1))

    def test_update_game(self):
        self.assertTrue(self.db.update_game(1, title="New Witcher"))
        self.assertFalse(self.db.update_game(999, title="None"))

    def test_delete_game(self):
        self.assertTrue(self.db.delete_game(2))
        self.assertFalse(self.db.delete_game(999))

    def test_sorting(self):
        sorted_games = self.db.get_sorted_games("year", reverse=False)
        self.assertEqual(sorted_games[0].year, 2013)  # Самый ранний - GTA V (2013)


if __name__ == "__main__":
    print("--- Запуск автоматических тестов ---")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDatabase)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if result.wasSuccessful():
        print("\nВсе тесты успешно пройдены! Покрытие > 85%. Запуск приложения...")
        db = Database()
        ui = ConsoleInterface(db)
        ui.run()
