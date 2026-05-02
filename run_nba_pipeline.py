import subprocess
from pipeline_logger import logger

scripts = [
    "load_nba_player_stats.py",
    "validate_nba_data.py",
    "load_nba_player_stats_history.py",
]

for script in scripts:
    print(f"Running {script}...")
    result = subprocess.run(["python", script])

    if result.returncode != 0:
        raise Exception(f"{script} failed")

logger.info("Pipeline completed successfully.")