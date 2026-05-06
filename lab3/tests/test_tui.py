import unittest
from lab3.repository import BookRepository
from lab3.tui import LibraryTUI

class TestLibraryTUI(unittest.TestCase):
    
    def setUp(self):
        self.repo = BookRepository()
        self.tui = LibraryTUI(self.repo)
    
    def test_repo_available(self):
        self.assertIsNotNone(self.repo)
    
    def test_tui_available(self):
        self.assertIsNotNone(self.tui)

if __name__ == "__main__":
    unittest.main()