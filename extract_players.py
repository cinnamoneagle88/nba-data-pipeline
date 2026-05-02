import pandas as pd
from sqlalchemy import create_engine

DB_URI = "postgresql+psycopg2://postgres:mammoth@localhost:5432/nba_pipeline"

QUERY = """
SELECT
  p.id,
  p.name,
  p.team,
  p.points,
  t.city
FROM players p
JOIN teams t
  ON p.team = t.team_name
ORDER BY p.team, p.points DESC;
"""

def main():
    engine = create_engine(DB_URI)
    with engine.connect() as conn:
        df = pd.read_sql_query(QUERY, conn)

    print(df)
    df.to_csv("players_with_city.csv", index=False)
    print("\nWrote: players_with_city.csv")

if __name__ == "__main__":
    main()