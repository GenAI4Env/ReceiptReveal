import os
from google import genai
from google.genai import types
from PIL import Image, ImageFile
from carbon_scanner.config import config

assert config.GEMINI_API_KEY, "GEMINI_API_KEY is not set in the environment variables."
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
    response = client.models.generate_content(
        model="gemini-2.0-pro-exp-02-05",
        contents=prompt,
    )
    return response.text


if __name__ == "__main__":
    # Example usage
    prompt = "What is the capital of France?"

    text_response = text_resp(prompt)
    print("Response from Gemini with text:", text_response)
