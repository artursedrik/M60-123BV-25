from typing import Optional, List
from .repository import BookRepository
from .models import Book

class LibraryTUI:
    """Текстовый интерфейс для управления библиотекой"""
    
    def __init__(self, repository: BookRepository):
        self.repo = repository
    
    def _print_menu(self) -> None:
        print("\n" + "=" * 40)
        print("         БИБЛИОТЕКА КНИГ")
        print("=" * 40)
        print("1. Добавить книгу")
        print("2. Показать все книги")
        print("3. Найти книги")
        print("4. Обновить информацию о книге")
        print("5. Удалить книгу")
        print("0. Выход")
        print("-" * 40)
    
    def _read_int(self, prompt: str) -> int:
        while True:
            try:
                return int(input(prompt).strip())
            except ValueError:
                print("Ошибка: введите целое число")
    
    def _read_optional_int(self, prompt: str) -> Optional[int]:
        while True:
            value = input(prompt).strip()
            if value == "":
                return None
            try:
                return int(value)
            except ValueError:
                print("Ошибка: введите целое число или оставьте пустым")
    
    def _print_books(self, books: List[Book]) -> None:
        if not books:
            print("Книги не найдены.")
            return
        
        print("\nНайденные книги:")
        print("-" * 60)
        for book in books:
            print(f"ID: {book.id}")
            print(f"Название: {book.title}")
            print(f"Автор: {book.author}")
            print(f"Год: {book.year}")
            print(f"Жанр: {book.genre}")
            print("-" * 60)
    
    def _add_book(self) -> None:
        print("\n--- Добавление новой книги ---")
        
        try:
            book_id = self._read_int("ID книги: ")
            title = input("Название: ").strip()
            author = input("Автор: ").strip()
            year = self._read_int("Год издания: ")
            genre = input("Жанр: ").strip()
            
            book = self.repo.create(book_id, title, author, year, genre)
            print(f"✓ Книга успешно добавлена: {book.title}")
            
        except ValueError as e:
            print(f"✗ Ошибка: {e}")
    
    def _show_all_books(self) -> None:
        print("\n--- Все книги ---")
        books = self.repo.get_all()
        self._print_books(books)
    
    def _find_books(self) -> None:
        print("\n--- Поиск книг ---")
        print("(Оставьте поле пустым, чтобы не учитывать его в поиске)")
        
        book_id = self._read_optional_int("ID: ")
        title = input("Название: ").strip() or None
        author = input("Автор: ").strip() or None
        year = self._read_optional_int("Год: ")
        genre = input("Жанр: ").strip() or None
        
        books = self.repo.select(
            book_id=book_id,
            title=title,
            author=author,
            year=year,
            genre=genre
        )
        
        print(f"\nНайдено книг: {len(books)}")
        self._print_books(books)
    
    def _update_book(self) -> None:
        print("\n--- Обновление книги ---")
        
        book_id = self._read_int("Введите ID книги для обновления: ")
        
        books = self.repo.select(book_id=book_id)
        if not books:
            print(f"✗ Книга с ID {book_id} не найдена")
            return
        
        current_book = books[0]
        print("\nТекущая информация:")
        self._print_books([current_book])
        
        print("\nВведите новые значения (Enter - оставить без изменений):")
        updates = {}
        
        title = input(f"Новое название [{current_book.title}]: ").strip()
        if title:
            updates['title'] = title
        
        author = input(f"Новый автор [{current_book.author}]: ").strip()
        if author:
            updates['author'] = author
        
        year_str = input(f"Новый год [{current_book.year}]: ").strip()
        if year_str:
            try:
                updates['year'] = int(year_str)
            except ValueError:
                print("Год должен быть числом. Поле не будет обновлено.")
        
        genre = input(f"Новый жанр [{current_book.genre}]: ").strip()
        if genre:
            updates['genre'] = genre
        
        if not updates:
            print("Нет изменений для сохранения.")
            return
        
        try:
            updated = self.repo.update(book_id, **updates)
            print("✓ Книга успешно обновлена:")
            self._print_books([updated])
        except ValueError as e:
            print(f"✗ Ошибка: {e}")
    
    def _delete_book(self) -> None:
        print("\n--- Удаление книги ---")
        
        book_id = self._read_int("Введите ID книги для удаления: ")
        
        books = self.repo.select(book_id=book_id)
        if not books:
            print(f"✗ Книга с ID {book_id} не найдена")
            return
        
        print("\nБудет удалена следующая книга:")
        self._print_books(books)
        
        confirm = input("Вы уверены? (д/Н): ").strip().lower()
        if confirm in ['д', 'да', 'y', 'yes']:
            try:
                deleted = self.repo.delete(book_id)
                print(f"✓ Книга '{deleted.title}' удалена")
            except ValueError as e:
                print(f"✗ Ошибка: {e}")
        else:
            print("Удаление отменено")
    
    def run(self) -> None:
        """Запуск основного цикла программы"""
        while True:
            self._print_menu()
            choice = input("Выберите действие: ").strip()
            
            if choice == "1":
                self._add_book()
            elif choice == "2":
                self._show_all_books()
            elif choice == "3":
                self._find_books()
            elif choice == "4":
                self._update_book()
            elif choice == "5":
                self._delete_book()
            elif choice == "0":
                print("До свидания!")
                break
            else:
                print("Неизвестная команда. Попробуйте снова.")