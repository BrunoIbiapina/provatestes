from clients.base_client import BaseClient


class UserClient(BaseClient):
    """Cliente HTTP do recurso User da Petstore API.

    Cobre CRUD de usuarios, login/logout e criacao em lote (createWithList).
    Sobrescreve `delete` da base para preservar a assinatura `delete(username)`.
    """

    BASE = "/user"

    def create(self, payload: dict):
        """POST /user — cria um usuario. `payload` deve seguir `USER_SCHEMA`."""
        return self.post(self.BASE, json=payload)

    def create_with_list(self, payload: list):
        """POST /user/createWithList — cria varios usuarios numa unica chamada."""
        return self.post(f"{self.BASE}/createWithList", json=payload)

    def get_by_username(self, username: str):
        """GET /user/{username} — busca usuario pelo username."""
        return self.get(f"{self.BASE}/{username}")

    def update(self, username: str, payload: dict):
        """PUT /user/{username} — atualiza dados do usuario."""
        return self.put(f"{self.BASE}/{username}", json=payload)

    def delete(self, username: str):
        """DELETE /user/{username} — remove um usuario."""
        return super().delete(f"{self.BASE}/{username}")

    def login(self, username: str, password: str):
        """GET /user/login — autentica e retorna sessao logada."""
        return self.get(f"{self.BASE}/login", params={"username": username, "password": password})

    def logout(self):
        """GET /user/logout — encerra a sessao atual."""
        return self.get(f"{self.BASE}/logout")
