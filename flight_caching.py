# flight_data_cacher.py
# ------------------------------------------------------------
"""
This script periodically fetches airplane data using the airplane_data_fetcher
module and caches the data into timestamped JSON files.
"""

import time
import json
from datetime import datetime
import os
import airplane_data_fetcher

# --- Configuration ---
# The interval in seconds between each data fetch.
FETCH_INTERVAL = 60
# The directory where the cached data files will be stored.
CACHE_DIRECTORY = "flight_data_cache"


def run_periodic_fetch():
    """
    Main function to run the data fetching and caching loop.
    """
    print("--- Flight Data Cacher Initialized ---")
    print(f"Data will be fetched every {FETCH_INTERVAL} seconds.")
    print(f"Cached files will be saved in the '{CACHE_DIRECTORY}/' directory.")
    print("Press Ctrl+C to stop the script.")
    print("----------------------------------------")

    # Create the cache directory if it doesn't already exist.
    try:
        os.makedirs(CACHE_DIRECTORY, exist_ok=True)
    except OSError as e:
        print(f"Error creating directory {CACHE_DIRECTORY}: {e}")
        return # Exit if we can't create the directory

    while True:
        try:
            # 1. Get the current time for the filename
            timestamp = datetime.now()
            print(f"\n[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] Starting fetch cycle...")

            # 2. Fetch the airplane data
            airplanes = airplane_data_fetcher.get_airplanes()

            if airplanes:
                # 3. Convert the list of Airplane objects to a list of dictionaries
                #    This makes the data serializable to JSON.
                airplanes_data = [vars(plane) for plane in airplanes]

                # 4. Construct the filename with the timestamp
                filename = f"flight_data_{timestamp.strftime('%Y-%m-%d_%H-%M-%S')}.json"
                filepath = os.path.join(CACHE_DIRECTORY, filename)

                # 5. Save the data to a JSON file
                try:
                    with open(filepath, 'w') as f:
                        json.dump(airplanes_data, f, indent=4)
                    print(f"Successfully saved data for {len(airplanes_data)} airplanes to '{filepath}'")
                except IOError as e:
                    print(f"Error writing to file {filepath}: {e}")

            else:
                print("No airplane data to save.")

            # 6. Wait for the specified interval before the next run
            print(f"Sleeping for {FETCH_INTERVAL} seconds...")
            time.sleep(FETCH_INTERVAL)

        except KeyboardInterrupt:
            print("\n--- Script stopped by user. ---")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print(f"Retrying in {FETCH_INTERVAL} seconds...")
            time.sleep(FETCH_INTERVAL)

if __name__ == "__main__":
    # Ensure you have the airplane_data_fetcher.py file in the same directory
    # as this script.
    run_periodic_fetch()
