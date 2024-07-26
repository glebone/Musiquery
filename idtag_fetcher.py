import os
import argparse
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC

def get_mp3_info(mp3_path):
    try:
        audio = EasyID3(mp3_path)
        artist = audio.get('artist', ['Unknown Artist'])[0]
        title = audio.get('title', ['Unknown Title'])[0]
        return artist, title
    except Exception as e:
        print(f"Error reading {mp3_path}: {e}")
        return None, None

def get_flac_info(flac_path):
    try:
        audio = FLAC(flac_path)
        artist = audio.get('artist', ['Unknown Artist'])[0]
        title = audio.get('title', ['Unknown Title'])[0]
        return artist, title
    except Exception as e:
        print(f"Error reading {flac_path}: {e}")
        return None, None

def find_audio_files(directory):
    audio_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.mp3') or file.endswith('.flac'):
                audio_files.append(os.path.join(root, file))
    return audio_files

def gather_audio_info(directory, output_file):
    audio_files = find_audio_files(directory)
    with open(output_file, 'w') as f:
        for audio_file in audio_files:
            if audio_file.endswith('.mp3'):
                artist, title = get_mp3_info(audio_file)
            elif audio_file.endswith('.flac'):
                artist, title = get_flac_info(audio_file)
            else:
                continue
            
            if artist and title:
                f.write(f"{artist} - {title}\n")

def main():
    parser = argparse.ArgumentParser(description="Extract artist and track name from MP3 and FLAC files.")
    parser.add_argument("directory", type=str, help="Directory to search for audio files")
    parser.add_argument("output_file", type=str, help="Output file to write the results")
    args = parser.parse_args()

    gather_audio_info(args.directory, args.output_file)
    print(f"Audio information has been written to {args.output_file}")

if __name__ == "__main__":
    main()
