from sqlalchemy.orm import Session
from agents import (
    Agent,
    Runner,
    RunContextWrapper,
    set_default_openai_key,
    function_tool,
    ModelSettings,
)

from src.api_helper import get_design
from src.database import crud
from src.schemas.agent import AgentRequest, AgentResponse
from src.schemas.message import MessageCreate
from src.schemas.user import UserContext
from src.core.config import settings

from src.agents.design_agent import get_design_feedback
from src.agents.enhancer_agent import edit_image_tool

set_default_openai_key(settings.OPENAI_API_KEY)


INSTRUCTIONS = """
You are the design orchestrator agent. You assist the user with general design advice and image enhancement requests.

Available tools:
- get_design_feedback: Downloads the current design and returns feedback about the design.
- edit_image_tool: Edits an image based on the user's prompt.

Workflow:
1. Categorize the user's question into general feedback or a specific request on an image.
2. If the user wants feedback, use the get_design_feedback tool and return the result.
3. If the user wants to edit an image, use the edit_image_tool and be sure to pass in the user's request.
"""


class MainAgent:
    # instructions = "You are a helpful assistant"
    instructions = (
        "You are an orchestrator agent. Begin by categorizing the users prompt into"
        "overall design feedback or specific image enhancement request. "
        "If the user wants feedback on their design, use the get_design_feedback tool "
        "to get overall design feedback."
        "If the user requests a specific image modification, use the edit_image_tool along with the user's request. "
        "When responding after using the edit_image_tool, do not mention the download link in your message."
    )

    def __init__(self, db: Session, user_id: str, session_id: str) -> None:
        self.user_context = crud.get_user_context(db, user_id)
        self.user_id = user_id
        self.session_id = session_id
        self.db = db
        self.agent = Agent[UserContext](
            name="Main Agent",
            instructions=INSTRUCTIONS,
            model="gpt-4.1-mini",
            tools=[get_design_feedback, edit_image_tool],
            output_type=AgentResponse,
            model_settings=ModelSettings(tool_choice="required"),
        )

    async def call_agent(self, request_body: AgentRequest) -> AgentResponse:
        if request_body.contains_selection:
            self.user_context = self.user_context.model_copy(
                update={
                    "contains_selection": request_body.contains_selection,
                    "selection_data": request_body.selection_data,
                }
            )
        result = await Runner.run(
            self.agent, request_body.query, context=self.user_context
        )
        output = result.final_output_as(AgentResponse)

        message = MessageCreate(
            user_id=self.user_id,
            session_id=self.session_id,
            role="agent",
            content=output.message,
        )

        crud.create_message(db=self.db, message=message)

        return output
