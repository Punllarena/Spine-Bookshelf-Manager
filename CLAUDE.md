# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

All commands run from `src/`:

```bash
# Set up
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run locally
python main.py

# Docker
docker-compose up --build -d   # build and start
docker-compose down             # stop
```

The Docker volume `spine-data` must exist before first run: `docker volume create spine-data`

## Architecture

The app is a single-process Flask app with no blueprints. Routes are defined as plain functions in `routes.py` and registered manually via `app.add_url_rule()` in `main.py`.

**Request flow for adding a book:**
1. User searches → `routes.search()` calls `apirequest.search_volume()` → renders `search.html`
2. User clicks a result → `routes.volume_info()` calls `apirequest.get_volume()` + `apirequest.get_series()` → renders `volumeinfo.html`
3. User clicks Add → `routes.add()` calls `get_volume_info()` (which makes both API calls) → writes a `Book` row to SQLite

**Key architectural decisions:**
- Book metadata is fetched from the RanobeDB API at add-time and stored in full in SQLite — shelves, series views, and timeline all read only from the DB, never the API.
- `g_volume_id` (named for legacy reasons) stores the RanobeDB integer book ID as a string. It is the unique key used in all URLs (`/volumeInfo/<volume_id>`, `/edit/<volume_id>`, etc.).
- Series ordering uses `sort_order` from the `/series/{id}` endpoint, which requires a second API call when viewing or adding a book that belongs to a series.
- The `Upcoming` table caches scrape results from yattatachi.com keyed by the post URL. Stale entries (different URL) are deleted on each `/upcoming` visit.

**API layer (`apirequest.py`):**
- `search_volume(query, page)` → `GET /books?q=...&rl=en` (English releases only)
- `get_volume(volume_id)` → `GET /book/{id}`, returns the raw `book` dict
- `get_series(series_id)` → `GET /series/{id}`, used to resolve `sort_order` for a book within its series

**Backup/restore (`utils.py`):**
- CSV format, semicolon-delimited, one book per line, header line starts with `#`
- Column order is hardcoded in both `download_backup()` and `restore_backup()` — they must stay in sync with each other and with the `Book` model field order

**`yattaUpcoming.py`** scrapes yattatachi.com for upcoming light novel releases. The function `run_scraper()` is called with the result of `check_latest_post()` as its default argument — this means the HTTP request fires at import time unless the module is run directly. This is intentional but means importing the module in tests or dev will hit the network.
