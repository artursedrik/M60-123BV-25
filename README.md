# Лабораторная работа №4 - Файловая СУБД

## Описание

Добавление файлового хранилища (JSON) к существующей ООП-реализации.
Поддерживаются два типа хранилищ: in-memory и file-based.

## Структура проекта

src/db/
├── init.py
├── models.py # Классы Book, Column, Table
├── repository.py # BookRepository (in-memory) + FileBookRepository (JSON)
└── tui.py # LibraryTUI (текстовый интерфейс)

tests/
├── test_models.py
└── test_repository.py

run.py

## Запуск программы

bash
python run.py

## Запуск тестов

pytest tests/ -v

## Запуск тестов с покрытием

pytest --cov=src --cov-report=term-missing
