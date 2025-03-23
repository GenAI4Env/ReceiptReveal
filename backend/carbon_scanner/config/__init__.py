from dotenv import load_dotenv
import os

# Load environment variables from the project's root directory
load_dotenv()


class Config:
    @property
    def GEMINI_API_KEY(self) -> str:
        return os.getenv("GEMINI_API_KEY", "")

    @property
    def DATABASE_URL(self) -> str:
        return os.getenv("DATABASE_URL", "/tmp/carbon_scanner.db")

    @property
    def SECRET_KEY(self) -> str:
        return os.getenv("SECRET_KEY", "")


config = Config()
