import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from extract_github import extract_github_repos
from extract_huggingface import extract_huggingface_models
from extract_news import extract_news
from companies import get_companies
from dedupe import deduplicate
from relationships import build_relationships
from validate import validate_records


def run_pipeline():
    print("Starting AI Orbit Pipeline...")

    all_records = []

    print("Collecting from GitHub...")
    all_records.extend(extract_github_repos())

    print("Collecting from Hugging Face...")
    all_records.extend(extract_huggingface_models())

    print("Collecting from News...")
    all_records.extend(extract_news())
    
    print("Adding curated companies list...")
    all_records.extend(get_companies())

    print(f"Total raw records: {len(all_records)}")

    print("Removing duplicates...")
    all_records = deduplicate(all_records)
    print(f"Records after dedup: {len(all_records)}")

    print("Building relationships...")
    relationships = build_relationships(all_records)

    print("Validating records...")
    valid_records, issues = validate_records(all_records)

    os.makedirs("data", exist_ok=True)

    with open("data/entities.json", "w", encoding="utf-8") as f:
        json.dump(valid_records, f, indent=2, ensure_ascii=False)

    with open("data/relationships.json", "w", encoding="utf-8") as f:
        json.dump(relationships, f, indent=2, ensure_ascii=False)

    with open("data/validation_issues.json", "w", encoding="utf-8") as f:
        json.dump(issues, f, indent=2, ensure_ascii=False)

    print(f"\nDone! Saved {len(valid_records)} entities and {len(relationships)} relationships.")
    print("Check the 'data' folder for your output files.")


if __name__ == "__main__":
    run_pipeline()