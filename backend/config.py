import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from root directory first, then local (local overrides root)
root_env = Path(__file__).parent.parent / '.env'
local_env = Path(__file__).parent / '.env'

load_dotenv(root_env)
load_dotenv(local_env, override=True)

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    SHOPSTYLE_PID = os.getenv('SHOPSTYLE_PID')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    PORT = int(os.getenv('PORT', 5000))

    @classmethod
    def validate(cls):
        """Check that all required config is present."""
        missing = []
        if not cls.OPENAI_API_KEY:
            missing.append('OPENAI_API_KEY')
        if not cls.SHOPSTYLE_PID:
            missing.append('SHOPSTYLE_PID')

        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

        return True
