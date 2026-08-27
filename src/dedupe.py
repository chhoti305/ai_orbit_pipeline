from rapidfuzz import fuzz

NAME_ALIASES = {
    "open ai": "OpenAI",
    "openai inc": "OpenAI",
    "hugging face": "Hugging Face",
    "huggingface": "Hugging Face",
}

FUZZY_THRESHOLD = 90


def canonicalize_name(name):
    if not name:
        return ""
    key = name.strip().lower()
    return NAME_ALIASES.get(key, name.strip())


def deduplicate(records):
    for r in records:
        r["name"] = canonicalize_name(r["name"])

    by_type = {}
    for r in records:
        by_type.setdefault(r["entity_type"], []).append(r)

    final_list = []

    for entity_type, group in by_type.items():
        resolved = []
        for record in group:
            match_found = False
            for existing in resolved:
                same_name = record["name"].lower() == existing["name"].lower()
                same_url = record["url"] and record["url"] == existing["url"]
                similar_name = fuzz.token_sort_ratio(record["name"], existing["name"]) >= FUZZY_THRESHOLD

                if same_name or same_url or similar_name:
                    if not existing["description"] and record["description"]:
                        existing["description"] = record["description"]
                    match_found = True
                    break

            if not match_found:
                resolved.append(record)

        final_list.extend(resolved)

    return final_list