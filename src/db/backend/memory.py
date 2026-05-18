type BookRecord = tuple[int, str, str, int, str]

Book: list[BookRecord] = []

def create_record(
    book_id: int,
    title: str,
    author: str,
    year: int,
    genre: str,
) -> BookRecord:
    if year < 0:
        raise ValueError("Год издания не может быть отрицательным")
    
    for book in Book:
        if book[0] == book_id:
            raise ValueError(f"Книга с id={book_id} уже существует")
    
    new_book: BookRecord = (
        book_id,
        title.strip(),
        author.strip(),
        year,
        genre.strip(),
    )
    
    Book.append(new_book)
    return new_book

def select_record(
    book_id: int | None = None,
    title: str | None = None,
    author: str | None = None,
    year: int | None = None,
    genre: str | None = None,
) -> list[BookRecord]:
    if (book_id is None and title is None and 
        author is None and year is None and genre is None):
        return Book.copy()
    
    result = []
    
    for book in Book:
        if book_id is not None and book[0] != book_id:
            continue
            
        if title is not None and book[1].lower() != title.lower():
            continue
            
        if author is not None and book[2].lower() != author.lower():
            continue
            
        if year is not None and book[3] != year:
            continue
            
        if genre is not None and book[4].lower() != genre.lower():
            continue
        
        result.append(book)
    
    return result

def update_record(book_id: int, **kwargs) -> BookRecord:
    for i, book in enumerate(Book):
        if book[0] == book_id:
            valid_fields = {'title', 'author', 'year', 'genre'}
            for field in kwargs:
                if field not in valid_fields:
                    raise ValueError(f"Некорректное поле: {field}")
            
            if 'year' in kwargs and kwargs['year'] < 0:
                raise ValueError("Год не может быть отрицательным")
            
            new_data = [
                kwargs.get('title', book[1]),
                kwargs.get('author', book[2]),
                kwargs.get('year', book[3]),
                kwargs.get('genre', book[4])
            ]
            
            updated_book = (book[0], *new_data)
            Book[i] = updated_book
            return updated_book
    
    raise ValueError(f"Книга с id={book_id} не найдена")

def delete_record(book_id: int) -> BookRecord:
    for i, book in enumerate(Book):
        if book[0] == book_id:
            deleted = Book.pop(i)
            return deleted
    
    raise ValueError(f"Книга с id={book_id} не найдена")