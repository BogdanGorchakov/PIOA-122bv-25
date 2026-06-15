db = [
    {"id": 1, "title": "The Witcher 3", "genre": "RPG", "year": 2015},
    {"id": 2, "title": "GTA V", "genre": "Action", "year": 2013},
    {"id": 3, "title": "Cyberpunk 2077", "genre": "RPG", "year": 2020}
]
current_id = 4


def add_game():
    global current_id
    print("\n--- Добавление новой игры ---")
    title = input("Введите название игры: ").strip()
    genre = input("Введите жанр игры: ").strip()

    try:
        year = int(input("Введите год выпуска: "))
    except ValueError:
        print("Ошибка: Год должен быть числом! Игра не добавлена.")
        return

    if not title or not genre:
        print("Ошибка: Поля названия и жанра не могут быть пустыми!")
        return

    new_game = {"id": current_id, "title": title, "genre": genre, "year": year}
    db.append(new_game)
    print(f"Успешно добавлено! ID игры: {current_id}")
    current_id += 1


def show_and_filter_games():
    print("\n--- Чтение и фильтрация ---")
    print("Выбери фильтр: 1 - Показать все, 2 - Фильтр по жанру, 3 - Фильтр по году")
    choice = input("Твой выбор: ").strip()

    filtered = db

    if choice == "2":
        search_genre = input("Введите жанр для поиска: ").strip().lower()
        filtered = [g for g in db if g["genre"].lower() == search_genre]
    elif choice == "3":
        try:
            search_year = int(input("Введите год для поиска: "))
            filtered = [g for g in db if g["year"] == search_year]
        except ValueError:
            print("Ошибка: Некорректный год для фильтрации!")
            return
    elif choice != "1":
        print("Неверный вариант фильтра. Показываю все игры.")

    if not filtered:
        print("Игры по вашему запросу не найдены.")
        return

    print("\nID | Название | Жанр | Год")
    print("-" * 35)
    for game in filtered:
        print(f"{game['id']} | {game['title']} | {game['genre']} | {game['year']}")


def main():
    while True:
        print("\n===== МЕНЮ БАЗЫ ДАННЫХ ИГР =====")
        print("1. Добавить игру")
        print("2. Просмотр / Фильтрация игр")
        print("3. Выйти из программы")

        choice = input("Выберите действие (1-3): ").strip()

        if choice == "1":
            add_game()
        elif choice == "2":
            show_and_filter_games()
        elif choice == "3":
            print("Выход из программы. Пока!")
            break
        else:
            print("Ошибка: Неверный пункт меню! Попробуйте снова.")


if __name__ == "__main__":
    main()
