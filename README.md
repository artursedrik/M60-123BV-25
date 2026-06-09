# Лабораторная работа №4 - Файловая СУБД

## Описание

Добавление файлового хранилища (JSON) к существующей ООП-реализации.
Поддерживаются два типа хранилищ: in-memory и file-based.

## Структура проекта

src/db/
├── init.py
├── models.py # Класс Book
├── repository.py # BookRepository (in-memory) + FileBookRepository (JSON)
└── tui.py # LibraryTUI (текстовый интерфейс)

tests/
├── test_models.py
├── test_repository.py
└── test_tui.py

run.py # Точка входа с выбором хранилища

## Запуск программы

python run.py

## Запуск тестов

python -m pytest tests/ -v

## Запуск тестов с покрытием

python -m pytest --cov=src --cov-report=term-missing
