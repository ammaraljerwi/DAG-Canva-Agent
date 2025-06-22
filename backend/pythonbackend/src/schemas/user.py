from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    user_id: str
    design_id: str


class UserCreate(UserBase):
    pass


class UserInDB(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class UserContext(UserBase):
    access_token: str
    contains_selection: Optional[bool] = False
    selection_data: Optional[str] = None
