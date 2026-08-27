REQUIRED_FIELDS = ["id", "entity_type", "name", "url"]


def validate_records(records):
    valid = []
    issues = []

    for r in records:
        missing = [f for f in REQUIRED_FIELDS if not r.get(f)]

        if "id" in missing or "name" in missing:
            issues.append(f"Dropped record (missing id/name): {r.get('url', 'no-url')}")
            continue

        if missing:
            issues.append(f"Record '{r['name']}' missing fields: {missing}")

        if not r.get("description"):
            issues.append(f"Record '{r['name']}' has no description.")

        valid.append(r)

    return valid, issues