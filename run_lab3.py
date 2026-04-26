from lab3.repository import BookRepository
from lab3.tui import LibraryTUI

if __name__ == "__main__":
    repo = BookRepository()
    app = LibraryTUI(repo)
    app.run()
