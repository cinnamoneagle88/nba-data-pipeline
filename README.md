# NBA Data Pipeline

A production-style data engineering project that extracts NBA player statistics from the NBA API, loads curated player stats into PostgreSQL, stores historical snapshots, and exposes an analytics-ready leaderboard view.

## Stack
- Python
- PostgreSQL
- SQLAlchemy
- python-dotenv
- nba_api
- DBeaver

## Pipeline
1. Extract player stats from NBA API
2. Upsert latest player stats into `nba_player_stats`
3. Insert full snapshot into `nba_player_stats_history`
4. Query analytics-ready leaderboard via `nba_player_leaderboard`

## Run
```bash
source .venv/bin/activate
python run_nba_pipeline.py