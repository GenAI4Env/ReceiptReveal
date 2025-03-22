from dotenv import load_dotenv
import os

# Load environment variables from the project's root directory
load_dotenv()


class Config:
    @property
    def GEMINI_API_KEY(self) -> str:
        return os.getenv("GEMINI_API_KEY", "")


config = Config()
