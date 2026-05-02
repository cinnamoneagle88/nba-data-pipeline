# NBA Data Pipeline

A production-style data engineering pipeline that ingests NBA player statistics from the NBA API, loads curated data into PostgreSQL, validates data quality, stores historical snapshots, and exposes analytics-ready views.

## Tech Stack

* Python (nba_api, SQLAlchemy)
* PostgreSQL
* pandas
* python-dotenv

## Pipeline Architecture

1. Extract player stats from NBA API
2. Upsert latest data into `nba_player_stats`
3. Validate data quality (nulls, counts, anomalies)
4. Store full snapshot in `nba_player_stats_history`
5. Query analytics-ready leaderboard via `nba_player_leaderboard`

## Run Locally

```bash
source .venv/bin/activate
python run_nba_pipeline.py
```

## Data Model

* `nba_player_stats` → latest player stats (upserted)
* `nba_player_stats_history` → time-series snapshots
* `nba_player_leaderboard` → analytics view (PPG, RPG, APG)

## Example Query

```sql
SELECT player_name, team_abbreviation, gp, ppg
FROM public.nba_player_leaderboard
ORDER BY ppg DESC
LIMIT 10;
```

## Key Features

* Idempotent upsert pipeline
* Retry logic for API reliability
* Data validation checks before persistence
* Historical snapshot tracking for trend analysis
* Centralized configuration via `config.py`
