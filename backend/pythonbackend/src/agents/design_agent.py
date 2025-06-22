from pydantic import BaseModel
from agents import (
    Agent,
    RunContextWrapper,
    FunctionTool,
    set_default_openai_key,
    function_tool,
    Runner,
)

from src.api_helper import get_design
from src.schemas.user import UserContext
from src.core.config import settings

set_default_openai_key(settings.OPENAI_API_KEY)

FEEDBACK_PROMPT = (
    "You are an expert in design fundamentals, your primary focus is to "
    "critique a design and provide short, brief feedback on improvement."
    "Begin by using the get_design_link tool to get the design image link."
    "Analyze the image and provide 2-3 bullet points of where the design "
    "could be improved."
)

feedback_agent = Agent[UserContext](
    name="design_feedback_agent", instructions=FEEDBACK_PROMPT
)


class ImageData(BaseModel):
    type: str
    image_url: str


@function_tool
async def get_design_feedback(ctx: RunContextWrapper[UserContext], user_input: str):
    design_id = ctx.context.design_id
    access_token = ctx.context.access_token

    res = get_design(access_token, design_id)

    input = [
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": user_input},
                {"type": "input_image", "image_url": res[0]},
            ],
        }
    ]

    result = await Runner.run(feedback_agent, input, context=ctx.context)

    return result.final_output
