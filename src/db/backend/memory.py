from typing import List, Optional
from src.db.backend.database import Game
from src.db.backend.errors import ValidationError


class InMemoryDatabase:
    def __init__(self):
        self.games: List[Game] = []
        self.current_id: int = 1
        self.columns: List[str] = ["id", "title", "genre", "year", "studio_id"]

    def add_game(self, title: str, genre: str, year: int, studio_id: int) -> bool:
        try:
            Game.validate(title, genre, year, studio_id)
            game = Game(self.current_id, title, genre, year, studio_id)
            self.games.append(game)
            self.current_id += 1
            return True
        except ValidationError:
            return False

    def delete_game(self, game_id: int) -> bool:
        if not isinstance(game_id, int):
            return False
        for i, g in enumerate(self.games):
            if g.id == game_id:
                self.games.pop(i)
                return True
        return False

    def update_game(self, game_id: int, title: str, genre: str, year: int, studio_id: int) -> bool:
        if not isinstance(game_id, int):
            return False

        target_index = -1
        for i, g in enumerate(self.games):
            if g.id == game_id:
                target_index = i
                break

        if target_index == -1:
            return False

        try:
            Game.validate(title, genre, year, studio_id)
        except ValidationError:
            return False

        self.games[target_index] = Game(game_id, title, genre, year, studio_id)
        return True

    def get_games(
        self,
        title: Optional[str] = None,
        genre: Optional[str] = None,
        year: Optional[int] = None
    ) -> List[Game]:
        filtered = [g.clone() for g in self.games]

        if title is not None:
            title_clean = str(title).strip().lower()
            filtered = [g for g in filtered if title_clean in g.title.lower()]

        if genre is not None:
            genre_clean = str(genre).strip().lower()
            filtered = [g for g in filtered if genre_clean == g.genre.lower()]

        if year is not None:
            if not isinstance(year, int):
                return []
            filtered = [g for g in filtered if g.year == year]

        return filtered
