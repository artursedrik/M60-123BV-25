from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Book:
    """Модель книги (основная сущность)."""
    id: int
    title: str
    author: str
    year: int
    genre: str

    def __str__(self) -> str:
        return f"ID: {self.id} | {self.title} | {self.author} | {self.year} | {self.genre}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "genre": self.genre
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Book":
        return cls(
            id=data["id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            genre=data["genre"]
        )