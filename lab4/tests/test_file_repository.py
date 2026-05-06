import unittest
import tempfile
import os
from lab4.file_repository import FileRepository

class TestFileRepository(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.temp.close()
        self.repo = FileRepository(self.temp.name)

    def tearDown(self):
        if os.path.exists(self.temp.name):
            os.unlink(self.temp.name)

    def test_create_and_persist(self):
        self.repo.create(1, "Книга", "Автор", 2024, "Жанр")
        self.repo = FileRepository(self.temp.name)  # пересоздаём
        self.assertEqual(len(self.repo.get_all()), 1)

    def test_delete_persists(self):
        self.repo.create(1, "Книга", "Автор", 2024, "Жанр")
        self.repo.delete(1)
        self.repo = FileRepository(self.temp.name)
        self.assertEqual(len(self.repo.get_all()), 0)
        