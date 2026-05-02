
import sys
from lab4 import InMemoryRepository, FileRepository, LibraryTUI

def choose_repository():
    """Выбор типа хранилища при запуске"""
    print("\n" + "=" * 40)
    print("    ВЫБОР ТИПА ХРАНИЛИЩА ДАННЫХ")
    print("=" * 40)
    print("1. In-Memory (данные не сохраняются после выхода)")
    print("2. File-based (данные сохраняются в JSON файл)")
    print("-" * 40)
    
    while True:
        choice = input("Выберите тип хранилища (1/2): ").strip()
        if choice == "1":
            print("\n✓ Выбрано In-Memory хранилище")
            return InMemoryRepository()
        elif choice == "2":
            filename = input("Введите имя файла для сохранения (Enter - library_data.json): ").strip()
            if not filename:
                filename = "library_data.json"
            print(f"\n✓ Выбрано File-based хранилище (файл: {filename})")
            return FileRepository(filename)
        else:
            print("Неверный выбор. Попробуйте снова.")

def main():
    repo = choose_repository()
    app = LibraryTUI(repo)
    app.run()

if __name__ == "__main__":
    main()