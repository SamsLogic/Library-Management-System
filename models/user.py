from typing import Union
from pydantic import BaseModel

class User(BaseModel):
    user_id: Union[int, None]
    name: Union[str, None]
    is_checked_out: bool = False

class AddUser(BaseModel):
    user_id: int
    name: str
    is_checked_out: bool = False

class DeleteUser(BaseModel):
    user_id: int
