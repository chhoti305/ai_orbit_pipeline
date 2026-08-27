from datetime import datetime, timedelta, timezone
from schema import build_entity


def tag_recently_added(records, days=30):
    """
    Looks at whichever date field each record has (pushed_at, last_modified,
    published_at) and adds "New" to its categories list if within `days`.
    Mutates and returns the same list — no new entities, just a category tag.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    date_fields = ["pushed_at", "last_modified", "published_at"]

    for record in records:
        meta = record.get("metadata", {}) or {}
        raw_date = None
        for field in date_fields:
            if meta.get(field):
                raw_date = meta[field]
                break
        if not raw_date:
            continue

        try:
            parsed = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            continue

        if parsed >= cutoff and "New" not in record["categories"]:
            record["categories"].append("New")

    return records


def build_collections(records):
    """
    Groups existing records into a couple of curated Collection entities.
    Each Collection links out via metadata["entity_ids"] to records already
    in the dataset — satisfies the Collections category without a new source.
    """
    collections = []

    models = [r for r in records if r["entity_type"] == "model"]
    top_models = sorted(models, key=lambda r: r.get("metadata", {}).get("downloads", 0), reverse=True)[:8]
    if top_models:
        collections.append(build_entity(
            entity_type="collection",
            name="Most Downloaded Models",
            description="Highest-download Hugging Face models found in this dataset",
            url="",
            categories=["Collections"],
            source_name="AI Orbit Pipeline",
            source_url="",
            extra={"entity_ids": [m["id"] for m in top_models]},
        ))

    repos = [r for r in records if r["entity_type"] == "repository"]
    top_repos = sorted(repos, key=lambda r: r.get("metadata", {}).get("stars", 0), reverse=True)[:8]
    if top_repos:
        collections.append(build_entity(
            entity_type="collection",
            name="Trending AI Repositories",
            description="Highest-starred AI repositories found in this dataset",
            url="",
            categories=["Collections"],
            source_name="AI Orbit Pipeline",
            source_url="",
            extra={"entity_ids": [r["id"] for r in top_repos]},
        ))

    mcp_entities = [r for r in records if r["entity_type"] == "mcp"]
    if mcp_entities:
        collections.append(build_entity(
            entity_type="collection",
            name="MCP Server Directory",
            description="MCP servers found in this dataset",
            url="",
            categories=["Collections", "MCP"],
            source_name="AI Orbit Pipeline",
            source_url="",
            extra={"entity_ids": [m["id"] for m in mcp_entities]},
        ))

    return collections