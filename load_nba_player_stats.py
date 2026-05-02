from datetime import datetime, timezone
import time
from nba_api.stats.endpoints import leaguedashplayerstats
from sqlalchemy import create_engine, text

from config import DB_URI, SEASON, SEASON_TYPE


def main():
    engine = create_engine(DB_URI)

    df = None

for attempt in range(1, 4):
    try:
        stats = leaguedashplayerstats.LeagueDashPlayerStats(
            season=SEASON,
            season_type_all_star=SEASON_TYPE,
            timeout=60,
        )
        df = stats.get_data_frames()[0]
        break

    except Exception as e:
        print(f"NBA API attempt {attempt} failed: {e}")

        if attempt == 3:
            raise RuntimeError("NBA API failed after 3 attempts") from e

        time.sleep(5)

    fetched_at = datetime.now(timezone.utc)

    upsert_sql = text("""
        INSERT INTO public.nba_player_stats (
          player_id, player_name, team_id, team_abbreviation, age,
          gp, min, pts, reb, ast, stl, blk, tov,
          fg_pct, fg3_pct, ft_pct, fetched_at
        )
        VALUES (
          :player_id, :player_name, :team_id, :team_abbreviation, :age,
          :gp, :min, :pts, :reb, :ast, :stl, :blk, :tov,
          :fg_pct, :fg3_pct, :ft_pct, :fetched_at
        )
        ON CONFLICT (player_id) DO UPDATE SET
          player_name = EXCLUDED.player_name,
          team_id = EXCLUDED.team_id,
          team_abbreviation = EXCLUDED.team_abbreviation,
          age = EXCLUDED.age,
          gp = EXCLUDED.gp,
          min = EXCLUDED.min,
          pts = EXCLUDED.pts,
          reb = EXCLUDED.reb,
          ast = EXCLUDED.ast,
          stl = EXCLUDED.stl,
          blk = EXCLUDED.blk,
          tov = EXCLUDED.tov,
          fg_pct = EXCLUDED.fg_pct,
          fg3_pct = EXCLUDED.fg3_pct,
          ft_pct = EXCLUDED.ft_pct,
          fetched_at = EXCLUDED.fetched_at;
    """)

    rows = []
    for _, r in df.iterrows():
        rows.append({
            "player_id": int(r["PLAYER_ID"]),
            "player_name": r["PLAYER_NAME"],
            "team_id": int(r["TEAM_ID"]),
            "team_abbreviation": r["TEAM_ABBREVIATION"],
            "age": r["AGE"],
            "gp": int(r["GP"]),
            "min": r["MIN"],
            "pts": r["PTS"],
            "reb": r["REB"],
            "ast": r["AST"],
            "stl": r["STL"],
            "blk": r["BLK"],
            "tov": r["TOV"],
            "fg_pct": r["FG_PCT"],
            "fg3_pct": r["FG3_PCT"],
            "ft_pct": r["FT_PCT"],
            "fetched_at": fetched_at,
        })

    with engine.begin() as conn:
        conn.execute(upsert_sql, rows)

    print(f"Upserted {len(rows)} NBA player stat rows for season {SEASON}")


if __name__ == "__main__":
    main()