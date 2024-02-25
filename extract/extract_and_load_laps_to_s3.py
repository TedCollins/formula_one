import fastf1
from fastf1 import plotting
#from pathlib import Path
import pandas as pd
import boto3
from io import StringIO

# Enable the cache
fastf1.Cache.enable_cache('extract/cache')

def df_to_s3_csv(df, bucket_name, object_name):
    """
    Write a DataFrame to a CSV on S3

    Parameters:
    - df: DataFrame to write.
    - bucket_name: Name of the S3 bucket.
    - object_name: S3 object name (path within the bucket).
    """
    # Create an S3 client
    s3_client = boto3.client('s3')
    csv_buffer = StringIO()
    df.to_csv(csv_buffer)

    # Write the DataFrame to a CSV in S3
    s3_client.put_object(Bucket=bucket_name, Body=csv_buffer.getvalue(), Key=object_name)

def fetch_and_save_lap_times_to_s3(season, bucket_name):
    """
    Fetches lap time data for each race in a given F1 season and saves it to CSV files on S3.

    Parameters:
    - season: The F1 season year as an integer.
    - bucket_name: The name of the S3 bucket where files will be saved.
    """
    schedule = fastf1.get_event_schedule(season)
    for _, race in schedule.iterrows():
        race_name = race['EventName']
        race_date = race['EventDate'].date()
        print(f"Fetching data for: {race_name} ({race_date})")

        try:
            # Qualifying session is used as an example; you can change this to 'Race' or another session
            the_session = fastf1.get_session(season, race_name, session_type)
            the_session.load()

            # Get lap times for all drivers
            lap_times = the_session.laps.pick_quicklaps()

            # Define S3 object name
            object_name = f"{season}/{race_name.replace(' ', '_')}/{session_type}_LapTimes.csv"
            
            # Save DataFrame to S3
            df_to_s3_csv(lap_times, bucket_name, object_name)
            print(f"Saved lap times to {bucket_name}/{object_name}")
        except Exception as e:
            print(f"Could not fetch data for {race_name} due to error: {e}")

# Execution
season = 2023  # Example season year
session_type = 'R'
bucket_name = 'f1datalaketc'
fetch_and_save_lap_times_to_s3(season, bucket_name)
