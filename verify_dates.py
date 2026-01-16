import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
import calendar
import re

def verify_song_date(artist, name, current_year=None):
    """
    Verifies and potentially corrects the release date of a song using MusicBrainz.
    Returns a dict with updated date fields if a better date is found, or None.
    """
    # Strategy 1: Release Group (Preferred for Singles/Albums)
    mb_result = get_original_date_from_release_group(artist, name)
    strategy = "Release Group"
    
    # Strategy 2: Recording (Fallback)
    if not mb_result:
            mb_result = get_original_date_musicbrainz_recording(artist, name)
            strategy = "Recording"
    
    if mb_result:
        mb_date, mb_year, mb_month, mb_day = mb_result
        
        # Logic: If new year is OLDER, definitely take it.
        # If current_year is not provided, we just return the found date.
        if mb_year and (not current_year or mb_year < current_year):
            # print(f"  -> UPDATE FOUND via {strategy}: {current_year} -> {mb_year} ({mb_date})")
            
            updates = {
                "year": mb_year,
                "release_date": mb_date
            }
            if mb_month:
                updates["month"] = mb_month
            elif current_year and mb_year != current_year:
                # If year changed but we don't have a specific month, reset it (it might be wrong)
                updates["month"] = ""
            
            if mb_day:
                updates["day"] = mb_day
            elif current_year and mb_year != current_year:
                updates["day"] = ""
                
            return updates

    return None


def get_session():
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

def get_original_date_from_release_group(artist, track_name):
    """
    Queries MusicBrainz 'release-group' for the given artist and track.
    Returns a tuple (date_string, year, month, day) or None if not found/error.
    """
    base_url = "https://musicbrainz.org/ws/2/release-group"
    
    # Clean up track name for search (remove parentheses info like "Remastered")
    search_name = track_name
    match = re.search(r"(.*)\s*\(.*\)", track_name)
    if match:
         search_name = match.group(1).strip()

    # Search query
    query = f'artist:"{artist}" AND releasegroup:"{search_name}"'
    headers = {
        "User-Agent": "HitsterDateVerifier/1.0 ( contact@example.com )"
    }
    params = {
        "query": query,
        "fmt": "json",
        "limit": 20
    }

    session = get_session()

    try:
        response = session.get(base_url, params=params, headers=headers)
        if response.status_code != 200:
            print(f"  [ReleaseGroup] HTTP Error: {response.status_code}")
            return None

        data = response.json()
        release_groups = data.get("release-groups", [])
        
        earliest_date = None
        
        for rg in release_groups:
            date = rg.get("first-release-date")
            if date:
                 if earliest_date is None or date < earliest_date:
                     earliest_date = date
                     
        if earliest_date:
             return parse_date(earliest_date)
             
        # print("  [ReleaseGroup] No date found in results.")
        return None

    except Exception as e:
        print(f"Exception during Release Group API call: {e}")
        return None

