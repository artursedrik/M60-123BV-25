from dataclasses import dataclass

@dataclass
class Book:
    id: int
    title: str
    author: str
    year: int
    genre: str

    def __str__(self):
        return f"ID: {self.id} | {self.title} | {self.author} | {self.year} | {self.genre}"
    