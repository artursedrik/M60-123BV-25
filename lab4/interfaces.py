from abc import ABC, abstractmethod
from typing import List, Optional
from lab3.models import Book

class BookRepositoryInterface(ABC):
    @abstractmethod
    def create(self, book_id: int, title: str, author: str, year: int, genre: str) -> Book:
        pass
    
    @abstractmethod
    def select(self, book_id: Optional[int] = None, title: Optional[str] = None,
               author: Optional[str] = None, year: Optional[int] = None,
               genre: Optional[str] = None) -> List[Book]:
        pass
    
    @abstractmethod
    def update(self, book_id: int, **kwargs) -> Book:
        pass
    
    @abstractmethod
    def delete(self, book_id: int) -> Book:
        pass
    
    @abstractmethod
    def get_all(self) -> List[Book]:
        pass