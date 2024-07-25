import re

# Read the list from the file
with open('tracks.txt', 'r') as file:
    lines = file.readlines()

# Function to clean and format the lines
def clean_and_format(line):
    # Remove the './' prefix
    line = line.lstrip('./')
    # Remove leading numbers and spaces
    line = re.sub(r'^\d+\s*', '', line)
    # Remove the '.mp3' suffix and newline character
    line = line.rstrip('.mp3\n')
    # Split artist and song title
    parts = line.split(' - ', 1)
    if len(parts) == 2:
        artist, song = parts
        return f"{artist.strip()} - {song.strip()}"
    return line.strip()

# Process each line
formatted_lines = [clean_and_format(line) for line in lines]

# Write the formatted list to the file
with open('tracks_cleaned.txt', 'w') as file:
    for formatted_line in formatted_lines:
        file.write(formatted_line + '\n')

print("Formatting completed. Check the 'tracks_cleaned.txt' file.")
