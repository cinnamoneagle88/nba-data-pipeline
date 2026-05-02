from sqlalchemy import create_engine, text

DB_URI = "postgresql+psycopg2://postgres:mammoth@localhost:5432/nba_pipeline"

def main():
    engine = create_engine(DB_URI)

    # Grab the latest raw payload for that source
    extract_sql = text("""
        SELECT source, fetched_at, payload
        FROM api_raw
        WHERE source = :source
        ORDER BY fetched_at DESC
        LIMIT 1;
    """)

    upsert_sql = text("""
        INSERT INTO repo_stats (
          source, fetched_at, full_name, description, language,
          stargazers_count, forks_count, open_issues_count, watchers_count
        )
        VALUES (
          :source, :fetched_at, :full_name, :description, :language,
          :stargazers_count, :forks_count, :open_issues_count, :watchers_count
        )
        ON CONFLICT (source) DO UPDATE SET
          fetched_at = EXCLUDED.fetched_at,
          full_name = EXCLUDED.full_name,
          description = EXCLUDED.description,
          language = EXCLUDED.language,
          stargazers_count = EXCLUDED.stargazers_count,
          forks_count = EXCLUDED.forks_count,
          open_issues_count = EXCLUDED.open_issues_count,
          watchers_count = EXCLUDED.watchers_count;
    """)

    source = "github:pandas-dev/pandas"

    with engine.begin() as conn:
        row = conn.execute(extract_sql, {"source": source}).mappings().first()
        if not row:
            raise RuntimeError(f"No raw payloads found for source={source}")

        payload = row["payload"]  # JSONB comes back as a dict-like object

        data = {
            "source": row["source"],
            "fetched_at": row["fetched_at"],
            "full_name": payload.get("full_name"),
            "description": payload.get("description"),
            "language": payload.get("language"),
            "stargazers_count": payload.get("stargazers_count"),
            "forks_count": payload.get("forks_count"),
            "open_issues_count": payload.get("open_issues_count"),
            "watchers_count": payload.get("watchers_count"),
        }

        # Basic sanity checks (DE habit)
        if not data["full_name"]:
            raise RuntimeError("Missing full_name in payload; schema changed?")

        conn.execute(upsert_sql, data)

    print("Upserted repo_stats for", source)

if __name__ == "__main__":
    main()