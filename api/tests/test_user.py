import allure
import pytest
from jsonschema import validate

from data.factories import build_user
from schemas.user_schema import USER_SCHEMA


@allure.epic("Petstore API")
@allure.feature("User")
class TestUser:

    @allure.story("Criar user")
    @pytest.mark.smoke
    @pytest.mark.user
    def test_create_user(self, user_client):
        payload = build_user()
        response = user_client.create(payload)

        assert response.status_code == 200
        assert response.json().get("message") == str(payload["id"])

        user_client.delete(payload["username"])

    @allure.story("Buscar user por username")
    @pytest.mark.smoke
    @pytest.mark.user
    def test_get_user(self, user_client, new_user):
        response = user_client.get_by_username(new_user["username"])

        assert response.status_code == 200
        validate(instance=response.json(), schema=USER_SCHEMA)
        assert response.json()["username"] == new_user["username"]

    @allure.story("Atualizar user")
    @pytest.mark.regression
    @pytest.mark.user
    def test_update_user(self, user_client, new_user):
        new_user["firstName"] = "NovoNome"
        new_user["email"] = "novo@email.com"

        response = user_client.update(new_user["username"], new_user)
        assert response.status_code == 200

        get_response = user_client.get_by_username(new_user["username"])
        assert get_response.json()["firstName"] == "NovoNome"

    @allure.story("Deletar user")
    @pytest.mark.regression
    @pytest.mark.user
    def test_delete_user(self, user_client):
        payload = build_user()
        user_client.create(payload)

        response = user_client.delete(payload["username"])
        assert response.status_code == 200

        get_response = user_client.get_by_username(payload["username"])
        assert get_response.status_code == 404

    @allure.story("Login do user")
    @pytest.mark.smoke
    @pytest.mark.user
    def test_login(self, user_client, new_user):
        response = user_client.login(new_user["username"], new_user["password"])

        assert response.status_code == 200
        assert "logged in user session" in response.json().get("message", "")

    @allure.story("Logout do user")
    @pytest.mark.regression
    @pytest.mark.user
    def test_logout(self, user_client):
        response = user_client.logout()
        assert response.status_code == 200

    @allure.story("Criar lista de users")
    @pytest.mark.regression
    @pytest.mark.user
    def test_create_with_list(self, user_client):
        users = [build_user() for _ in range(3)]
        response = user_client.create_with_list(users)

        assert response.status_code == 200
        for u in users:
            user_client.delete(u["username"])

    @allure.story("Cenario negativo: user inexistente")
    @pytest.mark.negative
    @pytest.mark.user
    def test_get_user_not_found(self, user_client):
        response = user_client.get_by_username("usuario_inexistente_12345")
        assert response.status_code == 404
