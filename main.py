import json
import argparse
import os
import shutil
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import time

import qrcode
import spotipy
import typst
from spotipy import SpotifyClientCredentials
import qrcode.image.svg
import logging
import calendar

from gameset_config import GAMESETS
import verify_dates

logging.basicConfig(level=logging.INFO)


def get_env_var(key):
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(f"Environment variable {key} is required but not set.")
    return value


def resolve_date(date_str):
    date_parts = date_str.split("-")[::-1]
    parts = [""] * (3 - len(date_parts)) + date_parts

    day = f"{int(parts[0])}." if parts[0] else ""
    month = calendar.month_name[int(parts[1])] if parts[1] else ""
    year = parts[2]

    return day, month, year

def get_spotify_data_batch(sp, card_entries):
    """
    Fetches track data from Spotify in batches.
    card_entries: List of dicts {CardNumber, Spotify}
    """
    songs = []
    
    # Extract IDs, filtering out any empty ones
    track_ids = [entry["Spotify"] for entry in card_entries if entry.get("Spotify")]

    chunk_size = 50
    total_tracks = len(track_ids)
    
    logging.info(f"Fetching metadata for {total_tracks} tracks...")

    fetched_tracks = {}

    for i in range(0, total_tracks, chunk_size):
        batch = track_ids[i : i + chunk_size]
        try:
            results = sp.tracks(batch)
            for track in results["tracks"]:
                if track:
                    fetched_tracks[track["id"]] = track
        except Exception as e:
            logging.error(f"Error fetching batch {i}: {e}")
            
    # Reassemble songs list preserving order of card_entries
    for entry in card_entries:
        spotify_id = entry.get("Spotify")
        card_number = entry.get("CardNumber")
        
        if not spotify_id or spotify_id not in fetched_tracks:
            logging.warning(f"Track data not found for Card {card_number} (ID: {spotify_id})")
            continue

        track = fetched_tracks[spotify_id]
        day, month, year = resolve_date(track["album"]["release_date"])
        
        song = {
            "name": track["name"],
            "artists": [artist["name"] for artist in track["artists"]],
            "day": day,
            "month": month,
            "year": year,
            "release_date": track["album"]["release_date"],
            "url": track["external_urls"]["spotify"],
            "id": track["id"],
            "CardNumber": card_number 
        }
        songs.append(song)
        
    return songs


def generate_qr_codes(songs, config, country_code):
    if os.path.isdir(f"qr_codes_{country_code}"):
        shutil.rmtree(f"qr_codes_{country_code}")
    os.mkdir(f"qr_codes_{country_code}")

    sku = config['sku']
    
    # URL Pattern: https://www.hitstergame.com/{country}/{sku}/{CardNumber}
    
    for song in songs:
        card_number = song.get("CardNumber")
        if not card_number:
            logging.warning(f"Song {song.get('name')} missing CardNumber, skipping QR generation.")
            continue
            
        url = f"https://www.hitstergame.com/{country_code}/{sku}/{card_number}"
        
        img = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage)
        img.save(f"qr_codes_{country_code}/{song['id']}.svg")


def generate_overview_pdf(songs, output_pdf):
    year_counts = Counter(int(song["year"]) for song in songs if "year" in song and song["year"])

    if not year_counts:
        logging.warning("No year data found for overview PDF.")
        return

    min_year = min(year_counts.keys())
    max_year = max(year_counts.keys())
    all_years = list(range(min_year, max_year + 1))
    counts = [year_counts.get(year, 0) for year in all_years]

    plt.figure()
    plt.bar(all_years, counts, color="black")
    plt.ylabel("number of songs released")
    # plt.xticks() 

    with PdfPages(output_pdf) as pdf:
        pdf.savefig()
        plt.close()


def main():
    parser = argparse.ArgumentParser(description="Hitster Game Generator")
    parser.add_argument("--file", help="Path to a JSON file containing songs (Legacy/Override)")
    parser.add_argument("--country", default="br", help="Country code for gameset configuration (default: br)")
    parser.add_argument("--db", default="database.json", help="Path to database.json")
    parser.add_argument("--limit", type=int, help="Limit number of songs to process (for testing)")
    args = parser.parse_args()

    country_code = args.country
    gameset_key = None
    
    # Helper map for likely codes to Config Keys
    # Note: gameset_config.py keys are like "Brazil", "United Kingdom"
    code_map = {
        "br": "Brazil",
        "us": "United States of America",
        "uk": "United Kingdom",
        "de": "Germany",
        "es": "Spain",
        "nl": "Netherlands",
        "fr": "France",
        "it": "Italy",
        "mx": "Mexico",
        "ca": "Canada",
        "pl": "Poland",
        "au": "Australia"
    }
    
    # Try direct match or map match
    if country_code in GAMESETS:
        gameset_key = country_code
    elif country_code in code_map and code_map[country_code] in GAMESETS:
        gameset_key = code_map[country_code]
    else:
        # Fallback: Search values for matching keys (case insensitive)
        for k in GAMESETS:
            if k.lower() == country_code.lower():
                gameset_key = k
                break
    
    if not gameset_key:
         logging.error(f"Could not find gameset config for country '{country_code}'.")
         return

    config = GAMESETS[gameset_key]
    sku = config.get("sku")
    logging.info(f"Selected Gameset: {gameset_key} (SKU: {sku})")

    songs = []

    if args.file:
        logging.info(f"Loading songs from {args.file}")
        with open(args.file, "r") as file:
            songs = json.load(file)
    else:
        # Load from database.json
        if not os.path.exists(args.db):
             logging.error(f"Database file {args.db} not found.")
             return
             
        with open(args.db, "r") as f:
            db_data = json.load(f)
            
        # Find matches for SKU
        card_entries = []
        for gameset in db_data.get("gamesets", []):
             if gameset.get("sku") == sku:
                 card_entries = gameset["gameset_data"]["cards"]
                 break
        
        if not card_entries:
            logging.error(f"No cards found for SKU {sku} in database.")
            return

        logging.info(f"Found {len(card_entries)} cards for {gameset_key}.")

        sp = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=get_env_var("CLIENT_ID"),
                client_secret=get_env_var("CLIENT_SECRET"),
            )
        )

        songs = get_spotify_data_batch(sp, card_entries)

    if args.limit:
        logging.info(f"Limiting to first {args.limit} songs for testing.")
        songs = songs[:args.limit]

    # Verification Step
    logging.info("Verifying release dates...")
    for i, song in enumerate(songs):
        updates = verify_dates.verify_song_date(
            song["artists"][0] if song["artists"] else "",
            song["name"],
            song["year"]
        )
        if updates:
            logging.info(f"Updating {song['name']}: {song['year']} -> {updates['year']}")
            song.update(updates)
        
        # Rate limit kindness
        time.sleep(1.2) 

    logging.info("Writing songs to file")
    with open(f"songs_{country_code}.json", "w") as file:
        json.dump(songs, file, indent=4)

    logging.info("Generating QR codes")
    generate_qr_codes(songs, config, country_code) 

    logging.info("Compiling Cards PDF")
    typst.compile("hitster.typ", output=f"hitster_{country_code}.pdf")

    logging.info("Compiling Year Overview PDF")
    generate_overview_pdf(songs, f"overview_{country_code}.pdf")

    logging.info("Done")

if __name__ == "__main__":
    main()
