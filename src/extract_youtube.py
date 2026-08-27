import os
import requests
from schema import build_entity
from utils import clean_text, normalize_url

YOUTUBE_API = "https://www.googleapis.com/youtube/v3/search"

SEARCH_TERMS = [
    "AI tool demo 2026",
    "MCP server tutorial",
    "AI agent framework tutorial",
    "new AI model review",
    "AI coding assistant demo",
    "text to speech AI tool",
]


def extract_youtube_videos():
    """
    Requires a free API key from console.cloud.google.com
    (enable 'YouTube Data API v3', create an API key).
    Set it as an environment variable before running:
        setx YOUTUBE_API_KEY "your-key-here"      (Windows, new terminal after)
        export YOUTUBE_API_KEY="your-key-here"    (Mac/Linux)
    """
    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        print("YOUTUBE_API_KEY not set — skipping video extraction.")
        return []

    records = []
    seen_ids = set()

    for term in SEARCH_TERMS:
        params = {
            "part": "snippet",
            "q": term,
            "type": "video",
            "maxResults": 10,
            "order": "relevance",
            "key": api_key,
        }
        response = requests.get(YOUTUBE_API, params=params, timeout=15)

        if response.status_code != 200:
            print(f"YouTube request failed for '{term}': {response.status_code} {response.text[:200]}")
            continue

        items = response.json().get("items", [])

        for item in items:
            video_id = item.get("id", {}).get("videoId")
            if not video_id or video_id in seen_ids:
                continue
            seen_ids.add(video_id)

            snippet = item.get("snippet", {})
            url = normalize_url(f"https://www.youtube.com/watch?v={video_id}")

            record = build_entity(
                entity_type="video",
                name=clean_text(snippet.get("title", "")),
                description=clean_text(snippet.get("description", "")),
                url=url,
                categories=["Videos"],
                source_name="YouTube",
                source_url=url,
                extra={
                    "channel": snippet.get("channelTitle"),
                    "published_at": snippet.get("publishedAt"),  # used later to tag "new"
                },
            )
            records.append(record)

    return records


if __name__ == "__main__":
    results = extract_youtube_videos()
    print(f"Got {len(results)} records")
    if results:
        print(results[0])