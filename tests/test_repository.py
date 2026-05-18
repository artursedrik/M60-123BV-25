import pytest
import tempfile
import os
from src.db.repository import DatabaseRepository
from src.db.models import Column

@pytest.fixture
def repo():
    """Фикстура: временное хранилище для тестов"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as f:
        temp_file = f.name
    
    repo = DatabaseRepository(temp_file)
    yield repo
    
    if os.path.exists(temp_file):
        os.unlink(temp_file)

def test_create_table(repo):
    """Тест создания таблицы"""
    columns = [
        Column("id", "int", nullable=False),
        Column("name", "str")
    ]
    table = repo.create_table("users", columns)
    
    assert table.name == "users"
    assert len(table.columns) == 2
    assert "users" in repo.list_tables()

def test_add_row(repo):
    """Тест добавления записи"""
    columns = [Column("name", "str"), Column("age", "int")]
    repo.create_table("users", columns)
    
    repo.add_row("users", {"name": "Alice", "age": 25})
    rows = repo.get_rows("users")
    
    assert len(rows) == 1
    assert rows[0]["name"] == "Alice"
    assert rows[0]["age"] == 25

def test_update_row(repo):
    """Тест обновления записи"""
    columns = [Column("name", "str")]
    repo.create_table("users", columns)
    
    repo.add_row("users", {"name": "Alice"})
    repo.update_row("users", 0, {"name": "Bob"})
    
    rows = repo.get_rows("users")
    assert rows[0]["name"] == "Bob"

def test_delete_row(repo):
    """Тест удаления записи"""
    columns = [Column("name", "str")]
    repo.create_table("users", columns)
    
    repo.add_row("users", {"name": "Alice"})
    repo.delete_row("users", 0)
    
    rows = repo.get_rows("users")
    assert len(rows) == 0

def test_persistence(repo):
    """Тест сохранения и загрузки"""
    columns = [Column("name", "str")]
    repo.create_table("users", columns)
    repo.add_row("users", {"name": "Alice"})
    
    # Пересоздаём репозиторий с тем же файлом
    repo2 = DatabaseRepository(repo.filename)
    rows = repo2.get_rows("users")
    
    assert len(rows) == 1
    assert rows[0]["name"] == "Alice"

def test_select_with_condition(repo):
    """Тест выборки по условию"""
    columns = [Column("name", "str"), Column("age", "int")]
    repo.create_table("users", columns)
    
    repo.add_row("users", {"name": "Alice", "age": 25})
    repo.add_row("users", {"name": "Bob", "age": 30})
    
    results = repo.select("users", lambda row: row["age"] > 25)
    assert len(results) == 1
    assert results[0]["name"] == "Bob"
    