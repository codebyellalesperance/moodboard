"""Application configuration."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Flask configuration variables."""

    # Flask
    DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'
    PORT = int(os.getenv('PORT', 5000))

    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    # ShopStyle
    SHOPSTYLE_PID = os.getenv('SHOPSTYLE_PID')

    # Limits
    MAX_IMAGES = 5
    MAX_IMAGE_SIZE_MB = 5
    MAX_PROMPT_LENGTH = 200
