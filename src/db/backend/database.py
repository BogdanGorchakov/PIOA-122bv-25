class Game:
    def __init__(self, id: int, title: str, genre: str, year: int, studio_id: int):
        self.id = id
        self.title = title
        self.genre = genre
        self.year = year
        self.studio_id = studio_id

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "genre": self.genre,
            "year": self.year,
            "studio_id": self.studio_id
        }
