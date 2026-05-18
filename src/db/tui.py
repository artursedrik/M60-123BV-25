from typing import List, Dict, Any
from .repository import DatabaseRepository
from .models import Column

class DatabaseTUI:
    """Текстовый интерфейс для работы с базой данных"""
    
    def __init__(self, repo: DatabaseRepository):
        self.repo = repo
    
    def _print_menu(self) -> None:
        print("\n" + "=" * 50)
        print("         СИСТЕМА УПРАВЛЕНИЯ БАЗОЙ ДАННЫХ")
        print("=" * 50)
        print("1. Создать таблицу")
        print("2. Показать все таблицы")
        print("3. Работа с таблицей")
        print("4. Удалить таблицу")
        print("0. Выход")
        print("-" * 50)
    
    def _table_menu(self, table_name: str) -> None:
        while True:
            print(f"\n--- Таблица: {table_name} ---")
            print("1. Добавить запись")
            print("2. Показать все записи")
            print("3. Обновить запись")
            print("4. Удалить запись")
            print("0. Назад")
            
            choice = input("Выберите действие: ").strip()
            
            if choice == "1":
                self._add_row(table_name)
            elif choice == "2":
                self._show_rows(table_name)
            elif choice == "3":
                self._update_row(table_name)
            elif choice == "4":
                self._delete_row(table_name)
            elif choice == "0":
                break
            else:
                print("Неизвестная команда")
    
    def _add_row(self, table_name: str) -> None:
        try:
            table = self.repo.get_table(table_name)
            print("\n--- Добавление записи ---")
            row = {}
            for col_name, col in table.columns.items():
                value = input(f"{col_name} ({col.data_type}): ").strip()
                if col.data_type == 'int':
                    row[col_name] = int(value) if value else None
                elif col.data_type == 'float':
                    row[col_name] = float(value) if value else None
                elif col.data_type == 'bool':
                    row[col_name] = value.lower() in ('true', 'да', 'yes', '1') if value else None
                else:
                    row[col_name] = value if value else None
            
            self.repo.add_row(table_name, row)
            print("✓ Запись добавлена")
        except Exception as e:
            print(f"Ошибка: {e}")
    
    def _show_rows(self, table_name: str) -> None:
        try:
            rows = self.repo.get_rows(table_name)
            if not rows:
                print("Записей нет")
                return
            
            print(f"\n--- Записи ({len(rows)}) ---")
            for i, row in enumerate(rows):
                print(f"[{i}] {row}")
        except Exception as e:
            print(f"Ошибка: {e}")
    
    def _update_row(self, table_name: str) -> None:
        try:
            rows = self.repo.get_rows(table_name)
            if not rows:
                print("Записей нет")
                return
            
            index = int(input("Введите индекс записи: "))
            if index < 0 or index >= len(rows):
                print("Неверный индекс")
                return
            
            table = self.repo.get_table(table_name)
            print("Введите новые значения (Enter - оставить без изменений):")
            row = rows[index].copy()
            for col_name, col in table.columns.items():
                current = row.get(col_name, '')
                value = input(f"{col_name} [{current}]: ").strip()
                if value:
                    if col.data_type == 'int':
                        row[col_name] = int(value)
                    elif col.data_type == 'float':
                        row[col_name] = float(value)
                    elif col.data_type == 'bool':
                        row[col_name] = value.lower() in ('true', 'да', 'yes', '1')
                    else:
                        row[col_name] = value
            
            self.repo.update_row(table_name, index, row)
            print("✓ Запись обновлена")
        except Exception as e:
            print(f"Ошибка: {e}")
    
    def _delete_row(self, table_name: str) -> None:
        try:
            rows = self.repo.get_rows(table_name)
            if not rows:
                print("Записей нет")
                return
            
            index = int(input("Введите индекс записи для удаления: "))
            confirm = input("Вы уверены? (д/н): ").lower()
            if confirm in ('д', 'да', 'y', 'yes'):
                self.repo.delete_row(table_name, index)
                print("✓ Запись удалена")
        except Exception as e:
            print(f"Ошибка: {e}")
    
    def _create_table(self) -> None:
        print("\n--- Создание таблицы ---")
        name = input("Название таблицы: ").strip()
        if not name:
            print("Название не может быть пустым")
            return
        
        columns = []
        print("Введите колонки (пустое имя - завершить):")
        while True:
            col_name = input("Имя колонки: ").strip()
            if not col_name:
                break
            
            print("Тип данных: 1-str, 2-int, 3-float, 4-bool")
            type_choice = input("Выберите тип (1-4): ").strip()
            data_type_map = {
                "1": "str",
                "2": "int",
                "3": "float",
                "4": "bool"
            }
            data_type = data_type_map.get(type_choice, "str")
            
            nullable = input("Может быть пустым? (д/н): ").lower()
            nullable = nullable in ('д', 'да', 'y', 'yes')
            
            columns.append(Column(
                name=col_name,
                data_type=data_type,
                nullable=nullable
            ))
        
        if not columns:
            print("Таблица должна иметь хотя бы одну колонку")
            return
        
        try:
            self.repo.create_table(name, columns)
            print(f"✓ Таблица '{name}' создана")
        except Exception as e:
            print(f"Ошибка: {e}")
    
    def _list_tables(self) -> None:
        tables = self.repo.list_tables()
        if not tables:
            print("Таблиц нет")
        else:
            print("\n--- Таблицы ---")
            for t in tables:
                print(f"  - {t}")
    
    def _work_with_table(self) -> None:
        tables = self.repo.list_tables()
        if not tables:
            print("Нет таблиц для работы")
            return
        
        print("\n--- Выберите таблицу ---")
        for i, t in enumerate(tables):
            print(f"{i+1}. {t}")
        
        try:
            choice = int(input("Номер таблицы: ")) - 1
            if 0 <= choice < len(tables):
                self._table_menu(tables[choice])
            else:
                print("Неверный номер")
        except ValueError:
            print("Ошибка: введите число")
    
    def _delete_table(self) -> None:
        tables = self.repo.list_tables()
        if not tables:
            print("Нет таблиц для удаления")
            return
        
        print("\n--- Выберите таблицу для удаления ---")
        for i, t in enumerate(tables):
            print(f"{i+1}. {t}")
        
        try:
            choice = int(input("Номер таблицы: ")) - 1
            if 0 <= choice < len(tables):
                confirm = input(f"Удалить таблицу '{tables[choice]}'? (д/н): ").lower()
                if confirm in ('д', 'да', 'y', 'yes'):
                    self.repo.delete_table(tables[choice])
                    print("✓ Таблица удалена")
            else:
                print("Неверный номер")
        except ValueError:
            print("Ошибка: введите число")
    
    def run(self) -> None:
        """Запуск главного меню"""
        print("\n🐍 Добро пожаловать в СУБД!")
        
        while True:
            self._print_menu()
            choice = input("Выберите действие: ").strip()
            
            if choice == "1":
                self._create_table()
            elif choice == "2":
                self._list_tables()
            elif choice == "3":
                self._work_with_table()
            elif choice == "4":
                self._delete_table()
            elif choice == "0":
                print("До свидания!")
                break
            else:
                print("Неизвестная команда")
                