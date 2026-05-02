# NBA Data Pipeline & Analytics Dashboard

Production-style data pipeline that ingests NBA player statistics from the NBA API, stores curated and historical data in PostgreSQL, and powers an interactive Tableau dashboard for performance analysis.

## Live Dashboard
https://public.tableau.com/app/profile/alex.quintero4755/viz/NBAPlayerPerformanceDashboard_17777630690560/NBAPlayerPerformanceDashboard

## Key Features
- Ingests 500+ player records from NBA API
- Idempotent upsert pipeline using PostgreSQL
- Data validation checks (nulls, anomalies, record counts)
- Retry logic for API reliability
- Historical snapshot tracking for time-series analysis
- Analytics-ready SQL view powering Tableau dashboard

## Tech Stack
Python, PostgreSQL, SQLAlchemy, pandas, Tableau

## Architecture
API → Python ETL → PostgreSQL (curated + history) → SQL View → Tableau Dashboard

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
