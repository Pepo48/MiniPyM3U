import sys
from fuzzywuzzy import fuzz

def shrink_m3u(txt_file_path, m3u_file_path, output_file_path, callback):
    # Read the text file and store channel names in a list
    with open(txt_file_path, 'r') as txt_file:
        channels = [line.strip() for line in txt_file]

    # Read the m3u file and write matching records to a new file
    with open(m3u_file_path, 'r') as m3u_file, open(output_file_path, 'w') as output_file:
        record = ''
        for line in m3u_file:
            if line.startswith('#EXTINF'):
                if record:  # if record is not empty, process it
                    name_part = record.split("\n")[0].split(",")[-1].strip() if "," in record else ""
                    for channel in channels:
                        similarity = fuzz.token_set_ratio(channel, name_part)
                        if similarity >= 80:
                            output_file.write(record)
                            callback(f'Successful match: {name_part} with {channel} (similarity: {similarity})\n', "success")
                            break
                        else:
                            callback(f'Failed match: {name_part} with {channel} (similarity: {similarity})\n', "fail")
                record = line  # start a new record
            else:
                record += line  # add to current record