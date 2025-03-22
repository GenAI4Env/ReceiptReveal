import os
from google import genai
from google.genai import types
from PIL import Image, ImageFile
from .config import config


client = genai.Client(api_key=config.GEMINI_API_KEY)


def image_resp(prompt: str, image: ImageFile) -> str:
    """
    Generates a model response based on a prompt and an image.
    """
    # Read image bytes
    image_bytes = image.fp.read()

    response = client.models.generate_content(
        model="gemini-2.0-pro-exp-02-05",
        contents=[
            prompt,  # text part
            types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
        ],
    )
    return response.text


def text_resp(prompt: str) -> str:
    """
    Generates a model response based on a text prompt.
    """
    response = client.models.generate_text(
        model="gemini-2.0-pro-exp-02-05",
        prompt=prompt,
        temperature=0.5,
        max_output_tokens=100,
    )
    return response.text


if __name__ == "__main__":
    # Example usage
    prompt = "What is the capital of France?"

    text_response = text_resp(prompt)
    print("Response from Gemini with text:", text_response)
