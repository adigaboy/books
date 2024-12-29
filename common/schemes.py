from datetime import date
from typing import Optional
from pydantic import BaseModel


class Book(BaseModel):
    isbn: str
    title: str
    author: str
    publisher: str
    publication_date: date

class UpdateBook(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    publication_date: Optional[date] = None
