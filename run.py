import sys
sys.path.insert(0, '.')

from src.db.repository import DatabaseRepository
from src.db.tui import DatabaseTUI

def main():
    repo = DatabaseRepository("mydb.json")
    app = DatabaseTUI(repo)
    app.run()

if __name__ == "__main__":
    main()
    