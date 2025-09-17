# airplane_data_fetcher.py
# ------------------------------------------------------------
"""
This module fetches live airplane data and represents them as objects.
"""
import requests

class Airplane:
    """A simple class to hold airplane data."""
    def __init__(self, id, latitude, longitude):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude

def get_airplanes():
    """
    Fetches live flight data from OpenSky Network and returns a list of Airplane objects.
    """
    print("[Airplane Fetcher] Fetching live flight data...")
    url = 'https://opensky-network.org/api/states/all'
    airplanes = []
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        states = response.json().get('states', [])
        if not states:
            print("[Airplane Fetcher] No flight data received from OpenSky Network.")
            return []
        
        # state[6] is latitude, state[5] is longitude
        for i, state in enumerate(states):
            if state[5] is not None and state[6] is not None:
                # Create an Airplane object for each valid entry
                airplane = Airplane(
                    id=f"airplane_{i}",
                    latitude=state[6],
                    longitude=state[5]
                )
                airplanes.append(airplane)

        print(f"[Airplane Fetcher] Successfully processed {len(airplanes)} airplanes.")
        return airplanes
    except requests.exceptions.RequestException as e:
        print(f"[Airplane Fetcher] Could not fetch flight data: {e}")
        return []