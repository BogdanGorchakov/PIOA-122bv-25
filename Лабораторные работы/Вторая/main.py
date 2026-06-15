games_db = [
    {"id": 1, "title": "The Witcher 3", "genre": "RPG", "year": 2015, "studio_id": 1},
    {"id": 2, "title": "GTA V", "genre": "Action", "year": 2013, "studio_id": 2},
    {"id": 3, "title": "Cyberpunk 2077", "genre": "RPG", "year": 2020, "studio_id": 1}
]
game_current_id = 4

studios_db = [
    {"id": 1, "name": "CD Projekt RED", "country": "Poland"},
    {"id": 2, "name": "Rockstar Games", "country": "USA"}
]
studio_current_id = 3


def add_game():
    global game_current_id
    print("\n--- Добавление новой игры ---")
    title = input("Введите название игры: ").strip()
    genre = input("Введите жанр игры: ").strip()
    try:
        year = int(input("Введите год выпуска: "))
        studio_id = int(input("Введите ID студии-разработчика: "))
    except ValueError:
        print("Ошибка: Год и ID студии должны быть числами!")
        return

    if not title or not genre:
        print("Ошибка: Поля названия и жанра не могут быть пустыми!")
        return

    new_game = {"id": game_current_id, "title": title, "genre": genre, "year": year, "studio_id": studio_id}
    games_db.append(new_game)
    print(f"Успешно добавлено! ID игры: {game_current_id}")
    game_current_id += 1


def show_and_filter_games():
    print("\n--- Просмотр игр ---")
    print("Выбери фильтр: 1 - Показать все, 2 - Фильтр по жанру, 3 - Фильтр по году")
    choice = input("Твой выбор: ").strip()
    filtered = games_db

    if choice == "2":
        search_genre = input("Введите жанр для поиска: ").strip().lower()
        filtered = [g for g in games_db if g["genre"].lower() == search_genre]
    elif choice == "3":
        try:
            search_year = int(input("Введите год для поиска: "))
            filtered = [g for g in games_db if g["year"] == search_year]
        except ValueError:
            print("Ошибка: Некорректный год!")
            return

    if not filtered:
        print("Игры не найдены.")
        return

    print("\nID | Название | Жанр | Год | ID Студии")
    print("-" * 45)
    for g in filtered:
        print(f"{g['id']} | {g['title']} | {g['genre']} | {g['year']} | {g['studio_id']}")


def update_game():
    print("\n--- Обновление игры ---")
    try:
        game_id = int(input("Введите ID игры для редактирования: "))
    except ValueError:
        print("Ошибка: ID должен быть числом!")
        return

    for g in games_db:
        if g["id"] == game_id:
            title = input(f"Новое название ({g['title']}): ").strip()
            genre = input(f"Новый жанр ({g['genre']}): ").strip()
            year_input = input(f"Новый год ({g['year']}): ").strip()
            studio_input = input(f"Новый ID студии ({g['studio_id']}): ").strip()

            if title: g["title"] = title
            if genre: g["genre"] = genre
            if year_input:
                try:
                    g["year"] = int(year_input)
                except ValueError:
                    print("Год не изменен (нужно число)")
            if studio_input:
                try:
                    g["studio_id"] = int(studio_input)
                except ValueError:
                    print("ID студии не изменен (нужно число)")
            print("Игра успешно обновлена!")
            return
    print("Игра с таким ID не найдена.")


def delete_game():
    print("\n--- Удаление игры ---")
    try:
        game_id = int(input("Введите ID игры для удаления: "))
    except ValueError:
        print("Ошибка: ID должен быть числом!")
        return

    for i, g in enumerate(games_db):
        if g["id"] == game_id:
            del games_db[i]
            print("Игра успешно удалена!")
            return
    print("Игра с таким ID не найдена.")


def add_studio():
    global studio_current_id
    print("\n--- Добавление новой студии ---")
    name = input("Введите название студии: ").strip()
    country = input("Введите страну: ").strip()

    if not name or not country:
        print("Ошибка: Поля не могут быть пустыми!")
        return

    new_studio = {"id": studio_current_id, "name": name, "country": country}
    studios_db.append(new_studio)
    print(f"Студия добавлена! ID: {studio_current_id}")
    studio_current_id += 1


def show_studios():
    print("\n--- Список всех студий ---")
    if not studios_db:
        print("Студий нет в базе.")
        return
    print("ID | Название | Страна")
    print("-" * 35)
    for s in studios_db:
        print(f"{s['id']} | {s['name']} | {s['country']}")


def update_studio():
    print("\n--- Обновление студии ---")
    try:
        studio_id = int(input("Введите ID студии для редактирования: "))
    except ValueError:
        print("Ошибка: ID должен быть числом!")
        return

    for s in studios_db:
        if s["id"] == studio_id:
            name = input(f"Новое название ({s['name']}): ").strip()
            country = input(f"Новая страна ({s['country']}): ").strip()
            if name: s["name"] = name
            if country: s["country"] = country
            print("Данные студии обновлены!")
            return
    print("Студия не найдена.")


def delete_studio():
    print("\n--- Удаление студии ---")
    try:
        studio_id = int(input("Введите ID студии для удаления: "))
    except ValueError:
        print("Ошибка: ID должен быть числом!")
        return

    for i, s in enumerate(studios_db):
        if s["id"] == studio_id:
            del studios_db[i]
            print("Студия успешно удалена!")
            return
    print("Студия не найдена.")


def main():
    while True:
        print("\n===== СУБД ИГР И СТУДИЙ =====")
        print("1. Добавить игру | 2. Просмотр игр | 3. Изменить игру | 4. Удалить игру")
        print("5. Добавить студию | 6. Просмотр студий | 7. Изменить студию | 8. Удалить студию")
        print("9. Выйти из программы")

        choice = input("Выберите действие (1-9): ").strip()

        if choice == "1":
            add_game()
        elif choice == "2":
            show_and_filter_games()
        elif choice == "3":
            update_game()
        elif choice == "4":
            delete_game()
        elif choice == "5":
            add_studio()
        elif choice == "6":
            show_studios()
        elif choice == "7":
            update_studio()
        elif choice == "8":
            delete_studio()
        elif choice == "9":
            print("Выход из программы. Пока!")
            break
        else:
            print("Ошибка: Неверный пункт меню!")


if __name__ == "__main__":
    main()
