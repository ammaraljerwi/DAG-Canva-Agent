from typing import Optional
from pydantic import BaseModel


class AgentRequest(BaseModel):
    user_id: str
    session_id: str
    query: str
    contains_selection: bool = False
    selection_data: Optional[str] = None


class AgentResponse(BaseModel):
    message: str
    generated_image: Optional[list[str]]
    image_mimetype: Optional[str]
