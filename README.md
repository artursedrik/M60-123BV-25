Лабораторная работа №4 - Файловая СУБД

Функционал

- In-memory хранилище (данные не сохраняются)
- File-based хранилище (данные сохраняются в JSON)

Структура
src/db/
├── init.py
├── models.py # класс Book
└── repository.py # BookRepository и FileBookRepository

tests/
├── test_models.py
└── test_repository.py
Запуск

```bash
python run.py

Тесты
python -m pytest tests/ -v
python -m pytest --cov=src --cov-report=term-missing
```
