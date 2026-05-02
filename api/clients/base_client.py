import logging
import requests
from config import Config

logger = logging.getLogger(__name__)


class BaseClient:
    def __init__(self, base_url: str = Config.BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(Config.DEFAULT_HEADERS)

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}"
        kwargs.setdefault("timeout", Config.TIMEOUT)
        logger.info("%s %s", method, url)
        response = self.session.request(method, url, **kwargs)
        logger.info("Status: %s | Tempo: %.2fs", response.status_code, response.elapsed.total_seconds())
        return response

    def get(self, path: str, **kwargs):
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs):
        return self._request("POST", path, **kwargs)

    def put(self, path: str, **kwargs):
        return self._request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs):
        return self._request("DELETE", path, **kwargs)
