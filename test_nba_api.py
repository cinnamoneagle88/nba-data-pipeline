from nba_api.stats.endpoints import leaguedashplayerstats

def main():
    stats = leaguedashplayerstats.LeagueDashPlayerStats(
        season="2025-26",
        season_type_all_star="Regular Season"
    )

    df = stats.get_data_frames()[0]

    print(df.head())
    print(df.columns.tolist())

if __name__ == "__main__":
    main()