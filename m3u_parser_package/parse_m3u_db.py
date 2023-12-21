"""
parse-m3u.py

This script parses channel names from an m3u file and saves them to a txt file.

Usage:
    python parse_m3u.py <m3u_file_path> <output_file>

Arguments:
    m3u_file_path: The path to the m3u file to parse.
    output_file: The path to the txt file where the channel names will be saved.

Example:
    python parse-m3u.py channels.m3u output.txt
"""

import re
import sys
import os

def parse_m3u(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        sys.exit(1)

    with open(file_path, 'r') as file:
        content = file.readlines()

    channel_names = []
    for line in content:
        if line.startswith('#EXTINF:'):
            # Extract channel name using regex
            match = re.search(r',(.*)', line)
            if match:
                channel_names.append(match.group(1))

    return channel_names

def save_to_txt(channel_names, output_file):
    with open(output_file, 'w') as file:
        for channel in channel_names:
            file.write(f'{channel}\n')

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python parse-m3u.py <m3u_file_path> <output_file>")
        sys.exit(1)

    m3u_file_path = sys.argv[1]
    output_file = sys.argv[2]
    channel_names = parse_m3u(m3u_file_path)
    save_to_txt(channel_names, output_file)