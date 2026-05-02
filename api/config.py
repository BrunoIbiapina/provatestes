import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_URL = os.getenv("BASE_URL", "https://petstore.swagger.io/v2")
    TIMEOUT = int(os.getenv("TIMEOUT", "30"))
    DEFAULT_HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
