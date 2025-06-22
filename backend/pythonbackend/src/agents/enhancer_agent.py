from agents import (
    Agent,
    RunContextWrapper,
    set_default_openai_key,
    function_tool,
    Runner,
    ImageGenerationTool,
)
import requests
import base64
import mimetypes
from openai import OpenAI

from src.schemas.user import UserContext
from src.core.config import settings
from src.s3helpers import upload_image, create_url

set_default_openai_key(settings.OPENAI_API_KEY)


def download_image(image_url):
    res = requests.get(image_url)

    if not res.ok:
        print("failed to open image, returning None")
        print(res.json())
        return None

    header = res.headers
    mime_type = header["Content-Type"]
    suffix = mimetypes.guess_extension(mime_type)
    if not suffix:
        suffix = ".png"
    data = res.content
    with open("tmp" + suffix, "wb") as f:
        f.write(data)

    return mime_type


client = OpenAI(api_key=settings.OPENAI_API_KEY)

IMAGE_ENHANCEMENT_PROMPT = (
    # "You are an expert in design fundamentals, your primary focus is to "
    # "critique a design and provide short, brief feedback on improvement."
    # "Begin by using the get_design_link tool to get the design image link."
    # "Analyze the image and provide 2-3 bullet points of where the design "
    # "could be improved."
    "You are a helpful agent"
)

image_enhancer_agent = Agent[UserContext](
    name="image_enhancer_agent",
    instructions=IMAGE_ENHANCEMENT_PROMPT,
    tools=[ImageGenerationTool(tool_config={})],
)


@function_tool
async def edit_image_tool(ctx: RunContextWrapper[UserContext], user_request: str):
    """Enhances the user's selected image and returns a tuple containing an array containing the enhanced image and the associated mimetype"""
    mimetype = download_image(ctx.context.selection_data)

    if not mimetype:
        return None

    extension = mimetypes.guess_extension(mimetype)
    if not extension:
        extension = ".png"

    result = client.images.edit(
        model="gpt-image-1",
        image=[open("tmp" + extension, "rb")],
        prompt=user_request,
        quality="low",
        output_format="jpeg" if extension == ".jpg" else "png",
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    # Save the image to a file
    with open("edited_tmp" + extension, "wb") as f:
        f.write(image_bytes)

    if not upload_image(
        "edited_tmp" + extension,
        settings.BUCKET_NAME,
        "edited_upload" + extension,
        mimetype,
    ):
        return None

    url = create_url(
        "edited_upload" + extension, settings.BUCKET_NAME, settings.BUCKET_REGION
    )

    return url, mimetype
