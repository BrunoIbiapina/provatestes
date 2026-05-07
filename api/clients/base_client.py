import logging
import requests
from config import Config

logger = logging.getLogger(__name__)


class BaseClient:
    """Cliente HTTP base reaproveitado por todos os clientes de recurso da API.

    Centraliza session com keep-alive, headers padrao, timeout configuravel e
    logging estruturado de cada request (metodo, URL, status, tempo de resposta).

    Subclasses devem definir uma constante BASE com o prefixo do recurso
    (ex.: "/pet") e expor metodos de negocio que delegam para get/post/put/delete.
    """

    def __init__(self, base_url: str = Config.BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(Config.DEFAULT_HEADERS)

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        """Executa o request com timeout default e logging padronizado."""
        url = f"{self.base_url}{path}"
        kwargs.setdefault("timeout", Config.TIMEOUT)
        logger.info("%s %s", method, url)
        response = self.session.request(method, url, **kwargs)
        logger.info("Status: %s | Tempo: %.2fs", response.status_code, response.elapsed.total_seconds())
        return response

    def get(self, path: str, **kwargs):
        """GET no recurso. `path` e relativo ao `base_url`."""
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs):
        """POST no recurso. Aceita `json=`, `data=`, `headers=` etc."""
        return self._request("POST", path, **kwargs)

    def put(self, path: str, **kwargs):
        """PUT no recurso. Geralmente usado com `json=` para atualizacao."""
        return self._request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs):
        """DELETE no recurso."""
        return self._request("DELETE", path, **kwargs)
