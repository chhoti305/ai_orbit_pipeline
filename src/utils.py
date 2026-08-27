import re
import html
from urllib.parse import urlparse, urlunparse


def normalize_url(url):
    """Cleans up a URL - lowercase domain, no trailing slash, no tracking junk."""
    if not url:
        return ""
    try:
        parsed = urlparse(url.strip())
        scheme = "https" if parsed.scheme in ("http", "https", "") else parsed.scheme
        netloc = parsed.netloc.lower().replace("www.", "")
        path = parsed.path.rstrip("/")
        normalized = urlunparse((scheme, netloc, path, "", "", ""))
        return normalized
    except Exception:
        return url.strip()


def clean_text(text):
    """Removes HTML tags and extra spaces from text."""
    if not text:
        return ""
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text