import os
from dotenv import load_dotenv
load_dotenv()
from enum import Enum

from PIL import Image

from google import genai



class GeminiModel(Enum):
    GEMINI_2_0_FLASH = "gemini-2.0-flash"
    GEMINI_2_0_FLASH_LITE = "gemini-2.0-flash-lite"
    GEMINI_2_0_PRO_EXPERIMENTAL = "gemini-2.0-pro-exp-02-05"
    GEMINI_2_5_PRO_PREVIEW = "gemini-2.5-pro-preview-03-25"
    GEMINI_2_5_FLASH_PREVIEW = "gemini-2.5-flash-preview-04-17"
    GEMINI_1_5_FLASH = "gemini-1.5-flash"
    GEMINI_1_5_PRO = "gemini-1.5-pro"

def get_response(system_prompt: str, user_prompt: str, model: GeminiModel, input_images: list[Image.Image] = None, output_schema: type = None) -> str:
    api_key = os.getenv("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    config = {
        'system_instruction': system_prompt
    }

    if output_schema:
        config = {
            'response_mime_type': 'application/json',
            'response_schema': output_schema,
            'system_instruction': system_prompt,
        }

    contents = [user_prompt]
    if input_images:
        contents.extend(input_images)
    
    response = client.models.generate_content(
        model=model.value,
        config=config,
        contents=contents
    )

    return response.text
    