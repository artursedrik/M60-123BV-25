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
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "genre": self.genre
        }
    