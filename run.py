import sys
sys.path.insert(0, '.')

from src.db.repository import FileBookRepository
from src.db.models import Book

def main():
    repo = FileBookRepository("library.json")
    print("=== Демонстрация работы ===")
    
    # Добавляем книгу
    book = repo.create(1, "Война и мир", "Толстой", 1869, "Роман")
    print(f"Добавлено: {book}")
    
    # Показываем все книги
    print("\nВсе книги:")
    for b in repo.get_all():
        print(f"  {b}")

if __name__ == "__main__":
    main()
    