import allure
import pytest
from jsonschema import validate

from data.factories import build_pet
from schemas.pet_schema import PET_SCHEMA, PET_LIST_SCHEMA


@allure.epic("Petstore API")
@allure.feature("Pet")
class TestPet:

    @allure.story("Criar pet com sucesso")
    @pytest.mark.smoke
    @pytest.mark.pet
    def test_create_pet(self, pet_client):
        payload = build_pet()
        response = pet_client.create(payload)

        assert response.status_code == 200
        body = response.json()
        validate(instance=body, schema=PET_SCHEMA)
        assert body["name"] == payload["name"]
        assert body["status"] == "available"

        pet_client.delete_by_id(payload["id"])

    @allure.story("Buscar pet por ID")
    @pytest.mark.smoke
    @pytest.mark.pet
    def test_get_pet_by_id(self, pet_client, new_pet):
        response = pet_client.get_by_id(new_pet["id"])

        assert response.status_code == 200
        validate(instance=response.json(), schema=PET_SCHEMA)
        assert response.json()["id"] == new_pet["id"]

    @allure.story("Atualizar pet via PUT")
    @pytest.mark.regression
    @pytest.mark.pet
    def test_update_pet(self, pet_client, new_pet):
        new_pet["name"] = "PetAtualizado"
        new_pet["status"] = "sold"

        response = pet_client.update(new_pet)

        assert response.status_code == 200
        body = response.json()
        assert body["name"] == "PetAtualizado"
        assert body["status"] == "sold"

    @allure.story("Atualizar pet via formulario")
    @pytest.mark.regression
    @pytest.mark.pet
    def test_update_pet_with_form(self, pet_client, new_pet):
        response = pet_client.update_with_form(new_pet["id"], "NovoNome", "pending")
        assert response.status_code == 200

    @allure.story("Deletar pet")
    @pytest.mark.smoke
    @pytest.mark.pet
    def test_delete_pet(self, pet_client):
        payload = build_pet()
        pet_client.create(payload)

        response = pet_client.delete_by_id(payload["id"])
        assert response.status_code == 200

        get_response = pet_client.get_by_id(payload["id"])
        assert get_response.status_code == 404

    @allure.story("Buscar pets por status")
    @pytest.mark.regression
    @pytest.mark.pet
    @pytest.mark.parametrize("status", ["available", "pending", "sold"])
    def test_find_by_status(self, pet_client, status):
        response = pet_client.find_by_status(status)

        assert response.status_code == 200
        body = response.json()
        validate(instance=body, schema=PET_LIST_SCHEMA)
        assert all(p.get("status") == status for p in body if "status" in p)

    @allure.story("Cenario negativo: pet inexistente")
    @pytest.mark.negative
    @pytest.mark.pet
    def test_get_pet_not_found(self, pet_client):
        response = pet_client.get_by_id(0)
        assert response.status_code == 404

    @allure.story("Cenario negativo: deletar pet inexistente")
    @pytest.mark.negative
    @pytest.mark.pet
    def test_delete_pet_not_found(self, pet_client):
        response = pet_client.delete_by_id(0)
        assert response.status_code in (404, 400)

    @allure.story("Tempo de resposta aceitavel")
    @pytest.mark.regression
    @pytest.mark.pet
    def test_response_time(self, pet_client):
        response = pet_client.find_by_status("available")
        assert response.elapsed.total_seconds() < 5
