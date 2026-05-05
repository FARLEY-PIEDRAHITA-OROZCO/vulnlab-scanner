import os
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

class Config:
    TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", 5))
    USER_AGENT = os.getenv("USER_AGENT", "VulnLabScanner/1.0")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"