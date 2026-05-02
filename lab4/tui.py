from typing import List, Optional
from lab3.models import Book
from .interfaces import BookRepositoryInterface

class LibraryTUI:
    def __init__(self, repository: BookRepositoryInterface):
        self.repo = repository
    
    def run(self):
        while True:
            print('\n=== БИБЛИОТЕКА КНИГ ===')
            print('1. Добавить книгу')
            print('2. Показать все книги')
            print('3. Найти книги')
            print('4. Обновить книгу')
            print('5. Удалить книгу')
            print('0. Выход')
            choice = input('Выберите: ')
            if choice == '1':
                try:
                    self.repo.create(
                        int(input('ID: ')),
                        input('Название: '),
                        input('Автор: '),
                        int(input('Год: ')),
                        input('Жанр: ')
                    )
                    print('✓ Добавлено')
                except Exception as e:
                    print(f'Ошибка: {e}')
            elif choice == '2':
                for b in self.repo.get_all():
                    print(f'{b.id} | {b.title} | {b.author} | {b.year} | {b.genre}')
            elif choice == '3':
                book_id = input('ID (Enter - пропустить): ')
                try:
                    results = self.repo.select(book_id=int(book_id) if book_id else None)
                    for b in results:
                        print(f'{b.id} | {b.title}')
                except Exception as e:
                    print(f'Ошибка: {e}')
            elif choice == '4':
                try:
                    book_id = int(input('ID для обновления: '))
                    title = input('Новое название (Enter - пропустить): ')
                    if title:
                        self.repo.update(book_id, title=title)
                    print('✓ Обновлено')
                except Exception as e:
                    print(f'Ошибка: {e}')
            elif choice == '5':
                try:
                    book_id = int(input('ID для удаления: '))
                    self.repo.delete(book_id)
                    print('✓ Удалено')
                except Exception as e:
                    print(f'Ошибка: {e}')
            elif choice == '0':
                break
