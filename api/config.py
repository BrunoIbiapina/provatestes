import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuracao do projeto de API, carregada de variaveis de ambiente.

    Variaveis suportadas (com default sensato para execucao local):
        BASE_URL: URL base da API (default: Petstore publica).
        TIMEOUT: timeout de cada request em segundos.
    """

    BASE_URL = os.getenv("BASE_URL", "https://petstore.swagger.io/v2")
    TIMEOUT = int(os.getenv("TIMEOUT", "30"))
    DEFAULT_HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
