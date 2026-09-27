from src.db.backend.errors import ValidationError


class Game:
    def __init__(self, id: int, title: str, genre: str, year: int, studio_id: int):
        self.validate(title, genre, year, studio_id)
        if not isinstance(id, int) or id <= 0:
            raise ValidationError(f"Некорректный ID игры: {id}. ID должен быть положительным числом.")
        
        self.id = id
        self.title = str(title).strip()
        self.genre = str(genre).strip()
        self.year = int(year)
        self.studio_id = int(studio_id)

    @staticmethod
    def validate(title: str, genre: str, year: int, studio_id: int) -> None:
        """Единая валидация полей игры для всех бэкендов."""
        if not isinstance(title, str) or not title.strip():
            raise ValidationError("Название игры не может быть пустым.")
        if not isinstance(genre, str) or not genre.strip():
            raise ValidationError("Жанр игры не может быть пустым.")
        if not isinstance(year, int) or not (1950 <= year <= 2026):
            raise ValidationError(f"Недопустимый год выпуска: {year}. Допустимый диапазон: 1950-2026.")
        if not isinstance(studio_id, int) or studio_id <= 0:
            raise ValidationError(f"Некорректный ID студии: {studio_id}. ID должен быть положительным числом.")

    def clone(self) -> "Game":
        """Создает независимую копию объекта."""
        return Game(self.id, self.title, self.genre, self.year, self.studio_id)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "genre": self.genre,
            "year": self.year,
            "studio_id": self.studio_id
        }

    def __eq__(self, other):
        if not isinstance(other, Game):
            return False
        return (
            self.id == other.id and
            self.title == other.title and
            self.genre == other.genre and
            self.year == other.year and
            self.studio_id == other.studio_id
        )
