import json
from datetime import datetime, timezone

import requests
from sqlalchemy import create_engine, text

DB_URI = "postgresql+psycopg2://postgres:mammoth@localhost:5432/nba_pipeline"

# Simple, reliable public API for learning
API_URL = "https://api.github.com/repos/pandas-dev/pandas"

def main():
    engine = create_engine(DB_URI)

    # 1) Extract
    r = requests.get(API_URL, timeout=20)
    r.raise_for_status()
    payload = r.json()

    # 2) Load raw (JSONB)
    fetched_at = datetime.now(timezone.utc).isoformat()

    insert_sql = text("""
        INSERT INTO api_raw (source, fetched_at, payload)
        VALUES (:source, :fetched_at, CAST(:payload AS jsonb));
    """)

    with engine.begin() as conn:
        conn.execute(
            insert_sql,
            {
                "source": "github:pandas-dev/pandas",
                "fetched_at": fetched_at,
                "payload": json.dumps(payload),
            },
        )

    print("Inserted 1 raw payload at", fetched_at)

if __name__ == "__main__":
    main()