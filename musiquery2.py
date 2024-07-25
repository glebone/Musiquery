import re
import spotipy
import chardet
import argparse
import os
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Script to create Spotify playlist from CUE or TXT files.")
parser.add_argument('-cue', type=str, help="Path to the CUE file.")
parser.add_argument('-txt', type=str, help="Path to the TXT file.")
parser.add_argument('-folder', type=str, help="Path to the folder containing music files.")
args = parser.parse_args()

# Set up your client credentials
client_id = ''
client_secret = ''
redirect_uri = "http://localhost:8888/callback"
mi_playlist_id = "1iKbel9fJK63aJHGal7Qri"

def get_tracks_from_cue(cue_file):
    tracks = []
    title_pattern = re.compile(r'TITLE "(.*?)"')
    performer_pattern = re.compile(r'PERFORMER "(.*?)"')

    # First, detect the encoding of the cue file
    with open(cue_file, 'rb') as f:  # Open file in binary mode
        raw_data = f.read()
        encoding = chardet.detect(raw_data)['encoding']
        print(f"Detected encoding: {encoding}")

    # Now, read the file using the detected encoding
    with open(cue_file, 'r', encoding=encoding) as f:
        cue_sheet = f.read()
        titles = title_pattern.findall(cue_sheet)
        performers = performer_pattern.findall(cue_sheet)
        titles = titles[1:]  # Skipping the first title as it may be the album's title

    for title, performer in zip(titles, performers):
        tracks.append((performer, title))
    return tracks

def clean_and_format(line):
    # Remove the './' prefix
    line = line.lstrip('./')
    # Remove leading numbers and spaces
    line = re.sub(r'^\d+\s*', '', line)
    # Remove the '.mp3' suffix and newline character
    line = line.rstrip('.mp3\n')
    return line

def parse_filename(filename):
    # Split artist and song title
    parts = filename.split(' - ', 1)
    if len(parts) == 2:
        artist = parts[0].strip()
        song = parts[1].strip()
        return artist, song
    return None, None

def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".cue") or filename.endswith(".txt"):
            continue  # Skip CUE and TXT files
        artist, track = parse_filename(filename)
        if artist and track:
            print(f"Artist: {artist}, Track: {track}")
        else:
            print(f"Could not parse filename: {filename}")

def get_tracks_from_txt(txt_file):
    tracks = []
    with open(txt_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                cleaned_line = clean_and_format(line)
                artist, track = parse_filename(cleaned_line)
                if artist and track:
                    tracks.append((artist, track))
                else:
                    print(f"Could not parse line: {line}")
    return tracks

def search_and_add_to_playlist(sp, playlist_id, artist, track):
    query = f"artist:{artist} track:{track}"
    results = sp.search(q=query, type='track', limit=1)
    if results['tracks']['items']:
        track_id = results['tracks']['items'][0]['id']
        sp.playlist_add_items(playlist_id, [track_id])
        print(f"Added {artist} - {track} to playlist.")
    else:
        print(f"Track {artist} - {track} not found on Spotify.")

if __name__ == "__main__":
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="playlist-modify-public playlist-modify-private"))

    if args.folder:
        process_folder(args.folder)
    elif args.cue:
        tracks = get_tracks_from_cue(args.cue)
        for artist, track in tracks:
            search_and_add_to_playlist(sp, mi_playlist_id, artist, track)
    elif args.txt:
        tracks = get_tracks_from_txt(args.txt)
        for artist, track in tracks:
            search_and_add_to_playlist(sp, mi_playlist_id, artist, track)
