import sqlite3
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Optional
import os

DB_PATH = "links.db"
# Go one directory up, then into frontend/
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")

app = FastAPI(
    title="Job Posting Link Hub",
    description="A minimal personal API to store job posting links in one place.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def serve_ui():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS links (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                url        TEXT    NOT NULL UNIQUE,
                job_title  TEXT,
                company    TEXT,
                created_at TEXT    NOT NULL
            )
            """
        )
        conn.commit()


# Run on startup
init_db()


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class LinkIn(BaseModel):
    url: HttpUrl
    job_title: Optional[str] = None
    company: Optional[str] = None


class LinkOut(BaseModel):
    id: int
    url: str
    job_title: Optional[str]
    company: Optional[str]
    created_at: str


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.post("/links", response_model=LinkOut, status_code=201)
def save_link(payload: LinkIn):
    """Save a new job posting link. Returns 409 if the URL already exists."""
    now = datetime.now(timezone.utc).isoformat()
    url_str = str(payload.url)

    try:
        with get_conn() as conn:
            cursor = conn.execute(
                "INSERT INTO links (url, job_title, company, created_at) VALUES (?, ?, ?, ?)",
                (url_str, payload.job_title, payload.company, now),
            )
            conn.commit()
            row_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="URL already exists.")

    return LinkOut(
        id=row_id,
        url=url_str,
        job_title=payload.job_title,
        company=payload.company,
        created_at=now,
    )


@app.get("/links", response_model=list[LinkOut])
def list_links():
    """Return all saved links, newest first."""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, url, job_title, company, created_at FROM links ORDER BY id DESC"
        ).fetchall()
    return [LinkOut(**dict(r)) for r in rows]


@app.get("/links/{link_id}", response_model=LinkOut)
def get_link(link_id: int):
    """Return a single link by ID. Returns 404 if not found."""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT id, url, job_title, company, created_at FROM links WHERE id = ?",
            (link_id,),
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Link not found.")
    return LinkOut(**dict(row))


@app.delete("/links/{link_id}", status_code=204)
def delete_link(link_id: int):
    """Delete a link by ID. Returns 204 on success, 404 if not found."""
    with get_conn() as conn:
        cursor = conn.execute("DELETE FROM links WHERE id = ?", (link_id,))
        conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Link not found.")
    return JSONResponse(status_code=204, content=None)
