import allure
import pytest
from jsonschema import validate

from data.factories import build_order
from schemas.store_schema import ORDER_SCHEMA, INVENTORY_SCHEMA


@allure.epic("Petstore API")
@allure.feature("Store")
class TestStore:

    @allure.story("Buscar inventario")
    @pytest.mark.smoke
    @pytest.mark.store
    def test_get_inventory(self, store_client):
        response = store_client.get_inventory()

        assert response.status_code == 200
        validate(instance=response.json(), schema=INVENTORY_SCHEMA)

    @allure.story("Criar order")
    @pytest.mark.smoke
    @pytest.mark.store
    def test_place_order(self, store_client, new_pet):
        payload = build_order(new_pet["id"])
        response = store_client.place_order(payload)

        assert response.status_code == 200
        validate(instance=response.json(), schema=ORDER_SCHEMA)
        assert response.json()["petId"] == new_pet["id"]

        store_client.delete_order(payload["id"])

    @allure.story("Buscar order por ID")
    @pytest.mark.smoke
    @pytest.mark.store
    def test_get_order(self, store_client, new_order):
        response = store_client.get_order(new_order["id"])

        assert response.status_code == 200
        validate(instance=response.json(), schema=ORDER_SCHEMA)
        assert response.json()["id"] == new_order["id"]

    @allure.story("Deletar order")
    @pytest.mark.regression
    @pytest.mark.store
    def test_delete_order(self, store_client, new_pet):
        payload = build_order(new_pet["id"])
        store_client.place_order(payload)

        response = store_client.delete_order(payload["id"])
        assert response.status_code == 200

        get_response = store_client.get_order(payload["id"])
        assert get_response.status_code == 404

    @allure.story("Cenario negativo: order inexistente")
    @pytest.mark.negative
    @pytest.mark.store
    def test_get_order_not_found(self, store_client):
        response = store_client.get_order(99999999)
        assert response.status_code == 404

    @allure.story("Cenario negativo: ID invalido")
    @pytest.mark.negative
    @pytest.mark.store
    def test_get_order_invalid_id(self, store_client):
        response = store_client.get_order(-1)
        assert response.status_code in (400, 404)
