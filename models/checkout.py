from typing import Union
from pydantic import BaseModel

class Checkout(BaseModel):
    isbn: int
    user_id: Union[int, None]

class Return(BaseModel):
    isbn: int
