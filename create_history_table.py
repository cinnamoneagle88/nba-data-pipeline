from sqlalchemy import create_engine, text

DB_URI = "postgresql+psycopg2://postgres:mammoth@localhost:5432/nba_pipeline"

DDL = """
CREATE TABLE IF NOT EXISTS public.repo_stats_history (
  id BIGSERIAL PRIMARY KEY,
  source TEXT NOT NULL,
  fetched_at TIMESTAMPTZ NOT NULL,
  full_name TEXT NOT NULL,
  language TEXT,
  stargazers_count INT,
  forks_count INT,
  open_issues_count INT,
  watchers_count INT
);

CREATE INDEX IF NOT EXISTS idx_repo_stats_history_source_time
ON public.repo_stats_history (source, fetched_at DESC);
"""

def main():
    engine = create_engine(DB_URI)
    with engine.begin() as conn:
        conn.execute(text(DDL))
        check = conn.execute(text("SELECT to_regclass('public.repo_stats_history');")).scalar()
    print("Created table:", check)

if __name__ == "__main__":
    main()