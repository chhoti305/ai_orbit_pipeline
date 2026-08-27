import requests
from schema import build_entity
from utils import clean_text, normalize_url

GITHUB_API = "https://api.github.com/search/repositories"
SEARCH_TERMS = ["mcp-server", "llm agent", "ai-agent framework", "rag pipeline", "computer vision ai", "text to speech ai", "vector database ai", "ai chatbot framework"]

# Queries that should be classified as MCP entities rather than plain repos.
MCP_QUERIES = {"mcp-server"}

# Keywords in a repo description that suggest it's an end-user Tool
# rather than just a raw library/repository.
TOOL_KEYWORDS = ["app", "platform", "no-code", "saas", "dashboard", "extension", "plugin", "ui for"]


def extract_github_repos():
    records = []
    seen_urls = set()

    for query in SEARCH_TERMS:
        params = {"q": query, "sort": "stars", "order": "desc", "per_page": 15}
        response = requests.get(GITHUB_API, params=params, timeout=15)

        if response.status_code != 200:
            print(f"GitHub request failed for '{query}': {response.status_code}")
            continue

        items = response.json().get("items", [])

        for repo in items:
            url = normalize_url(repo.get("html_url", ""))
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)

            description = clean_text(repo.get("description", ""))
            is_mcp = query in MCP_QUERIES
            is_tool = any(kw in description.lower() for kw in TOOL_KEYWORDS)

            categories = ["Repositories"]
            entity_type = "repository"
            if is_mcp:
                entity_type = "mcp"
                categories = ["MCP", "Repositories"]
            elif is_tool:
                categories = ["Repositories", "Tools"]

            record = build_entity(
                entity_type=entity_type,
                name=repo.get("name", ""),
                description=description,
                url=url,
                categories=categories,
                source_name="GitHub",
                source_url=url,
                extra={
                    "stars": repo.get("stargazers_count", 0),
                    "language": repo.get("language"),
                    "pushed_at": repo.get("pushed_at"),  # used later to tag "new"
                },
            )
            records.append(record)

    return records


if __name__ == "__main__":
    results = extract_github_repos()
    print(f"Got {len(results)} records")
    by_type = {}
    for r in results:
        by_type[r["entity_type"]] = by_type.get(r["entity_type"], 0) + 1
    print(by_type)