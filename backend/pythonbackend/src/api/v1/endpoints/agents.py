from typing import Union
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.database import crud
from src.schemas.message import MessageCreate, MessageInDB
from src.schemas.agent import AgentRequest, AgentResponse
from src.agents.main_agent import MainAgent

from agents import trace

router = APIRouter()


@router.post("/call_agent", response_model=Union[list[AgentResponse], AgentResponse])
async def call_agent(message: AgentRequest, db: Session = Depends(get_db)):
    print(message)
    print(type(message))
    db_input = MessageCreate(
        user_id=message.user_id,
        session_id=message.session_id,
        role="user",
        content=message.query,
    )
    user_message = crud.create_message(db=db, message=db_input)
    main_agent = MainAgent(db, message.user_id, message.session_id)
    with trace("evaluate issues"):
        agent_response = await main_agent.call_agent(message)
    return agent_response


@router.get("/get_history/", response_model=list[MessageInDB])
def get_message_history_blank_session(
    user_id: str = "", session_id: str = "", db: Session = Depends(get_db)
):
    return crud.get_messages(db=db, user_id=user_id, session_id=session_id)
