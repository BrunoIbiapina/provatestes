from clients.base_client import BaseClient


class PetClient(BaseClient):
    """Cliente HTTP do recurso Pet da Petstore API.

    Cobre criacao, leitura individual, atualizacao (PUT e formulario), exclusao
    e buscas por status / tags. Todas as respostas sao retornadas como
    `requests.Response` para que o teste valide status, schema e payload.
    """

    BASE = "/pet"

    def create(self, payload: dict):
        """POST /pet — cria um pet. `payload` deve seguir `PET_SCHEMA`."""
        return self.post(self.BASE, json=payload)

    def get_by_id(self, pet_id: int):
        """GET /pet/{id} — busca um pet pelo identificador."""
        return self.get(f"{self.BASE}/{pet_id}")

    def update(self, payload: dict):
        """PUT /pet — atualiza um pet existente (payload completo)."""
        return self.put(self.BASE, json=payload)

    def delete_by_id(self, pet_id: int):
        """DELETE /pet/{id} — remove um pet."""
        return self.delete(f"{self.BASE}/{pet_id}")

    def find_by_status(self, status: str):
        """GET /pet/findByStatus — lista pets por status (`available`, `pending`, `sold`)."""
        return self.get(f"{self.BASE}/findByStatus", params={"status": status})

    def find_by_tags(self, tags: list):
        """GET /pet/findByTags — lista pets por tags."""
        return self.get(f"{self.BASE}/findByTags", params={"tags": tags})

    def update_with_form(self, pet_id: int, name: str, status: str):
        """POST /pet/{id} — atualiza nome/status via formulario url-encoded."""
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        return self.post(
            f"{self.BASE}/{pet_id}",
            data={"name": name, "status": status},
            headers=headers,
        )
