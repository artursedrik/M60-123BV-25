from .backend.memory import (
    create_record,
    select_record,
    update_record,
    delete_record
)

def _print_menu() -> None:
    print("\n" + "="*40)
    print("         БИБЛИОТЕКА КНИГ")
    print("="*40)
    print("1. Добавить книгу")
    print("2. Показать все книги")
    print("3. Найти книги")
    print("4. Обновить информацию о книге")
    print("5. Удалить книгу")
    print("0. Выход")
    print("-"*40)

def _read_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Ошибка: введите целое число")

def _read_optional_int(prompt: str) -> int | None:
    while True:
        value = input(prompt).strip()
        if value == "":
            return None
        try:
            return int(value)
        except ValueError:
            print("Ошибка: введите целое число или оставьте пустым")

def _print_books(books: list[tuple[int, str, str, int, str]]) -> None:
    if not books:
        print("Книги не найдены.")
        return
    
    print("\nНайденные книги:")
    print("-" * 60)
    for book in books:
        print(f"ID: {book[0]}")
        print(f"Название: {book[1]}")
        print(f"Автор: {book[2]}")
        print(f"Год: {book[3]}")
        print(f"Жанр: {book[4]}")
        print("-" * 60)

def _add_book() -> None:
    print("\n--- Добавление новой книги ---")
    
    try:
        book_id = _read_int("ID книги: ")
        title = input("Название: ").strip()
        author = input("Автор: ").strip()
        year = _read_int("Год издания: ")
        genre = input("Жанр: ").strip()
        
        book = create_record(book_id, title, author, year, genre)
        print(f"✓ Книга успешно добавлена: {book[1]}")
        
    except ValueError as e:
        print(f"✗ Ошибка: {e}")

def _show_all_books() -> None:
    print("\n--- Все книги ---")
    books = select_record()
    _print_books(books)

def _find_books() -> None:
    print("\n--- Поиск книг ---")
    print("(Оставьте поле пустым, чтобы не учитывать его в поиске)")
    
    book_id = _read_optional_int("ID: ")
    title = input("Название: ").strip() or None
    author = input("Автор: ").strip() or None
    year = _read_optional_int("Год: ")
    genre = input("Жанр: ").strip() or None
    
    books = select_record(
        book_id=book_id,
        title=title,
        author=author,
        year=year,
        genre=genre
    )
    
    print(f"\nНайдено книг: {len(books)}")
    _print_books(books)

def _update_book() -> None:
    print("\n--- Обновление книги ---")
    
    book_id = _read_int("Введите ID книги для обновления: ")
    
    books = select_record(book_id=book_id)
    if not books:
        print(f"✗ Книга с ID {book_id} не найдена")
        return
    
    print("\nТекущая информация:")
    _print_books(books)
    
    print("\nВведите новые значения (Enter - оставить без изменений):")
    updates = {}
    
    title = input(f"Новое название [{books[0][1]}]: ").strip()
    if title:
        updates['title'] = title
    
    author = input(f"Новый автор [{books[0][2]}]: ").strip()
    if author:
        updates['author'] = author
    
    year_str = input(f"Новый год [{books[0][3]}]: ").strip()
    if year_str:
        try:
            updates['year'] = int(year_str)
        except ValueError:
            print("Год должен быть числом. Поле не будет обновлено.")
    
    genre = input(f"Новый жанр [{books[0][4]}]: ").strip()
    if genre:
        updates['genre'] = genre
    
    if not updates:
        print("Нет изменений для сохранения.")
        return
    
    try:
        updated = update_record(book_id, **updates)
        print("✓ Книга успешно обновлена:")
        _print_books([updated])
    except ValueError as e:
        print(f"✗ Ошибка: {e}")

def _delete_book() -> None:
    print("\n--- Удаление книги ---")
    
    book_id = _read_int("Введите ID книги для удаления: ")
    
    books = select_record(book_id=book_id)
    if not books:
        print(f"✗ Книга с ID {book_id} не найдена")
        return
    
    print("\nБудет удалена следующая книга:")
    _print_books(books)
    
    confirm = input("Вы уверены? (д/Н): ").strip().lower()
    if confirm in ['д', 'да', 'y', 'yes']:
        try:
            deleted = delete_record(book_id)
            print(f"✓ Книга '{deleted[1]}' удалена")
        except ValueError as e:
            print(f"✗ Ошибка: {e}")
    else:
        print("Удаление отменено")

def run() -> None:
    while True:
        _print_menu()
        choice = input("Выберите действие: ").strip()
        
        if choice == "1":
            _add_book()
        elif choice == "2":
            _show_all_books()
        elif choice == "3":
            _find_books()
        elif choice == "4":
            _update_book()
        elif choice == "5":
            _delete_book()
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неизвестная команда. Попробуйте снова.")