from clients.base_client import BaseClient


class StoreClient(BaseClient):
    BASE = "/store"

    def get_inventory(self):
        return self.get(f"{self.BASE}/inventory")

    def place_order(self, payload: dict):
        return self.post(f"{self.BASE}/order", json=payload)

    def get_order(self, order_id: int):
        return self.get(f"{self.BASE}/order/{order_id}")

    def delete_order(self, order_id: int):
        return self.delete(f"{self.BASE}/order/{order_id}")
