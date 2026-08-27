import feedparser
from schema import build_entity
from utils import clean_text, normalize_url

RSS_FEEDS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://venturebeat.com/category/ai/feed/",
]


def extract_news():
    records = []
    seen_urls = set()

    for feed_url in RSS_FEEDS:
        parsed = feedparser.parse(feed_url)

        if not parsed.entries:
            print(f"No entries found for feed: {feed_url}")
            continue

        feed_title = parsed.feed.get("title", feed_url)

        for entry in parsed.entries[:20]:
            url = normalize_url(entry.get("link", ""))
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)

            record = build_entity(
                entity_type="news",
                name=clean_text(entry.get("title", "")),
                description=clean_text(entry.get("summary", "")),
                url=url,
                categories=["News"],
                source_name=feed_title,
                source_url=feed_url,
                extra={
                    "published": entry.get("published", ""),
                },
            )
            records.append(record)

    return records


if __name__ == "__main__":
    results = extract_news()
    print(f"Got {len(results)} records")
    if results:
        print(results[0])
        