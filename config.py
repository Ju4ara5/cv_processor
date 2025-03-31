import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Конфигурация приложения"""
    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")
    SPREADSHEET_URL = os.getenv("SPREADSHEET_URL")
    TRANSLATE_TO_RUSSIAN = os.getenv("TRANSLATE_TO_RUSSIAN", "true").lower() == "true"
