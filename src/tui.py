from src.db.backend.memory import InMemoryDatabase
from src.db.backend.file import JsonDatabase, CsvDatabase
from src.db.backend.errors import DatabaseError


class ConsoleInterface:
    def __init__(self):
        while True:
            print("Выберите режим работы СУБД:")
            print("1 - В оперативной памяти (In-Memory)")
            print("2 - Файл JSON")
            print("3 - Файл CSV")
            choice = input("Ваш выбор: ").strip()

            if choice == "1":
                self.db = InMemoryDatabase()
                print("Запущена СУБД (Режим: In-Memory)")
                break
            elif choice == "2":
                self.db = JsonDatabase("database.json")
                print("Запущена СУБД (Формат: JSON)")
                break
            elif choice == "3":
                self.db = CsvDatabase("database.csv")
                print("Запущена СУБД (Формат: CSV)")
                break
            else:
                print("Неверный выбор. Пожалуйста, введите 1, 2 или 3.\n")

    def _input_int(self, prompt: str, allow_empty: bool = False):
        while True:
            raw = input(prompt).strip()
            if allow_empty and not raw:
                return None
            try:
                return int(raw)
            except ValueError:
                print("Ошибка: значение должно быть целым числом. Попробуйте снова.")

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
                y = self._input_int("Год: ")
                s = self._input_int("ID студии: ")
                try:
                    if self.db.add_game(t, g, y, s):
                        print("Игра успешно сохранена!")
                    else:
                        print("Ошибка валидации данных! Проверьте корректность полей.")
                except (DatabaseError, OSError) as e:
                    print(f"Ошибка сохранения: {e}")

            elif choice == "2":
                games = self.db.get_games()
                self._print_list(games)

            elif choice == "3":
                print("\n--- Фильтрация (Оставьте пустым, если фильтр не нужен) ---")
                st = input("Поиск по названию: ").strip() or None
                sg = input("Поиск по жанру: ").strip() or None
                sy = self._input_int("Поиск по году: ", allow_empty=True)

                games = self.db.get_games(title=st, genre=sg, year=sy)
                self._print_list(games)

            elif choice == "4":
                idx = self._input_int("ID для удаления: ")
                try:
                    if self.db.delete_game(idx):
                        print("Игра удалена!")
                    else:
                        print("Игра не найдена!")
                except (DatabaseError, OSError) as e:
                    print(f"Ошибка сохранения: {e}")

            elif choice == "5":
                idx = self._input_int("ID игры для обновления: ")
                t = input("Новое название: ").strip()
                g = input("Новый жанр: ").strip()
                y = self._input_int("Новый год: ")
                s = self._input_int("Новый ID студии: ")
                try:
                    if self.db.update_game(idx, t, g, y, s):
                        print("Данные игры успешно обновлены!")
                    else:
                        print("Ошибка обновления! Проверьте ID и валидность данных.")
                except (DatabaseError, OSError) as e:
                    print(f"Ошибка сохранения: {e}")

            elif choice == "6":
                print("Выход.")
                break
            else:
                print("Неизвестный пункт меню. Попробуйте снова.")

    def _print_list(self, games):
        if not games:
            print("Список пуст или совпадений не найдено.")
            return
        print("\nID | Название | Жанр | Год | ID Студии")
        print("-" * 45)
        for g in games:
            print(f"{g.id} | {g.title} | {g.genre} | {g.year} | {g.studio_id}")
