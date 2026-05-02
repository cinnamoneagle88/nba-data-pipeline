from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from pipeline_logger import logger
from config import DB_URI
import os

load_dotenv()
DB_URI = os.environ["DB_URI"]

def main():
    engine = create_engine(DB_URI)

    checks = {
        "no_null_player_ids": """
            SELECT COUNT(*) FROM public.nba_player_stats
            WHERE player_id IS NULL;
        """,
        "no_null_player_names": """
            SELECT COUNT(*) FROM public.nba_player_stats
            WHERE player_name IS NULL;
        """,
        "player_count_reasonable": """
            SELECT COUNT(*) FROM public.nba_player_stats;
        """,
        "no_negative_points": """
            SELECT COUNT(*) FROM public.nba_player_stats
            WHERE pts < 0;
        """
    }

    with engine.connect() as conn:
        for check_name, sql in checks.items():
            result = conn.execute(text(sql)).scalar()

            if check_name == "player_count_reasonable":
                if result < 400:
                    raise ValueError(f"{check_name} failed: only {result} players")
            elif result != 0:
                raise ValueError(f"{check_name} failed: {result} bad rows")

            print(f"{check_name}: passed")

    print("All validation checks passed.")
if __name__ == "__main__":
    main()