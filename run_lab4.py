from lab4 import InMemoryRepository, FileRepository, LibraryTUI

def choose_repo():
    print("\n=== ВЫБОР ХРАНИЛИЩА ===")
    print("1. In-memory (данные не сохранятся)")
    print("2. File-based (сохраняются в JSON)")
    
    try:
        choice = input("Ваш выбор (1/2): ").strip()
    except EOFError:
        choice = "1"
    
    if choice == "1":
        print("✓ Выбрано In-memory хранилище")
        return InMemoryRepository()
    elif choice == "2":
        name = input("Имя файла [library.json]: ").strip()
        if not name:
            name = "library.json"
        print(f"✓ Выбрано File-based хранилище (файл: {name})")
        return FileRepository(name)
    else:
        print("Неверный выбор, выбираю In-memory")
        return InMemoryRepository()

def main():
    repo = choose_repo()
    app = LibraryTUI(repo)
    app.run()

if __name__ == "__main__":
    main()
    