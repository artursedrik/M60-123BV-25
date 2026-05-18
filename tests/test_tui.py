import pytest
from unittest.mock import Mock, patch
from src.db.tui import DatabaseTUI
from src.db.repository import DatabaseRepository
from src.db.models import Column

@pytest.fixture
def mock_repo():
    """Мок-репозиторий для тестов TUI"""
    repo = Mock(spec=DatabaseRepository)
    repo.list_tables.return_value = ["users", "products"]
    return repo

@pytest.fixture
def tui(mock_repo):
    return DatabaseTUI(mock_repo)

def test_list_tables(tui, mock_repo, capsys):
    """Тест отображения списка таблиц"""
    tui._list_tables()
    captured = capsys.readouterr()
    assert "users" in captured.out
    assert "products" in captured.out

def test_create_table(tui, mock_repo, monkeypatch, capsys):
    """Тест создания таблицы"""
    inputs = iter(["test_table", "id", "2", "n", "name", "1", "y", ""])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    tui._create_table()
    captured = capsys.readouterr()
    assert mock_repo.create_table.called

def test_delete_table(tui, mock_repo, monkeypatch, capsys):
    """Тест удаления таблицы"""
    # Сначала выбираем таблицу (первая в списке)
    inputs = iter(["1", "y"])  # Выбираем первую таблицу, подтверждаем удаление
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    tui._delete_table()
    captured = capsys.readouterr()
    assert mock_repo.delete_table.called
    # Проверяем, что удалили именно "users" (первая в списке)
    mock_repo.delete_table.assert_called_with("users")

def test_show_rows(tui, mock_repo, capsys):
    """Тест отображения записей"""
    mock_repo.get_rows.return_value = [{"id": 1, "name": "Alice"}]
    tui._show_rows("users")
    captured = capsys.readouterr()
    assert "Alice" in captured.out

def test_add_row(tui, mock_repo, monkeypatch, capsys):
    """Тест добавления записи"""
    # Мокаем get_table для получения колонок
    mock_table = Mock()
    mock_table.columns = {
        "name": Mock(data_type="str"),
        "age": Mock(data_type="int")
    }
    mock_repo.get_table.return_value = mock_table
    
    inputs = iter(["Alice", "25"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    tui._add_row("users")
    captured = capsys.readouterr()
    assert mock_repo.add_row.called

def test_update_row(tui, mock_repo, monkeypatch, capsys):
    """Тест обновления записи"""
    # Мокаем get_rows для возврата существующих записей
    mock_repo.get_rows.return_value = [{"name": "Alice", "age": 25}]
    
    # Мокаем get_table для получения колонок
    mock_table = Mock()
    mock_table.columns = {
        "name": Mock(data_type="str"),
        "age": Mock(data_type="int")
    }
    mock_repo.get_table.return_value = mock_table
    
    inputs = iter(["0", "Bob", ""])  # индекс 0, новое имя Bob, возраст пропускаем
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    tui._update_row("users")
    captured = capsys.readouterr()
    assert mock_repo.update_row.called

def test_delete_row(tui, mock_repo, monkeypatch, capsys):
    """Тест удаления записи"""
    # Мокаем get_rows для возврата существующих записей
    mock_repo.get_rows.return_value = [{"name": "Alice"}]
    
    inputs = iter(["0", "y"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    tui._delete_row("users")
    captured = capsys.readouterr()
    assert mock_repo.delete_row.called

def test_work_with_table(tui, mock_repo, monkeypatch, capsys):
    """Тест выбора таблицы для работы"""
    inputs = iter(["1", "0"])  # выбираем первую таблицу, потом выходим в меню
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    tui._work_with_table()
    captured = capsys.readouterr()
    # Проверяем, что меню таблицы было показано
    assert "Таблица: users" in captured.out

def test_run_main_menu_exit(tui, monkeypatch):
    """Тест выхода из главного меню"""
    inputs = iter(["0"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    tui.run()
    # Если дошли до конца без ошибок - тест пройден
    assert True
    