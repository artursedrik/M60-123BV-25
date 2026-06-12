Садриеив Артур Русланович
М6о-123бв-25
python

# Лабораторная работа №4 - Файловая СУБД

## Схема проекта

```plain
PIOA-123/
├── src/db
│   ├── __init__.py
│   ├── models.py
│   ├── repository.py
│   └── tui.py
│
├── tests/
│   ├── test_models.py
│   ├── test_repository.py
│   └── test_tui.py
│
└── README.md
```

## Различие реализаций

| Операция          | In-memory             | File-based                 |
| ----------------- | --------------------- | -------------------------- |
| Сохранение данных | Не сохраняется        | Сохраняется в JSON         |
| Скорость работы   | Очень быстро          | Медленнее (запись на диск) |
| Переносимость     | Теряется после выхода | Можно передать файл        |

## Запуск

```bash
python run.py
```

## Тесты

```bash
python -m pytest tests/ -v
```

## Тесты с покрытием

```bash
python -m pytest --cov=src --cov-report=term-missing
```
