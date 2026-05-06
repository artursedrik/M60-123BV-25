import sys
sys.path.insert(0, '.')

from lab3.repository import BookRepository
from lab3.tui import LibraryTUI

def main():
    repo = BookRepository()
    app = LibraryTUI(repo)
    app.run()

if __name__ == "__main__":
    main()