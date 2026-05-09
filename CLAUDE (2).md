# CLAUDE.md — Job Posting Link Hub

## What this is

A minimal personal API to store job posting links in one place.
You provide the URL, job title, and company name. That's it.

---

## Stack

| Layer | Choice |
|---|---|
| API | Python + FastAPI |
| Database | SQLite (single file: `links.db`) |
| Server | Uvicorn |

---

## Data Model

**Table: `links`**

| Column | Type | Notes |
|---|---|---|
| `id` | INTEGER | Auto-increment primary key |
| `url` | TEXT | Unique — no duplicate links |
| `job_title` | TEXT | Optional |
| `company` | TEXT | Optional |
| `created_at` | TEXT | UTC ISO-8601 timestamp |

---

## API Endpoints

Base URL: `http://localhost:8000`

### Save a link
```
POST /links
```
```json
{
  "url": "https://linkedin.com/jobs/view/123456",
  "job_title": "Backend Engineer",
  "company": "Acme Corp"
}
```
Returns `201` with the saved link. Returns `409` if the URL already exists.

---

### List all links
```
GET /links
```
Returns all saved links, newest first.

---

### Get one link
```
GET /links/{id}
```
Returns a single link by ID. Returns `404` if not found.

---

### Delete a link
```
DELETE /links/{id}
```
Returns `204` on success. Returns `404` if not found.

---

## Running locally

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload

# API is live at http://localhost:8000
# Interactive docs at http://localhost:8000/docs
```

---

## File structure

```
job-hub/
├── main.py           # All routes, DB init, schemas
├── requirements.txt  # fastapi, uvicorn, pydantic
├── links.db          # Auto-created on first run (gitignore this)
└── CLAUDE.md         # This file
```

---

## Notes for Claude

- SQLite is used intentionally — no setup, single file, perfect for personal use.
- `links.db` is created automatically on startup via `init_db()`.
- The `url` column has a UNIQUE constraint — posting the same URL twice returns a `409`.
- `job_title` and `company` are optional — URL-only saves are valid.
- All timestamps are stored as UTC ISO-8601 strings.
- To switch to PostgreSQL later, replace `sqlite3` calls with `psycopg2` or SQLAlchemy and update `DB_PATH` to a connection string.
