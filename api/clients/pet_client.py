from clients.base_client import BaseClient


class PetClient(BaseClient):
    BASE = "/pet"

    def create(self, payload: dict):
        return self.post(self.BASE, json=payload)

    def get_by_id(self, pet_id: int):
        return self.get(f"{self.BASE}/{pet_id}")

    def update(self, payload: dict):
        return self.put(self.BASE, json=payload)

    def delete_by_id(self, pet_id: int):
        return self.delete(f"{self.BASE}/{pet_id}")

    def find_by_status(self, status: str):
        return self.get(f"{self.BASE}/findByStatus", params={"status": status})

    def find_by_tags(self, tags: list):
        return self.get(f"{self.BASE}/findByTags", params={"tags": tags})

    def update_with_form(self, pet_id: int, name: str, status: str):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        return self.post(
            f"{self.BASE}/{pet_id}",
            data={"name": name, "status": status},
            headers=headers,
        )
