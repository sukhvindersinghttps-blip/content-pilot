# YouTube Content Opportunity Agent

A modular Python V1 for discovering recent YouTube content opportunities, detecting channel-size-adjusted outliers, extracting patterns, and generating original topic/SEO/thumbnail recommendations.

## What V1 does

- Searches YouTube videos for a chosen niche and recent time window.
- Collects public video/channel metadata through the YouTube Data API.
- Calculates an **outlier score** using views relative to channel subscribers and views/day.
- Extracts title/topic/format patterns from top outliers.
- Generates original content opportunities with an LLM when `OPENAI_API_KEY` is configured.
- Produces a Markdown report and JSON dataset.

> The system is designed to learn from successful patterns, not copy scripts, titles verbatim, or other creators' protected content.

## Quick start

### 1. Requirements

Python 3.10+

### 2. Install

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

### 3. Configure API keys

Copy `.env.example` to `.env` and add:

- `YOUTUBE_API_KEY`: Google/YouTube Data API v3 key.
- `OPENAI_API_KEY`: optional for AI-generated topic/SEO recommendations.
- `OPENAI_MODEL`: optional, defaults to `gpt-5.6`.

### 4. Run

```bash
python -m app.main --niche "history" --days 7 --max-results 50
```

The report is saved under `reports/`.

### Example

```bash
python -m app.main \
  --niche "Indian history" \
  --days 7 \
  --max-results 50 \
  --language en
```

## Architecture

```text
Niche
  ↓
YouTube Search
  ↓
Video + Channel Metadata
  ↓
Outlier Detection
  ↓
Pattern Extraction
  ↓
Original Topic Generation
  ↓
SEO + Thumbnail Strategy
  ↓
Markdown/JSON Report
```

## Outlier score

V1 intentionally uses transparent heuristics rather than pretending to predict virality. The score combines:

- views / subscribers
- views per day
- recency
- engagement when available

A high score means a video is performing unusually well relative to its channel size and age. It does **not** guarantee future virality.

## Roadmap

- Competitor/channel watchlists
- Better semantic topic clustering
- Thumbnail image generation
- Script-generation agent
- Multi-language research
- Historical trend database
- Scheduled daily research
- Web dashboard
- YouTube Analytics integration for the user's own channels
- Experiment tracking for title/thumbnail performance

## License

MIT
