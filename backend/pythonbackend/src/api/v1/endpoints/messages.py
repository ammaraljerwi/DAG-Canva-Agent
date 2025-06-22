from typing import Union
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.database import crud
from src.schemas.message import MessageCreate, MessageInDB
from src.agents.main_agent import MainAgent

from agents import trace

router = APIRouter()


@router.post("/send_message", response_model=Union[list[MessageInDB], MessageInDB])
async def send_message(message: MessageCreate, db: Session = Depends(get_db)):
    user_message = crud.create_message(db=db, message=message)
    main_agent = MainAgent(db, message.user_id, message.session_id)
    with trace("Evaluate run"):
        agent_response = await main_agent.call_agent(message.content)
    return [user_message, agent_response]


@router.get("/get_history/", response_model=list[MessageInDB])
def get_message_history_blank_session(
    user_id: str = "", session_id: str = "", db: Session = Depends(get_db)
):
    return crud.get_messages(db=db, user_id=user_id, session_id=session_id)
