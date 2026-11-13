from collections import defaultdict

def normalize_categories(categories):
    return {
        str(item.get("category_id")): item.get("category_name") or "Sem categoria"
        for item in (categories or [])
        if item.get("category_id") is not None
    }

def normalize_live(streams, categories):
    category_map = normalize_categories(categories)
    result = []
    for item in streams or []:
        stream_id = item.get("stream_id")
        if stream_id is None:
            continue
        category_id = str(item.get("category_id", ""))
        result.append({
            "id": str(stream_id),
            "name": item.get("name") or f"Canal {stream_id}",
            "category": category_map.get(category_id, "Sem categoria"),
            "logo": item.get("stream_icon") or "",
            "epg_id": item.get("epg_channel_id") or "",
            "kind": "live",
        })
    return result

def group_items(items):
    groups = defaultdict(list)
    for item in items:
        groups[item.get("category") or "Sem categoria"].append(item)
    return dict(groups)
