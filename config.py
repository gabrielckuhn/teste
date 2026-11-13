import os
from dotenv import load_dotenv

load_dotenv()

IPTV_BASE_URL = os.getenv("IPTV_BASE_URL", "").rstrip("/")
IPTV_USERNAME = os.getenv("IPTV_USERNAME", "")
IPTV_PASSWORD = os.getenv("IPTV_PASSWORD", "")
ADDON_PUBLIC_URL = os.getenv("ADDON_PUBLIC_URL", "http://127.0.0.1:8000").rstrip("/")
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "900"))
REQUEST_TIMEOUT_SECONDS = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "20"))

def credentials_configured() -> bool:
    return all([IPTV_BASE_URL, IPTV_USERNAME, IPTV_PASSWORD])