def get_original_date_musicbrainz_recording(artist, track_name):
    """
    Queries MusicBrainz 'recording' for the given artist and track to find the earliest release date.
    Returns a tuple (date_string, year, month, day) or None if not found/error.
    """
    base_url = "https://musicbrainz.org/ws/2/recording"
    query = f'artist:"{artist}" AND recording:"{track_name}"'
    headers = {
        "User-Agent": "HitsterDateVerifier/1.0 ( contact@example.com )"
    }
    params = {
        "query": query,
        "fmt": "json",
        "limit": 50 
    }

    session = get_session()

    try:
        response = session.get(base_url, params=params, headers=headers)
        if response.status_code != 200:
            print(f"Error querying MusicBrainz: {response.status_code}")
            return None
        
        data = response.json()
        recordings = data.get("recordings", [])
        
        earliest_date = None
        
        for recording in recordings:
            for release in recording.get("releases", []):
                date_str = release.get("date")
                if date_str:
                    # We want the earliest date
                    if earliest_date is None or date_str < earliest_date:
                        earliest_date = date_str
        
        # Search 2: Clean Name (if applicable)
        if "(" in track_name:
            match = re.search(r"(.*)\s*\(.*\)", track_name)
            if match:
                clean_name = match.group(1).strip()
                if clean_name and clean_name != track_name:
                     # print(f"  -> Also searching clean name: {clean_name}")
                     query2 = f'artist:"{artist}" AND recording:"{clean_name}"'
                     params2 = params.copy()
                     params2["query"] = query2
                     
                     try:
                         response2 = session.get(base_url, params=params2, headers=headers)
                         if response2.status_code == 200:
                             data2 = response2.json()
                             recordings2 = data2.get("recordings", [])
                             for recording in recordings2:
                                 for release in recording.get("releases", []):
                                     date_str = release.get("date")
                                     if date_str:
                                         if earliest_date is None or date_str < earliest_date:
                                             earliest_date = date_str
                     except Exception:
                        pass
        
        if earliest_date:
            return parse_date(earliest_date)

        return None

    except Exception as e:
        print(f"Exception during API call: {e}")
        return None

def parse_date(date_str):
    # Parse YYYY-MM-DD or YYYY-MM or YYYY
    parts = date_str.split("-")
    year = parts[0]
    month = ""
    day = ""
    
    if len(parts) > 1:
        try:
            month_idx = int(parts[1])
            if 1 <= month_idx <= 12:
                month = calendar.month_name[month_idx]
        except ValueError:
            pass
    
    if len(parts) > 2:
        try:
            day_val = int(parts[2])
            day = f"{day_val}."
        except ValueError:
            pass
            
    return date_str, year, month, day

def main():
    try:
        with open("songs.json", "r") as f:
            songs = json.load(f)
    except FileNotFoundError:
        print("songs.json not found.")
        return

    songs_fixed = []
    
    print(f"Checking {len(songs)} songs...")

    for i, song in enumerate(songs):
        artist = song["artists"][0] if song["artists"] else ""
        name = song["name"]
        
        print(f"[{i+1}/{len(songs)}] Checking: {name} - {artist}")
        
        # Strategy 1: Release Group (Preferred for Singles/Albums)
        mb_result = get_original_date_from_release_group(artist, name)
        strategy = "Release Group"
        
        # Strategy 2: Recording (Fallback)
        if not mb_result:
             # print("  -> Release Group strategy returned None/No Date. Trying Recording strategy...")
             mb_result = get_original_date_musicbrainz_recording(artist, name)
             strategy = "Recording"
        
        fixed_song = song.copy()
        
        if mb_result:
            mb_date, mb_year, mb_month, mb_day = mb_result
            
            # Use explicit print only for debugging interest or updates
            # print(f"  -> Found date via {strategy}: {mb_date} (Year: {mb_year})")
            
            current_year = str(song.get("year", ""))
            
            # Logic: If new year is OLDER, definitely take it.
            if mb_year and (not current_year or mb_year < current_year):
                print(f"  -> UPDATE FOUND via {strategy}: {current_year} -> {mb_year} ({mb_date})")
                fixed_song["year"] = mb_year
                
                if mb_month: 
                    fixed_song["month"] = mb_month
                elif mb_year != current_year:
                    fixed_song["month"] = "" 

                if mb_day: 
                    fixed_song["day"] = mb_day
                elif mb_year != current_year:
                    fixed_song["day"] = "" 
                    
                fixed_song["release_date"] = mb_date
            else:
                pass
                # print(f"  -> No earlier date found (MB: {mb_year})")
        else:
             pass
             # print("  -> Not found in MusicBrainz")

        songs_fixed.append(fixed_song)
        
        # Sleep to respect API rate limits
        time.sleep(1.2)

    with open("songs_fixed.json", "w") as f:
        json.dump(songs_fixed, f, indent=4)
    
    print("\nVerification complete. Saved to songs_fixed.json")

if __name__ == "__main__":
    main()
