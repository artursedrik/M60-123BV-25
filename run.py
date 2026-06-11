from src.db.repository import BookRepository, FileBookRepository
from src.db.tui import LibraryTUI


def choose_repository():
    print("\n=== ВЫБОР ТИПА ХРАНИЛИЩА ===")
    print("1. In-memory (данные не сохраняются)")
    print("2. File-based (сохраняются в JSON-файл)")
    choice = input("Ваш выбор (1/2): ").strip()
    if choice == "1":
        print("✓ Выбрано In-memory хранилище")
        return BookRepository()
    elif choice == "2":
        filename = input("Имя JSON-файла [library.json]: ").strip()
        if not filename:
            filename = "library.json"
        print(f"✓ Выбрано File-based хранилище (файл: {filename})")
        return FileBookRepository(filename)
    else:
        print("Неверный выбор, выбираю In-memory по умолчанию.")
        return BookRepository()


def main():
    repo = choose_repository()
    app = LibraryTUI(repo)
    app.run()


if __name__ == "__main__":
    main()
    