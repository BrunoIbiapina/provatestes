from clients.base_client import BaseClient


class StoreClient(BaseClient):
    """Cliente HTTP do recurso Store da Petstore API.

    Cobre consulta de inventario e CRUD de orders.
    """

    BASE = "/store"

    def get_inventory(self):
        """GET /store/inventory — retorna mapa de status -> quantidade."""
        return self.get(f"{self.BASE}/inventory")

    def place_order(self, payload: dict):
        """POST /store/order — cria uma order. `payload` deve seguir `ORDER_SCHEMA`."""
        return self.post(f"{self.BASE}/order", json=payload)

    def get_order(self, order_id: int):
        """GET /store/order/{id} — busca uma order pelo id."""
        return self.get(f"{self.BASE}/order/{order_id}")

    def delete_order(self, order_id: int):
        """DELETE /store/order/{id} — remove uma order."""
        return self.delete(f"{self.BASE}/order/{order_id}")
