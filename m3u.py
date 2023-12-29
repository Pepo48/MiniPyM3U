import argparse
import requests
from fuzzywuzzy import fuzz
import logging

def check_m3u_files(m3u_files, channel_names, similarity_ratio):
    valid_records = []
    for file in m3u_files:
        with open(file, 'r') as f:
            record = []
            for line in f:
                line = line.strip()
                if line.startswith('#EXTINF'):
                    if record:  # if record is not empty
                        channel_name_in_record = record[0].split(',', 1)[-1].strip()  # extract the channel name
                        url_in_record = record[-1]  # extract the URL
                        for channel_name in channel_names:
                            similarity = fuzz.token_set_ratio(channel_name_in_record, channel_name)
                            if similarity >= similarity_ratio:
                                try:
                                    response = requests.head(url_in_record)
                                    if response.status_code == 200:
                                        valid_records.append('\n'.join(record))
                                        logging.info(f'Added to the output file: {channel_name_in_record} compared to {channel_name} with a similarity ratio of {similarity}')
                                except requests.exceptions.RequestException as e:
                                    logging.debug(f'An error occurred while checking {url_in_record}: {e}')
                    record = [line]  # start a new record
                else:
                    record.append(line)
    return valid_records

# Create the parser
parser = argparse.ArgumentParser(description="Check M3U files")

# Add the arguments
parser.add_argument('-f', '--files', nargs='+', required=True, help='The M3U files to check')
parser.add_argument('-c', '--channel-name', nargs='+', required=True, help='The channel names to compare')
parser.add_argument('-r', '--similarity-ratio', type=int, default=70, help='The similarity ratio')
parser.add_argument('-o', '--output-file', required=True, help='The output M3U file')
parser.add_argument('-d', '--debug', action='store_true', help='Enable debug info')

# Parse the arguments
args = parser.parse_args()

# Set the logging level based on the debug flag
if args.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

valid_records = check_m3u_files(args.files, args.channel_names, args.similarity_ratio)

# Write the valid records to the output file
with open(args.output_file, 'w') as f:
    f.write('#EXTM3U\n')  # add #EXTM3U to the beginning of the file
    for record in valid_records:
        f.write(record + '\n')