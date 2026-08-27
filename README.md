AI Orbit Ecosystem Data Ingestion Pipeline
What This Project Does
This pipeline collects AI-ecosystem data — models, repositories, news articles, and
companies — from free public APIs (GitHub, Hugging Face, and RSS news feeds),
combines everything into a single structured dataset, removes duplicates, detects
relationships between entities (like which company built which model or tool), and
validates every record before saving the final output.
Project Structure
Code
Setup Instructions
Create the project folder with src, data, and logs subfolders.
Create and activate a virtual environment:
Code
(If PowerShell blocks this, run once:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser)
Install the required libraries:
Code
Run the pipeline from the main project folder (not inside src):
Code
The pipeline will automatically:
Collect repositories from GitHub
Collect models from Hugging Face
Collect news articles from RSS feeds
Add the curated companies list
Remove duplicates
Build relationships between entities
Validate every record
Save results to the data/ folder
Architecture Notes
The code is split into separate files by responsibility:
extract_*.py files each pull raw data from one source (GitHub, Hugging Face,
News) and convert it into the common record format defined in schema.py.
companies.py is a hand-curated list of 10 real AI companies (OpenAI,
Anthropic, Google DeepMind, Meta AI, Hugging Face, Stability AI, Mistral AI,
Cohere, xAI, Perplexity AI). This file exists because there is no free public API
that lists AI companies, so this data was researched and entered manually,
following the same record format as everything else.
dedupe.py merges duplicate entries so the final dataset only has one record
per unique entity (matched by name, URL, or fuzzy name similarity).
relationships.py detects real connections between entities — for example,
which company develops which model or repository — using whole-word text
matching against company names.
validate.py checks every record for required fields (id, entity_type, name,
url) and logs any issues before the final files are saved.
Known Limitations
Entity count varies between runs since data is pulled live from public APIs.
The search terms used for GitHub and Hugging Face had to be tuned and expanded
(from 3 to 8-10 terms per source) to reliably land the dataset in the 250-300
record range required by the spec.
Relationship detection is intentionally simple. It uses whole-word text
matching (checking if a company name appears in a model or repository
description) rather than deep semantic understanding, so it favors precision
over recall — it may miss some real relationships that are phrased differently,
but it avoids the false positives that a looser substring match produces.
The companies list is static. The 10 companies in companies.py are
hand-picked and hardcoded rather than pulled from a live source, so new
companies won't appear automatically without manually editing that file.
Output Files
data/entities.json — the full combined, deduplicated dataset
data/relationships.json — detected relationships between entities
data/validation_issues.json — any validation problems found (empty if none)
