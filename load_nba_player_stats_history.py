from datetime import datetime, timezone
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()
DB_URI = os.environ["DB_URI"]

def main():
    engine = create_engine(DB_URI)
    snapshot_at = datetime.now(timezone.utc)

    sql = text("""
    INSERT INTO public.nba_player_stats_history (
      player_id, player_name, team_id, team_abbreviation, age,
      gp, min, pts, reb, ast, stl, blk, tov,
      fg_pct, fg3_pct, ft_pct, fetched_at, snapshot_at
    )
    SELECT
      player_id, player_name, team_id, team_abbreviation, age,
      gp, min, pts, reb, ast, stl, blk, tov,
      fg_pct, fg3_pct, ft_pct, fetched_at, :snapshot_at
    FROM public.nba_player_stats;
""")
    with engine.begin() as conn:
        result = conn.execute(sql, {"snapshot_at": snapshot_at})

    print(f"Inserted {result.rowcount} rows into nba_player_stats_history at {snapshot_at}.")

if __name__ == "__main__":
    main()