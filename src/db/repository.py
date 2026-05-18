import json
import os
from typing import List, Dict, Any, Optional
from .models import Database, Table, Column

class DatabaseRepository:
    """Репозиторий для работы с базой данных (файловое хранилище)"""
    
    def __init__(self, filename: str = "database.json"):
        self.filename = filename
        self.db = Database()
        self._load()
    
    def _save(self) -> None:
        """Сохранить базу данных в JSON"""
        data = {
            "tables": {}
        }
        for table_name, table in self.db.tables.items():
            data["tables"][table_name] = {
                "name": table.name,
                "columns": [
                    {
                        "name": col.name,
                        "data_type": col.data_type,
                        "primary_key": col.primary_key,
                        "nullable": col.nullable
                    }
                    for col in table.columns.values()
                ],
                "rows": table.rows,
                "created_at": table.created_at.isoformat()
            }
        
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _load(self) -> None:
        """Загрузить базу данных из JSON"""
        if not os.path.exists(self.filename):
            return
        
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return
                data = json.loads(content)
        except (json.JSONDecodeError, ValueError):
            return
        
        self.db = Database()
        for table_name, table_data in data.get("tables", {}).items():
            columns = []
            for col_data in table_data.get("columns", []):
                columns.append(Column(
                    name=col_data["name"],
                    data_type=col_data["data_type"],
                    primary_key=col_data.get("primary_key", False),
                    nullable=col_data.get("nullable", True)
                ))
            
            from datetime import datetime
            created_at = datetime.fromisoformat(table_data.get("created_at", datetime.now().isoformat()))
            
            table = Table(
                name=table_data["name"],
                columns={col.name: col for col in columns},
                rows=table_data.get("rows", []),
                created_at=created_at
            )
            self.db.tables[table_name] = table
    
    def create_table(self, name: str, columns: List[Column]) -> Table:
        """Создать таблицу"""
        table = self.db.create_table(name, columns)
        self._save()
        return table
    
    def get_table(self, name: str) -> Table:
        """Получить таблицу"""
        return self.db.get_table(name)
    
    def list_tables(self) -> List[str]:
        """Список таблиц"""
        return self.db.list_tables()
    
    def delete_table(self, name: str) -> None:
        """Удалить таблицу"""
        self.db.delete_table(name)
        self._save()
    
    def add_row(self, table_name: str, row: Dict[str, Any]) -> None:
        """Добавить запись в таблицу"""
        table = self.db.get_table(table_name)
        table.add_row(row)
        self._save()
    
    def get_rows(self, table_name: str) -> List[Dict[str, Any]]:
        """Получить все записи из таблицы"""
        table = self.db.get_table(table_name)
        return table.get_rows()
    
    def update_row(self, table_name: str, index: int, row: Dict[str, Any]) -> None:
        """Обновить запись"""
        table = self.db.get_table(table_name)
        table.update_row(index, row)
        self._save()
    
    def delete_row(self, table_name: str, index: int) -> None:
        """Удалить запись"""
        table = self.db.get_table(table_name)
        table.delete_row(index)
        self._save()
    
    def select(self, table_name: str, condition=None) -> List[Dict[str, Any]]:
        """Выбрать записи по условию"""
        table = self.db.get_table(table_name)
        return table.select(condition)
    