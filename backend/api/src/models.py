from datetime import datetime

from sqlmodel import SQLModel, Field
from typing import Optional


class UserBase(SQLModel):
    username: str
    password: str
    email: str
    registered: datetime
    expires: datetime
    restrictions: int
    locked: int


class User(UserBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)
