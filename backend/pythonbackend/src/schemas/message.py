from datetime import datetime
from pydantic import BaseModel


class Content(BaseModel):
    type: str
    text: str | None
    image_url: str | None


class MessageBase(BaseModel):
    user_id: str
    session_id: str
    role: str
    content: Content | str


class MessageCreate(MessageBase):
    pass


class MessageInDB(MessageBase):
    timestamp: datetime

    class Config:
        from_attributes = True
