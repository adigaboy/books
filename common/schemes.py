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
    title: Optional[str]
    author: Optional[str]
    publisher: Optional[str]
    publication_date: Optional[date]
