import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db.repository import BookRepository

class TestBookRepository(unittest.TestCase):
    def setUp(self):
        self.repo = BookRepository()

    # === CREATE TESTS ===
    def test_create_book(self):
        book = self.repo.create(1, "Test", "Author", 2024, "Fiction")
        self.assertEqual(book.title, "Test")

    def test_create_negative_year_raises_error(self):
        with self.assertRaises(ValueError):
            self.repo.create(1, "Test", "Author", -5, "Fiction")

    def test_create_duplicate_id_raises_error(self):
        self.repo.create(1, "Book1", "Author1", 2000, "Genre1")
        with self.assertRaises(ValueError):
            self.repo.create(1, "Book2", "Author2", 2001, "Genre2")

    # === SELECT / FILTER TESTS ===
    def test_select_by_id(self):
        self.repo.create(1, "Book1", "Author1", 2000, "Genre1")
        self.repo.create(2, "Book2", "Author2", 2001, "Genre2")
        results = self.repo.select(book_id=1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Book1")

    def test_select_by_title_filter(self):
        self.repo.create(1, "War and Peace", "Tolstoy", 1869, "Novel")
        results = self.repo.select(title="war")
        self.assertEqual(len(results), 1)

    def test_select_by_author_filter(self):
        self.repo.create(1, "Book1", "Tolstoy", 1869, "Novel")
        self.repo.create(2, "Book2", "Dostoevsky", 1866, "Novel")
        results = self.repo.select(author="tolstoy")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].author, "Tolstoy")

    def test_select_by_year_filter(self):
        self.repo.create(1, "Book1", "Author1", 2000, "Genre1")
        self.repo.create(2, "Book2", "Author2", 2001, "Genre2")
        results = self.repo.select(year=2000)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].year, 2000)

    def test_select_by_genre_filter(self):
        self.repo.create(1, "Book1", "Author1", 2000, "Fantasy")
        self.repo.create(2, "Book2", "Author2", 2001, "Sci-Fi")
        results = self.repo.select(genre="fantasy")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].genre, "Fantasy")

    def test_select_by_multiple_filters(self):
        self.repo.create(1, "War and Peace", "Tolstoy", 1869, "Novel")
        self.repo.create(2, "Anna Karenina", "Tolstoy", 1877, "Novel")
        self.repo.create(3, "Crime and Punishment", "Dostoevsky", 1866, "Novel")
        results = self.repo.select(author="Tolstoy", year=1869)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "War and Peace")

    def test_select_no_results(self):
        self.repo.create(1, "Book1", "Author1", 2000, "Genre1")
        results = self.repo.select(author="Nonexistent")
        self.assertEqual(len(results), 0)

    def test_select_by_id_not_found(self):
        self.repo.create(1, "Book1", "Author1", 2000, "Genre1")
        results = self.repo.select(book_id=999)
        self.assertEqual(len(results), 0)

    # === UPDATE TESTS ===
    def test_update_book(self):
        self.repo.create(1, "Old", "Author", 2000, "Genre")
        updated = self.repo.update(1, title="New")
        self.assertEqual(updated.title, "New")

    def test_update_multiple_fields(self):
        self.repo.create(1, "Old", "OldAuthor", 2000, "OldGenre")
        updated = self.repo.update(1, title="New", author="NewAuthor", year=2024, genre="NewGenre")
        self.assertEqual(updated.title, "New")
        self.assertEqual(updated.author, "NewAuthor")
        self.assertEqual(updated.year, 2024)
        self.assertEqual(updated.genre, "NewGenre")

    def test_update_author_only(self):
        self.repo.create(1, "Book", "OldAuthor", 2000, "Genre")
        updated = self.repo.update(1, author="NewAuthor")
        self.assertEqual(updated.author, "NewAuthor")
        self.assertEqual(updated.title, "Book")

    def test_update_genre_only(self):
        self.repo.create(1, "Book", "Author", 2000, "OldGenre")
        updated = self.repo.update(1, genre="NewGenre")
        self.assertEqual(updated.genre, "NewGenre")

    def test_update_negative_year_raises_error(self):
        self.repo.create(1, "Book", "Author", 2000, "Genre")
        with self.assertRaises(ValueError):
            self.repo.update(1, year=-10)

    def test_update_nonexistent_book_raises_error(self):
        with self.assertRaises(ValueError):
            self.repo.update(999, title="New")

    # === DELETE TESTS ===
    def test_delete_book(self):
        self.repo.create(1, "Book", "Author", 2000, "Genre")
        deleted = self.repo.delete(1)
        self.assertEqual(deleted.id, 1)
        self.assertEqual(len(self.repo.get_all()), 0)

    def test_delete_nonexistent_book_raises_error(self):
        with self.assertRaises(ValueError):
            self.repo.delete(999)

    # === GET_ALL TESTS ===
    def test_get_all_returns_all_books(self):
        self.repo.create(1, "Book1", "Author1", 2000, "Genre1")
        self.repo.create(2, "Book2", "Author2", 2001, "Genre2")
        all_books = self.repo.get_all()
        self.assertEqual(len(all_books), 2)

    def test_get_all_empty_returns_empty_list(self):
        all_books = self.repo.get_all()
        self.assertEqual(len(all_books), 0)

if __name__ == "__main__":
    unittest.main()