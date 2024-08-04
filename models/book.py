from typing import Union
from pydantic import BaseModel

class Book(BaseModel):
    isbn: Union[int, None]
    title: Union[str, None]
    author: Union[str, None]
    availability: Union[int, None] = None

class AddBook(BaseModel):
    isbn: int
    title: str
    author: str
    availability: int = 1

class DeleteBook(BaseModel):
    isbn: int
