import sys
import logging
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from clients.pet_client import PetClient
from clients.store_client import StoreClient
from clients.user_client import UserClient
from data.factories import build_pet, build_order, build_user

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")


@pytest.fixture(scope="session")
def pet_client():
    return PetClient()


@pytest.fixture(scope="session")
def store_client():
    return StoreClient()


@pytest.fixture(scope="session")
def user_client():
    return UserClient()


@pytest.fixture
def new_pet(pet_client):
    payload = build_pet()
    response = pet_client.create(payload)
    assert response.status_code == 200, f"Falha ao criar pet: {response.text}"
    yield response.json()
    pet_client.delete_by_id(payload["id"])


@pytest.fixture
def new_order(store_client, new_pet):
    payload = build_order(new_pet["id"])
    response = store_client.place_order(payload)
    assert response.status_code == 200, f"Falha ao criar order: {response.text}"
    yield response.json()
    store_client.delete_order(payload["id"])


@pytest.fixture
def new_user(user_client):
    payload = build_user()
    response = user_client.create(payload)
    assert response.status_code == 200, f"Falha ao criar user: {response.text}"
    yield payload
    user_client.delete(payload["username"])
