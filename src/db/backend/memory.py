from src.db.backend.database import Game

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
                self.games.pop(i)
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