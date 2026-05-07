"""Factories de dados para os testes de API.

Cada `build_*` retorna um dicionario novo com IDs e campos aleatorios,
garantindo que execucoes paralelas e repetidas nao colidam entre si.
Usa Faker para gerar nomes/emails/etc realistas.
"""
import random
from datetime import datetime, timezone
from faker import Faker

fake = Faker()


def build_pet(status: str = "available") -> dict:
    """Gera payload valido para POST /pet com ID aleatorio.

    Args:
        status: Status inicial do pet (`available`, `pending` ou `sold`).
    """
    return {
        "id": random.randint(10**8, 10**9),
        "category": {"id": random.randint(1, 100), "name": fake.word()},
        "name": fake.first_name(),
        "photoUrls": [fake.image_url()],
        "tags": [{"id": random.randint(1, 100), "name": fake.word()}],
        "status": status,
    }


def build_order(pet_id: int) -> dict:
    """Gera payload valido para POST /store/order vinculado a um pet.

    Args:
        pet_id: Identificador de um pet existente (geralmente vindo de `build_pet`).
    """
    return {
        "id": random.randint(1, 10),
        "petId": pet_id,
        "quantity": random.randint(1, 5),
        "shipDate": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000+0000"),
        "status": "placed",
        "complete": True,
    }


def build_user() -> dict:
    """Gera payload valido para POST /user com username unico."""
    return {
        "id": random.randint(10**6, 10**7),
        "username": fake.user_name() + str(random.randint(1000, 9999)),
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "email": fake.email(),
        "password": fake.password(length=10),
        "phone": fake.msisdn(),
        "userStatus": 1,
    }
