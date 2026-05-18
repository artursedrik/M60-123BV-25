import pytest
import tempfile
import os
from src.db.repository import DatabaseRepository
from src.db.models import Column

@pytest.fixture
def repo():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as f:
        temp_file = f.name
    repo = DatabaseRepository(temp_file)
    yield repo
    if os.path.exists(temp_file):
        os.unlink(temp_file)

def test_create_table(repo):
    columns = [Column("id", "int"), Column("name", "str")]
    table = repo.create_table("users", columns)
    assert table.name == "users"

def test_add_row(repo):
    columns = [Column("name", "str")]
    repo.create_table("users", columns)
    repo.add_row("users", {"name": "Alice"})
    rows = repo.get_rows("users")
    assert len(rows) == 1
    assert rows[0]["name"] == "Alice"

def test_delete_row(repo):
    columns = [Column("name", "str")]
    repo.create_table("users", columns)
    repo.add_row("users", {"name": "Alice"})
    repo.delete_row("users", 0)
    rows = repo.get_rows("users")
    assert len(rows) == 0
    