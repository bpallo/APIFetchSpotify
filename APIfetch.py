import csv
import json
import os
import re
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables(.env) from client_creds.env file
load_dotenv("client_creds.env")

# Define the name of the output CSV and JSON files
OUTPUT_CSV_FILE_NAME = "playlist_tracks.csv"
OUTPUT_JSON_FILE_NAME = "playlist_tracks.json"

# Define the link to the Spotify playlist
PLAYLIST_LINK = "https://open.spotify.com/playlist/0FsNO0GQVwtSBysxY48zxR"

# Get client ID and client secret from .env
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Authenticate with Spotify using OAuth 2.0
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="playlist-read-private"))

# Extract playlist ID from the link
playlist_id_match = re.match(r"https://open.spotify.com/playlist/([a-zA-Z0-9]+)", PLAYLIST_LINK)
if playlist_id_match:
    playlist_id = playlist_id_match.group(1)
else:
    print("Error: Invalid playlist link format.")
    print("Expected format: https://open.spotify.com/playlist/...")
    exit(1)

# Get playlist information
playlist_info = sp.playlist(playlist_id)
print("Playlist Name:", playlist_info['name'])
print("Owner:", playlist_info['owner']['display_name'])

# Retrieve tracks from the playlist
playlist_tracks = sp.playlist_tracks(playlist_id)["items"]

# Print song names,  artists, and albums
print("Songs in the Playlist:")
for track in playlist_tracks:
    if track.get("track"):
        name = track["track"]["name"]
        artists = ", ".join([artist["name"] for artist in track["track"]["artists"]])
        album = track["track"]["album"]["name"]
        print(f"{name} by {artists}, Album: {album}")
    else:
        print("No track information available")

# Write track info to CSV
with open(OUTPUT_CSV_FILE_NAME, "w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["track", "artist", "album"])  # Write header row

    for track in playlist_tracks:
        name = track["track"]["name"]
        artists = ", ".join([artist["name"] for artist in track["track"]["artists"]])
        album = track["track"]["album"]["name"]
        csv_writer.writerow([name, artists, album])

# Write track info to JSON
json_data = []
for track in playlist_tracks:
    name = track["track"]["name"]
    artists = [artist["name"] for artist in track["track"]["artists"]]
    album = track["track"]["album"]["name"]
    json_data.append({"track": name, "artists": artists, "album": album})

with open(OUTPUT_JSON_FILE_NAME, "w") as json_file:
    json.dump(json_data, json_file, indent=4)

print("CSV and JSON files created successfully.")
