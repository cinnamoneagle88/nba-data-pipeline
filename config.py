from dotenv import load_dotenv
import os

load_dotenv()

DB_URI = os.environ["DB_URI"]

SEASON = "2025-26"
SEASON_TYPE = "Regular Season"
MIN_GAMES_THRESHOLD = 20