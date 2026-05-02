from sqlalchemy import create_engine, text

DB_URI = "postgresql+psycopg2://postgres:mammoth@localhost:5432/nba_pipeline"
SOURCE = "github:pandas-dev/pandas"

def main():
    engine = create_engine(DB_URI)

    latest_raw_sql = text("""
        SELECT source, fetched_at, payload
        FROM api_raw
        WHERE source = :source
        ORDER BY fetched_at DESC
        LIMIT 1;
    """)

    # Incremental: only insert if this fetched_at isn't already recorded
    exists_sql = text("""
        SELECT 1
        FROM repo_stats_history
        WHERE source = :source AND fetched_at = :fetched_at
        LIMIT 1;
    """)

    insert_sql = text("""
        INSERT INTO repo_stats_history (
          source, fetched_at, full_name, language,
          stargazers_count, forks_count, open_issues_count, watchers_count
        )
        VALUES (
          :source, :fetched_at, :full_name, :language,
          :stargazers_count, :forks_count, :open_issues_count, :watchers_count
        );
    """)

    with engine.begin() as conn:
        row = conn.execute(latest_raw_sql, {"source": SOURCE}).mappings().first()
        if not row:
            raise RuntimeError("No raw payload found")

        payload = row["payload"]
        fetched_at = row["fetched_at"]

        already = conn.execute(exists_sql, {"source": SOURCE, "fetched_at": fetched_at}).first()
        if already:
            print("Already captured this fetched_at; skipping history insert.")
            return

        data = {
            "source": row["source"],
            "fetched_at": fetched_at,
            "full_name": payload.get("full_name"),
            "language": payload.get("language"),
            "stargazers_count": payload.get("stargazers_count"),
            "forks_count": payload.get("forks_count"),
            "open_issues_count": payload.get("open_issues_count"),
            "watchers_count": payload.get("watchers_count"),
        }

        if not data["full_name"]:
            raise RuntimeError("Missing full_name in payload")

        conn.execute(insert_sql, data)

    print("Inserted 1 row into repo_stats_history.")

if __name__ == "__main__":
    main()