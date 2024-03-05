from typing import List, Union

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    is_active: bool
    full_name: Union[str, None] = None

    class Config:
        from_attributes = True


class UserWithPost(UserResponse):
    posts: List[Item] = []


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None


class PostWithUser(ItemBase):
    owner: UserResponse
