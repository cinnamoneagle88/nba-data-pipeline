import subprocess

scripts = [
    "load_nba_player_stats.py",
    "load_nba_player_stats_history.py",
]

for script in scripts:
    print(f"Running {script}...")
    result = subprocess.run(["python", script])

    if result.returncode != 0:
        raise Exception(f"{script} failed")

print("Pipeline completed successfully.")