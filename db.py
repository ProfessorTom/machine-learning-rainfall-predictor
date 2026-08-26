import sqlite3
import os
from pathlib import Path
from datetime import datetime, timezone
import shutil
from typing import Optional

from entities.geocoded_zip import GeocodedZip

# --- Configuration (runs when the module is imported) ---
CACHE_DB_NAME = os.getenv("CACHE_DB_NAME", "weather_cache.db")
CACHE_DB_DIR  = os.getenv("CACHE_DB_DIR", "")

if CACHE_DB_DIR:
    CACHE_DB_PATH = str(Path(CACHE_DB_DIR) / CACHE_DB_NAME)
else:
    CACHE_DB_PATH = CACHE_DB_NAME


def get_connection():
    """Return a connection to the SQLite database.
    Creates the database file if it does not exist yet.
    """
    conn = sqlite3.connect(CACHE_DB_PATH)
    conn.row_factory = sqlite3.Row  # Access columns by name (row["zip"])
    return conn


def backup_db():
    """Create a timestamped backup of the database."""
    if not os.path.exists(CACHE_DB_PATH):
        print("No database file found to back up.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"weather_cache_backup_{timestamp}.db"
    shutil.copy2(CACHE_DB_PATH, backup_name)
    print(f"Backup created: {backup_name}")


def init_db():
    """Create the tables if they do not already exist.
    Safe to call multiple times — it will never destroy existing data.
    """
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS locations (
                zip TEXT PRIMARY KEY,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                city TEXT,
                state TEXT,
                last_updated TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS historical (
                zip TEXT NOT NULL,
                date TEXT NOT NULL,
                temp_max REAL,
                temp_min REAL,
                precipitation REAL,
                PRIMARY KEY (zip, date),
                FOREIGN KEY (zip) REFERENCES locations(zip)
            );

            CREATE TABLE IF NOT EXISTS forecasts (
                zip TEXT NOT NULL,
                date TEXT NOT NULL,
                temp_max REAL,
                temp_min REAL,
                predicted_precipitation REAL,
                fetched_at TEXT NOT NULL,
                PRIMARY KEY (zip, date),
                FOREIGN KEY (zip) REFERENCES locations(zip)
            );
        """)
    print("Database ready.")


def get_db_status() -> str:
    """Return a human-readable status of the database."""
    try:
        with get_connection() as conn:
            tables = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()

            if not tables:
                return "Database connected, but no tables found."

            table_names = [row["name"] for row in tables]
            return f"Database connection successful. Tables: {', '.join(table_names)}"
    except Exception as e:
        return f"Database error: {e}"

def get_cached_location(zip_code: str) -> Optional[GeocodedZip]:
    """
    Look up a ZIP code in the locations table.
    Returns a GeocodedZip if found, otherwise None.
    """
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT zip, latitude, longitude, city, state
            FROM locations
            WHERE zip = ?
            """,
            (zip_code,)
        ).fetchone()

    if row is None:
        return None

    return GeocodedZip(
        zip=row["zip"],
        latitude=row["latitude"],
        longitude=row["longitude"],
        city=row["city"],
        state_abbr=row["state"],
    )


def save_location(location: GeocodedZip) -> None:
    """
    Insert or update a GeocodedZip in the locations table.
    """
    now = datetime.now(timezone.utc).isoformat()

    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO locations (zip, latitude, longitude, city, state, last_updated)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(zip) DO UPDATE SET
                latitude = excluded.latitude,
                longitude = excluded.longitude,
                city = excluded.city,
                state = excluded.state,
                last_updated = excluded.last_updated
            """,
            (
                location.zip,
                location.latitude,
                location.longitude,
                location.city,
                location.state_abbr,
                now,
            )
        )
        conn.commit()


if __name__ == "__main__":
    init_db()
    print(get_db_status())
    # backup_db()   # uncomment if you want to test backup
