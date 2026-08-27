import re


def _name_in_text(name, text):
    """Match name as a whole word only, not hidden inside other words."""
    if not name or not text:
        return False
    if len(name.strip()) < 4:
        return False  # skip short/generic names like "pi", "Go", "C"
    pattern = r"\b" + re.escape(name.strip()) + r"\b"
    return re.search(pattern, text, re.IGNORECASE) is not None


def build_relationships(records):
    relationships = []

    by_type = {}
    for r in records:
        by_type.setdefault(r["entity_type"], []).append(r)

    companies = by_type.get("company", [])
    models = by_type.get("model", [])
    repos = by_type.get("repository", [])

    # Company --develops--> Model (check provider metadata field)
    for company in companies:
        for model in models:
            provider = (model.get("metadata", {}) or {}).get("provider", "")
            if _name_in_text(company["name"], provider) or _name_in_text(company["name"], model["description"]):
                relationships.append({
                    "from": company["id"],
                    "from_name": company["name"],
                    "relation": "develops",
                    "to": model["id"],
                    "to_name": model["name"],
                })

    # Company --develops--> Repository (check description mentions)
    for company in companies:
        for repo in repos:
            if _name_in_text(company["name"], repo["description"]):
                relationships.append({
                    "from": company["id"],
                    "from_name": company["name"],
                    "relation": "develops",
                    "to": repo["id"],
                    "to_name": repo["name"],
                })

    return relationships