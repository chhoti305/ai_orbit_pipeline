import requests
from schema import build_entity
from utils import clean_text, normalize_url

GITHUB_API = "https://api.github.com/search/repositories"
SEARCH_TERMS = ["mcp-server", "llm agent", "ai-agent framework", "rag pipeline", "computer vision ai", "text to speech ai", "vector database ai", "ai chatbot framework"]
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

            record = build_entity(
                entity_type="repository",
                name=repo.get("name", ""),
                description=clean_text(repo.get("description", "")),
                url=url,
                categories=["Repositories"],
                source_name="GitHub",
                source_url=url,
                extra={
                    "stars": repo.get("stargazers_count", 0),
                    "language": repo.get("language"),
                },
            )
            records.append(record)

    return records


if __name__ == "__main__":
    results = extract_github_repos()
    print(f"Got {len(results)} records")
    if results:
        print(results[0])