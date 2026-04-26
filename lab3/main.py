from .repository import BookRepository
from .tui import LibraryTUI

def main():
    repo = BookRepository()
    app = LibraryTUI(repo)
    app.run()

if __name__ == "__main__":
    main()