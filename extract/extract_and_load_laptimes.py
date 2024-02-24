import fastf1
from fastf1 import plotting
from pathlib import Path
import pandas as pd

# Enable the cache
fastf1.Cache.enable_cache('extract/cache')

def fetch_and_save_lap_times(season, save_dir):
    """
    Fetches lap time data for each race in a given F1 season and saves it to CSV files.

    Parameters:
    - season: The F1 season year as an integer.
    - save_dir: Directory path as a string where the CSV files will be saved.
    """
    # Create a directory if it doesn't exist
    Path(save_dir).mkdir(parents=True, exist_ok=True)
    
    # Get the list of races for the season
    schedule = fastf1.get_event_schedule(season)
    for _, race in schedule.iterrows():
        race_name = race['EventName']
        race_date = race['EventDate'].date()
        print(f"Fetching data for: {race_name} ({race_date}) {session_type}")
        
        # Load the session
        try:
            # Qualifying session is used as an example; you can change this to 'Race' or another session
            the_session = fastf1.get_session(season, race_name, session_type)
            the_session.load()
            
            # Get lap times for all drivers
            lap_times = the_session.laps.pick_quicklaps()
            
            # Save to CSV
            file_path = Path(save_dir) / f"{season}_{race_name.replace(' ', '_')}_{session_type}_LapTimes.csv"
            lap_times.to_csv(file_path)
            print(f"Saved lap times to {file_path}")
        except Exception as e:
            print(f"Could not fetch data for {race_name} due to error: {e}")

# Example usage
season = 2023  # Example season year
save_dir = 'extract/ingest' 
session_type = 'R'
fetch_and_save_lap_times(season, save_dir)
