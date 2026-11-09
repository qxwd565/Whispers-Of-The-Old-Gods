# Whispers of the Old Gods card API

Canonical Korean-date card history is in `data/<original ID>.json`.
Initial full specifications and later sparse deltas preserve all 163 existing IDs.

- Legacy-compatible outputs: `cards.json`, `render.json`, `history.json`.
- Precise history outputs: `cards-date.json`, `render-date.json`, `history-date.json`.
- Source provenance and confidence: `metadata/`, `tools/wog-korean-source-audit.json`, and `tools/wog-archive-evidence.json`.
- Format, replay, evidence limits and checks: [docs/date-schema.md](docs/date-schema.md).

Run `python3 tools/build-api.py` after evidence-backed canonical edits. Artwork and golden assets are unchanged. No plugin or live site changes are required for the legacy endpoints.
