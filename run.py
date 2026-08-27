import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from extract_github import extract_github_repos
from extract_huggingface import extract_huggingface_models
from extract_news import extract_news
from companies import get_companies
from extract_youtube import extract_youtube_videos
from curated_entities import get_curated_entities
from postprocess import tag_recently_added, build_collections

all_records = []
all_records += extract_github_repos()
all_records += extract_huggingface_models()
all_records += extract_news()
all_records += get_companies()
all_records += extract_youtube_videos()
all_records += get_curated_entities()

all_records = tag_recently_added(all_records, days=30)
all_records += build_collections(all_records)
from dedupe import deduplicate
from relationships import build_relationships
from validate import validate_records
import json
import os

all_records = deduplicate(all_records)
valid_records, validation_issues = validate_records(all_records)
relationships = build_relationships(valid_records)

os.makedirs("data", exist_ok=True)

with open("data/entities.json", "w", encoding="utf-8") as f:
    json.dump(valid_records, f, indent=2, ensure_ascii=False)

with open("data/relationships.json", "w", encoding="utf-8") as f:
    json.dump(relationships, f, indent=2, ensure_ascii=False)

with open("data/validation_issues.json", "w", encoding="utf-8") as f:
    json.dump(validation_issues, f, indent=2, ensure_ascii=False)

print(f"Saved {len(valid_records)} entities and {len(relationships)} relationships.")