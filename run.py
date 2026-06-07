import sys
sys.path.insert(0, '.')

from src.db.repository import BookRepository
from src.db.tui import LibraryTUI

def main():
    repo = BookRepository()
    app = LibraryTUI(repo)
    app.run()

if __name__ == "__main__":
    main()