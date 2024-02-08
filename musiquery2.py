"""
     ^..^ CAT Soft - MS-Musiquery
	 ----------------------------
	 Script for 
	    - getting tracks from the CUE files,
		- searching for track in Spotify
		- adding track to the given playlist 
		- added encoding detection - 6 Feb 2024
	-----------------------------
	12 Jul 2023 || glebone@gmail.com 
"""
import re
import spotipy
import chardet
import argparse
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth




# Parse command-line arguments
parser = argparse.ArgumentParser(description="Script to create Spotify playlist from CUE or TXT files.")
parser.add_argument('-cue', type=str, help="Path to the CUE file.")
parser.add_argument('-txt', type=str, help="Path to the TXT file.")
args = parser.parse_args()


# Set up your client credentials
client_id = ""
client_secret = ""
redirect_uri = "http://localhost:8888/callback"
mi_playlist_id = "1O0GgXGfYaDXtxQcg9hjyt"  
cue_file = "./2.cue"

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
        performers = performers[1:]  # Same for performers
        tracks = [f'{performer} - {title}' for performer, title in zip(performers, titles)]
    return tracks


def get_tracks_from_txt(txt_file):
    tracks = []
    with open(txt_file, 'r', encoding='utf-8') as f:
        for line in f:
            # Assuming each line follows the 'Artist – Track Title' format
            match = re.match(r'^(.*?) – (.*?)$', line.strip())
            if match:
                artist, title = match.groups()
                tracks.append(f'{artist} - {title}')
    return tracks

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope='user-read-private playlist-modify-private'))


if args.cue:
    tracks = get_tracks_from_cue(args.cue)
elif args.txt:
    tracks = get_tracks_from_txt(args.txt)
else:
    raise ValueError("No valid input file provided. Use -cue or -txt.")
											   
# Get current user's info
user_info = sp.current_user()
# Extract user id
user_id = user_info['id']


print(tracks)


if tracks:
	for track_name in tracks:
		print("Searching for track...")
		print(track_name)
		
		results = sp.search(q=track_name, limit=1, type='track')
		# Print results
		first_track_uri = ""
		if results:
			for cur in results['tracks']['items']:
				first_track_uri = cur['uri']
				print("Found track:...")
				print(first_track_uri)
				break
			print(first_track_uri)
			sp.playlist_add_items(mi_playlist_id, [first_track_uri])
			print("Track added to playlist")
			print("=====================================")










