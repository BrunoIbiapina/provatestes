import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")
    BROWSER = os.getenv("BROWSER", "chrome")
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "5"))
    EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "10"))

    STANDARD_USER = os.getenv("STANDARD_USER", "standard_user")
    LOCKED_USER = os.getenv("LOCKED_USER", "locked_out_user")
    PROBLEM_USER = os.getenv("PROBLEM_USER", "problem_user")
    PASSWORD = os.getenv("PASSWORD", "secret_sauce")
