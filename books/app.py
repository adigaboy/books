from typing import Annotated, Dict, List

from fastapi import Depends, FastAPI, Response

from common.authentication import get_current_username
from common.schemes import Book, UpdateBook

app = FastAPI()

db: Dict[str, Book] = {}
authors_books: Dict[str, List[str]] = {}


@app.get("/books/{book_id}")
async def retrieve_a_book(book_id: str, response: Response) -> Book | None:
    book = db.get(book_id)
    if not book:
        response.status_code = 404
        return None
    return book

@app.get("/books")
async def list_books(author: str=None) -> List[Book]:
    if author:
        books_of_author = authors_books.get(author, [])
        return [db[isbn] for isbn in books_of_author]
    return list(db.values())

@app.post("/books")
async def add_book(username: Annotated[str, Depends(get_current_username)], book: Book, response: Response) -> Book | Dict[str, str]:
    if book.isbn in db:
        response.status_code = 400
        return {"error": "Book already exists"}
    db[book.isbn] = book
    return db[book.isbn]

@app.put("/books/{book_id}")
async def update_book(username: Annotated[str, Depends(get_current_username)], book_id: str, book_updates: UpdateBook) -> Book | None:
    if book_id not in db:
        return None
    book_in_db = db[book_id].model_dump()
    book_in_db.update(book_updates)
    db[book_id] = book_in_db
    return db[book_id]

@app.delete("/books/{book_id}")
async def delete_book(username: Annotated[str, Depends(get_current_username)], book_id: str, response: Response) -> dict:
    try:
        del db[book_id]
        return {"status": "OK"}
    except KeyError:
        response.status_code = 404
        return {"error": "Book not found"}
