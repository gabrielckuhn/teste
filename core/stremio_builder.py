import re
from config import ADDON_PUBLIC_URL

ADDON_ID = "br.private.iptv.catalog"
ADDON_NAME = "IPTV Privada"
ADDON_VERSION = "1.0.0"

def slugify(value):
    value = re.sub(r"[^a-zA-Z0-9_-]+", "-", str(value).strip().lower()).strip("-")
    return value or "outros"

def build_manifest(catalogs):
    return {
        "id": ADDON_ID,
        "version": ADDON_VERSION,
        "name": ADDON_NAME,
        "description": "Catálogos de TV ao vivo da sua fonte IPTV autorizada.",
        "resources": ["catalog", "stream"],
        "types": ["tv"],
        "idPrefixes": ["iptv:"],
        "catalogs": catalogs,
        "behaviorHints": {"configurable": False, "configurationRequired": False},
    }

def catalog_id_for(category):
    return "live-" + slugify(category)

def build_catalogs(categories):
    return [
        {
            "type": "tv",
            "id": catalog_id_for(category),
            "name": category,
        }
        for category in sorted(set(categories), key=str.casefold)
    ]

def build_metas(channels, category):
    metas = []
    for channel in channels:
        if channel["category"] != category:
            continue
        metas.append({
            "id": f"iptv:{channel['id']}",
            "type": "tv",
            "name": channel["name"],
            "poster": channel.get("logo") or None,
            "description": f"TV ao vivo · {channel['category']}",
            "genres": [channel["category"]],
            "behaviorHints": {"defaultVideoId": f"iptv:{channel['id']}"},
        })
    return metas
