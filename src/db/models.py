from dataclasses import dataclass
from typing import Dict, Any, List
from datetime import datetime

@dataclass
class Column:
    """Определение колонки таблицы"""
    name: str
    data_type: str  # 'int', 'str', 'float', 'bool', 'datetime'
    primary_key: bool = False
    nullable: bool = True

@dataclass
class Table:
    """Пользовательская таблица"""
    name: str
    columns: Dict[str, Column]
    rows: List[Dict[str, Any]]
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def add_row(self, row: Dict[str, Any]) -> None:
        """Добавить запись в таблицу"""
        # Проверяем, что все колонки есть
        for col_name, col in self.columns.items():
            if not col.nullable and col_name not in row:
                raise ValueError(f"Колонка '{col_name}' не может быть пустой")
        
        # Проверяем типы данных
        for col_name, value in row.items():
            if col_name not in self.columns:
                raise ValueError(f"Неизвестная колонка '{col_name}'")
            col = self.columns[col_name]
            if col.data_type == 'int' and not isinstance(value, int):
                raise TypeError(f"Колонка '{col_name}' должна быть int")
            elif col.data_type == 'str' and not isinstance(value, str):
                raise TypeError(f"Колонка '{col_name}' должна быть str")
            elif col.data_type == 'float' and not isinstance(value, (int, float)):
                raise TypeError(f"Колонка '{col_name}' должна быть float")
            elif col.data_type == 'bool' and not isinstance(value, bool):
                raise TypeError(f"Колонка '{col_name}' должна быть bool")
        
        self.rows.append(row)
    
    def get_rows(self) -> List[Dict[str, Any]]:
        """Получить все записи"""
        return self.rows
    
    def update_row(self, index: int, row: Dict[str, Any]) -> None:
        """Обновить запись по индексу"""
        if index < 0 or index >= len(self.rows):
            raise IndexError("Индекс вне диапазона")
        self.rows[index] = row
    
    def delete_row(self, index: int) -> None:
        """Удалить запись по индексу"""
        if index < 0 or index >= len(self.rows):
            raise IndexError("Индекс вне диапазона")
        self.rows.pop(index)
    
    def select(self, condition=None):
        """Выбрать записи по условию"""
        if condition is None:
            return self.rows
        return [row for row in self.rows if condition(row)]

@dataclass
class Database:
    """База данных с пользовательскими таблицами"""
    tables: Dict[str, Table]
    
    def __init__(self):
        self.tables = {}
    
    def create_table(self, name: str, columns: List[Column]) -> Table:
        """Создать новую таблицу"""
        if name in self.tables:
            raise ValueError(f"Таблица '{name}' уже существует")
        
        columns_dict = {col.name: col for col in columns}
        table = Table(
            name=name,
            columns=columns_dict,
            rows=[],
            created_at=datetime.now()
        )
        self.tables[name] = table
        return table
    
    def get_table(self, name: str) -> Table:
        """Получить таблицу по имени"""
        if name not in self.tables:
            raise ValueError(f"Таблица '{name}' не существует")
        return self.tables[name]
    
    def list_tables(self) -> List[str]:
        """Список всех таблиц"""
        return list(self.tables.keys())
    
    def delete_table(self, name: str) -> None:
        """Удалить таблицу"""
        if name not in self.tables:
            raise ValueError(f"Таблица '{name}' не существует")
        del self.tables[name]
        