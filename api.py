from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from core.iptv_client import IPTVClient, IPTVError
from core.channel_manager import normalize_live
from core.stremio_builder import (
    build_manifest, build_catalogs, build_metas, catalog_id_for
)

app = FastAPI(title="Private IPTV Stremio Addon", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=False,
    allow_methods=["GET"], allow_headers=["*"],
)

def load_live_data():
    client = IPTVClient()
    categories = client.live_categories()
    streams = client.live_streams()
    return client, normalize_live(streams, categories)

@app.get("/")
def root():
    return {"service": "Private IPTV Stremio Addon", "manifest": "/manifest.json"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/manifest.json")
def manifest():
    try:
        _, channels = load_live_data()
        cats = sorted({c["category"] for c in channels}, key=str.casefold)
        return build_manifest(build_catalogs(cats))
    except IPTVError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

@app.get("/catalog/tv/{catalog_id}.json")
def catalog(catalog_id: str):
    try:
        _, channels = load_live_data()
        categories = sorted({c["category"] for c in channels}, key=str.casefold)
        matching = next((cat for cat in categories if catalog_id_for(cat) == catalog_id), None)
        if matching is None:
            raise HTTPException(status_code=404, detail="Catálogo não encontrado.")
        return {"metas": build_metas(channels, matching)}
    except IPTVError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

@app.get("/meta/tv/{meta_id}.json")
def meta(meta_id: str):
    channel_id = meta_id.removeprefix("iptv:")
    try:
        _, channels = load_live_data()
        channel = next((c for c in channels if c["id"] == channel_id), None)
        if not channel:
            raise HTTPException(status_code=404, detail="Canal não encontrado.")
        return {"meta": build_metas([channel], channel["category"])[0]}
    except IPTVError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

@app.get("/stream/tv/{meta_id}.json")
def stream(meta_id: str):
    channel_id = meta_id.removeprefix("iptv:")
    try:
        client, channels = load_live_data()
        channel = next((c for c in channels if c["id"] == channel_id), None)
        if not channel:
            raise HTTPException(status_code=404, detail="Canal não encontrado.")
        # URL de reprodução derivada do ID retornado pelo provedor; não aceitar URL arbitrária do cliente.
        url = client.live_stream_url(channel_id, "ts")
        return {"streams": [{"title": channel["name"], "url": url}]}
    except IPTVError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
