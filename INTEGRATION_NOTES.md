Integration Notes
Files to replace
src/extract_huggingface.py → replace with the new version (now also
returns Task entities derived from pipeline_tag)
src/extract_github.py → replace with the new version (MCP-server search
results are now tagged entity_type="mcp"; some repos get a "Tools"
category added)
Files to add
src/extract_youtube.py (new — needs a free YOUTUBE_API_KEY env var)
src/postprocess.py (new — tags "New" entities, builds Collections)
src/curated_entities.py (new — Robots, Devices, Personal, Creative)
Changes to run.py
Wherever run.py currently does something like:
Python
Add the new sources and the postprocessing step before dedupe/validate:
Python
Category coverage after these changes
Tools, Tasks, Companies, News, Videos, Robots, Devices, Models, Repositories,
MCP, Collections, Personal, Creative, New — all 14.
README updates worth making
Move MCP, Videos, Tasks, Robots/Devices/Personal/Creative out of "not
covered" and into the source list
Note that Robots/Devices/Personal/Creative are hand-curated for the same
reason companies.py is (no free API covers them) — this is already your
precedent, so it's consistent rather than a new weak spot
Mention the YouTube API key requirement in setup instructions
Before you submit
Set YOUTUBE_API_KEY and re-run run.py
Check data/entities.json has all 14 categories represented
Check data/relationships.json — the new MCP↔Tool and Device↔Model
mappings should have new entries now (or add: MCP integrates with Tool,
Device runs Model, from your relationships.py)
Send me the final entities.json + relationships.json and I'll build
your spreadsheet from the real numbers