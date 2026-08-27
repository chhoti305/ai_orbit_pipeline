# AI Orbit Ecosystem Data Ingestion Pipeline

## What This Project Does

This pipeline collects AI-ecosystem data — models, repositories, MCP servers, tasks, news, companies, robots, devices, personal assistants, creative tools, and curated collections — from a mix of free public APIs (GitHub, Hugging Face, RSS news feeds, YouTube) and hand-researched sources where no reliable free API exists. It combines everything into a single structured dataset, removes duplicates, detects relationships between entities (like which company built which model or tool), tags recently-updated entities, and validates every record before saving the final output.

## Project Structure

```
ai_orbit_pipeline/
├── run.py                        # Main entry point - runs the full pipeline
├── src/
│   ├── schema.py                 # Common record template (build_entity)
│   ├── utils.py                  # Helper functions (clean_text, normalize_url)
│   ├── extract_github.py         # Pulls repositories & MCP servers from GitHub Search API
│   ├── extract_huggingface.py    # Pulls models from Hugging Face Hub API + derives Task entities
│   ├── extract_news.py           # Pulls articles from TechCrunch AI + VentureBeat AI RSS feeds
│   ├── extract_youtube.py        # Pulls videos from YouTube Data API v3 (requires API key)
│   ├── companies.py              # Hand-curated list of 10 real AI companies
│   ├── curated_entities.py       # Hand-curated Robots, Devices, Personal, Creative entities
│   ├── postprocess.py            # Tags recently-added entities, builds Collections
│   ├── dedupe.py                 # Removes duplicate records (by name/URL/fuzzy match)
│   ├── relationships.py          # Detects relationships between entities
│   └── validate.py               # Validates records before saving
├── data/
│   ├── entities.json             # Final combined dataset
│   ├── relationships.json        # Detected relationships between entities
│   └── validation_issues.json    # Any validation issues found (empty = all clean)
├── logs/
└── venv/                         # Python virtual environment
```

## Setup Instructions

1. Create the project folder with `src`, `data`, and `logs` subfolders.
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\Activate.ps1
   ```
   (If PowerShell blocks this, run once: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`)
3. Install the required libraries:
   ```
   pip install requests feedparser rapidfuzz huggingface_hub
   ```
4. (Optional) Set a YouTube Data API v3 key to enable video extraction:
   ```
   $env:YOUTUBE_API_KEY="your-key-here"
   ```
   If not set, the pipeline logs a notice and continues without video data — it does not fail the run.
5. Run the pipeline from the main project folder (not inside `src`):
   ```
   python run.py
   ```
6. The pipeline will automatically:
   - Collect repositories and MCP servers from GitHub
   - Collect models from Hugging Face, deriving Task entities from each model's pipeline tag
   - Collect news articles from RSS feeds
   - Collect videos from YouTube (if a key is set)
   - Add the curated companies list
   - Add hand-curated Robots, Devices, Personal, and Creative entities
   - Tag recently-updated entities as "New" and build Collection entities
   - Remove duplicates
   - Build relationships between entities
   - Validate every record
   - Save results to the `data/` folder

## Architecture Notes

- **`extract_*.py` files** each pull raw data from one source (GitHub, Hugging Face, News, YouTube) and convert it into the common record format defined in `schema.py`. `extract_github.py` classifies MCP-server search results as `entity_type: "mcp"` rather than generic repositories, and tags a subset of repos as Tools based on description keywords. `extract_huggingface.py` derives a Task entity for each unique Hugging Face `pipeline_tag` it encounters, alongside the Model entities.
- **`companies.py` and `curated_entities.py`** are hand-curated lists (10 real AI companies; a small set of real Robots, Devices, Personal assistants, and Creative tools). These exist because there is no free public API that reliably lists these categories, so the data was researched and entered manually, following the same record format as everything else.
- **`postprocess.py`** tags entities updated within the last 30 days as "New" (based on each source's own date field — `pushed_at`, `last_modified`, or `published_at`), and builds Collection entities that group existing records (e.g. "Most Downloaded Models," "Trending AI Repositories," "MCP Server Directory") without requiring a new data source.
- **`dedupe.py`** merges duplicate entries so the final dataset only has one record per unique entity (matched by name, URL, or fuzzy name similarity), and canonicalizes known name variants (e.g. "OpenAI" vs "Open AI").
- **`relationships.py`** detects real connections between entities — for example, which company develops which model or repository — using whole-word text matching against company names.
- **`validate.py`** checks every record for required fields (`id`, `entity_type`, `name`, `url`) and logs any issues before the final files are saved.

## Known Limitations

- **Entity count varies between runs** since data is pulled live from public APIs. The search terms used for GitHub and Hugging Face were tuned to reliably land the dataset in the 250–300+ record range required by the spec.
- **Relationship detection is intentionally simple.** It uses whole-word text matching (checking if a company name appears in a model or repository description) rather than deep semantic understanding, so it favors precision over recall — it may miss some real relationships that are phrased differently, but it avoids the false positives that a looser substring match produces.
- **The companies, robots, devices, personal, and creative lists are static.** These are hand-picked and hardcoded rather than pulled from a live source, since no free public API reliably covers them — new entries won't appear automatically without manually editing the relevant file.
- **Video extraction depends on a YouTube API key.** The extractor (`extract_youtube.py`) is fully implemented, but if no `YOUTUBE_API_KEY` environment variable is set at runtime, it logs a notice and returns no records rather than failing the pipeline.

## Output Files

- `data/entities.json` — the full combined, deduplicated dataset across all 14 categories (Tools, Tasks, Companies, News, Videos, Robots, Devices, Models, Repositories, MCP, Collections, Personal, Creative, New)
- `data/relationships.json` — detected relationships between entities
- `data/validation_issues.json` — any validation problems found (empty if none)

spreadsheet file :- https://1drv.ms/x/c/f9546aec3796ebcf/IQCcFECBk93-TJgN5qDpMc5VAaHpql8wMxNw3WrHq2cASSI?e=WhhzD8
-
