from src.db.backend.file import JsonDatabase, CsvDatabase

class ConsoleInterface:
    def __init__(self):
        print("Выберите формат хранения: 1 - JSON, 2 - CSV")
        choice = input("Выбор: ").strip()
        if choice == "2":
            self.db = CsvDatabase("database.csv")
            print("Запущена СУБД (Формат: CSV)")
        else:
            self.db = JsonDatabase("database.json")
            print("Запущена СУБД (Формат: JSON)")

    def run(self):
        while True:
            print("\n===== СУБД =====")
            print("1. Добавить игру")
            print("2. Показать все игры")
            print("3. Поиск и фильтрация")
            print("4. Удалить игру")
            print("5. Обновить данные игры")
            print("6. Выйти")
            choice = input("Выберите действие (1-6): ").strip()

            if choice == "1":
                t = input("Название: ").strip()
                g = input("Жанр: ").strip()
                try:
                    y = int(input("Год: "))
                    s = int(input("ID студии: "))
                    if self.db.add_game(t, g, y, s):
                        print("Игра успешно сохранена!")
                    else:
                        print("Ошибка валидации данных!")
                except ValueError:
                    print("Ошибка: Год и ID должны быть числами!")
            elif choice == "2":
                games = self.db.get_games()
                self._print_list(games)
            elif choice == "3":
                print("\n--- Фильтрация (Оставьте пустым, если фильтр не нужен) ---")
                st = input("Поиск по названию: ").strip() or None
                sg = input("Поиск по жанру: ").strip() or None
                sy_raw = input("Поиск по году: ").strip()
                sy = int(sy_raw) if sy_raw.isdigit() else None

                games = self.db.get_games(title=st, genre=sg, year=sy)
                self._print_list(games)
            elif choice == "4":
                try:
                    idx = int(input("ID для удаления: "))
                    if self.db.delete_game(idx):
                        print("Игра удалена!")
                    else:
                        print("Игра не найдена!")
                except ValueError:
                    print("Введите числовой ID!")
            elif choice == "5":
                try:
                    idx = int(input("ID игры для обновления: "))
                    t = input("Новое название: ").strip()
                    g = input("Новый жанр: ").strip()
                    y = int(input("Новый год: "))
                    s = int(input("Новый ID студии: "))
                    if self.db.update_game(idx, t, g, y, s):
                        print("Данные игры успешно обновлены!")
                    else:
                        print("Ошибка обновления! Проверьте ID и валидность данных.")
                except ValueError:
                    print("Ошибка ввода чисел!")
            elif choice == "6":
                print("Выход.")
                break

    def _print_list(self, games):
        if not games:
            print("Список пуст или совпадений не найдено.")
            return
        print("\nID | Название | Жанр | Год | ID Студии")
        print("-" * 45)
        for g in games:
            print(f"{g.id} | {g.title} | {g.genre} | {g.year} | {g.studio_id}")