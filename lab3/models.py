from dataclasses import dataclass
from typing import Optional

@dataclass
class Book:
    """Модель книги"""
    id: int
    title: str
    author: str
    year: int
    genre: str
    
    def __str__(self) -> str:
        return f"ID: {self.id} | {self.title} | {self.author} | {self.year} | {self.genre}"
    
    def to_tuple(self) -> tuple:
        """Для совместимости с форматом вывода"""
        return (self.id, self.title, self.author, self.year, self.genre)
    
    @classmethod
    def from_tuple(cls, data: tuple) -> 'Book':
        """Создать книгу из кортежа"""
        return cls(id=data[0], title=data[1], author=data[2], year=data[3], genre=data[4])
    
    def to_dict(self) -> dict:
        """Для удобного обновления"""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'genre': self.genre
        }