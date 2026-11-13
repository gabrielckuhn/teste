import requests
from config import (
    IPTV_BASE_URL, IPTV_USERNAME, IPTV_PASSWORD, REQUEST_TIMEOUT_SECONDS
)

class IPTVError(RuntimeError):
    pass

class IPTVClient:
    """Cliente mínimo Xtream Codes API. Use apenas com uma conta autorizada."""

    def __init__(self):
        if not all([IPTV_BASE_URL, IPTV_USERNAME, IPTV_PASSWORD]):
            raise IPTVError("Configure IPTV_BASE_URL, IPTV_USERNAME e IPTV_PASSWORD no .env.")
        self.base = IPTV_BASE_URL
        self.username = IPTV_USERNAME
        self.password = IPTV_PASSWORD
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Private-Stremio-Addon/1.0"})

    def _get(self, params):
        params.update({"username": self.username, "password": self.password})
        try:
            response = self.session.get(
                f"{self.base}/player_api.php",
                params=params,
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            raise IPTVError(f"Falha ao consultar o servidor IPTV: {exc}") from exc
        except ValueError as exc:
            raise IPTVError("O servidor não retornou JSON válido.") from exc

    def account_info(self):
        return self._get({})

    def live_categories(self):
        return self._get({"action": "get_live_categories"})

    def live_streams(self, category_id=None):
        params = {"action": "get_live_streams"}
        if category_id is not None:
            params["category_id"] = category_id
        return self._get(params)

    def vod_categories(self):
        return self._get({"action": "get_vod_categories"})

    def vod_streams(self, category_id=None):
        params = {"action": "get_vod_streams"}
        if category_id is not None:
            params["category_id"] = category_id
        return self._get(params)

    def series_categories(self):
        return self._get({"action": "get_series_categories"})

    def series(self, category_id=None):
        params = {"action": "get_series"}
        if category_id is not None:
            params["category_id"] = category_id
        return self._get(params)

    def live_stream_url(self, stream_id, extension="ts"):
        return f"{self.base}/live/{self.username}/{self.password}/{stream_id}.{extension}"

    def vod_stream_url(self, stream_id, extension="mp4"):
        return f"{self.base}/movie/{self.username}/{self.password}/{stream_id}.{extension}"
