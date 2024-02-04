import argparse, requests, logging, urllib.request, datetime
from fuzzywuzzy import fuzz

def check_m3u_files(m3u_files, channel_names, similarity_ratio):
    records = set()
    for file in m3u_files:
        if file.startswith('http://') or file.startswith('https://'):
            # If the file is a URL, download it
            try:
                response = urllib.request.urlopen(file)
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    logging.info(f"The file {file} was not found.")
                else:
                    logging.debug(f"An HTTP error occurred when trying to access {file}.")
                continue
            except urllib.error.URLError as e:
                logging.debug(f"A URL error occurred when trying to access {file}.")
                continue
            else:
                data = response.read()      # a `bytes` object
                text = data.decode('utf-8') # a `str`; this step can't be used if data is binary
                lines = text.split('\n')
        else:
            # If the file is a file path, read it
            with open(file, 'r') as f:
                lines = f.readlines()

        record = []
        for line in lines:
            line = line.strip()
            if line.startswith('#EXTINF'):
                if record:  # if record is not empty
                    records.add(tuple(record))
                record = [line]  # start a new record
            else:
                record.append(line)
        if record:  # add the last record
            records.add(tuple(record))

    valid_records = []
    for record in records:
        channel_name_in_record = record[0].split(',', 1)[-1].strip()  # extract the channel name
        url_in_record = record[-1]  # extract the URL
        for channel_name in channel_names:
            similarity = fuzz.token_set_ratio(channel_name_in_record, channel_name)
            if similarity >= similarity_ratio:
                try:
                    #response = requests.head(url_in_record, timeout=5)
                    #if response.status_code == 200:
                        valid_records.append(list(record))
                        logging.info(f'Added to the output file: {channel_name_in_record} compared to {channel_name} with a similarity ratio of {similarity}')
                except requests.exceptions.RequestException as e:
                    logging.debug(f'An error occurred while checking {url_in_record}: {e}')
    logging.info(f'Found {len(valid_records)} valid records')
    return valid_records

# Create the parser
parser = argparse.ArgumentParser(description="Check M3U files")

# Add the arguments
parser.add_argument('-f', '--files', nargs='+', help='The M3U files to check')
parser.add_argument('-u', '--urls', nargs='+', help='The M3U URLs to check')
parser.add_argument('-c', '--channel-names', nargs='+', required=True, help='The channel names to compare')
parser.add_argument('-r', '--similarity-ratio', type=int, default=95, help='The similarity ratio')
parser.add_argument('-o', '--output-file', help='The output M3U file')
parser.add_argument('-d', '--debug', action='store_true', help='Enable debug info')

# Parse the arguments
args = parser.parse_args()

# Check if at least one of --files or --urls is specified
if args.files is None and args.urls is None:
    parser.error('At least one of --files or --urls must be specified')

# If the output file is not specified, attach the current date and time to the output file name
if args.output_file is None:
    now = datetime.datetime.now()
    args.output_file = f"output_{now.strftime('%Y-%m-%d-%H-%M-%S')}.m3u"

# Combine the file paths and the URLs
m3u_files = args.files if args.files else []
m3u_files.extend(args.urls if args.urls else [])

# Set the logging level based on the debug flag
if args.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

valid_records = check_m3u_files(m3u_files, args.channel_names, args.similarity_ratio)

# Write the valid records to the output file
with open(args.output_file, 'w') as f:
    f.write('#EXTM3U\n')  # add #EXTM3U to the beginning of the file
    for record in valid_records:
        f.write('\n'.join(record) + '\n')