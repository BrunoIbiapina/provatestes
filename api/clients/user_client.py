from clients.base_client import BaseClient


class UserClient(BaseClient):
    BASE = "/user"

    def create(self, payload: dict):
        return self.post(self.BASE, json=payload)

    def create_with_list(self, payload: list):
        return self.post(f"{self.BASE}/createWithList", json=payload)

    def get_by_username(self, username: str):
        return self.get(f"{self.BASE}/{username}")

    def update(self, username: str, payload: dict):
        return self.put(f"{self.BASE}/{username}", json=payload)

    def delete(self, username: str):
        return super().delete(f"{self.BASE}/{username}")

    def login(self, username: str, password: str):
        return self.get(f"{self.BASE}/login", params={"username": username, "password": password})

    def logout(self):
        return self.get(f"{self.BASE}/logout")
