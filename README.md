# Лабораторная работа №3 - ООП и тестирование

## Описание

Переход от процедурного кода к объектно-ориентированному.

## Структура

src/db/
├── init.py
├── models.py # класс Book
├── repository.py # класс BookRepository (in-memory)
└── tui.py # класс LibraryTUI

tests/
├── test_models.py
└── test_repository.py

## Запуск

```bash
python run.py

## Тесты
python -m pytest tests/ -v
python -m pytest --cov=src --cov-report=term-missing

## Функционал
Добавление, поиск, обновление, удаление книг

Поиск по ID, названию, автору, году, жанру

Проверка отрицательного года
```
