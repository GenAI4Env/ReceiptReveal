from google.genai import Client
from carbon_scanner.config import config

client = Client(api_key=config.GEMINI_API_KEY)


class ImageUploader:
    @staticmethod
    def upload_image(file_path: str) -> str:
        response = client.files.upload(filepath=file_path)
        return response.document_uri
