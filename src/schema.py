import uuid

def build_entity(entity_type, name, description, url, categories, source_name, source_url, extra=None):
    record = {
        "id": str(uuid.uuid4()),
        "entity_type": entity_type,
        "name": (name or "").strip(),
        "description": (description or "").strip(),
        "url": (url or "").strip(),
        "categories": categories or [],
        "source": {
            "name": source_name,
            "url": source_url,
        },
    }
    if extra:
        record["metadata"] = extra
    return record