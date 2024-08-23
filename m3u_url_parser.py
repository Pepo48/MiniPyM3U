import re
import argparse
from urllib.parse import urlparse

def parse_m3u_urls(text, skip_duplicates):
    # Regular expression to find M3U/M3U8 URLs
    url_pattern = re.compile(r'https?://[^\s]+(?:\.m3u8?|type=m3u8?|type=m3u)')
    urls = url_pattern.findall(text)
    
    if skip_duplicates:
        seen_domains = set()
        filtered_urls = []
        for url in urls:
            domain = urlparse(url).netloc
            if domain not in seen_domains:
                seen_domains.add(domain)
                filtered_urls.append(url)
        return filtered_urls
    else:
        return urls

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Parse M3U/M3U8 URLs from text")

    # Add the arguments
    parser.add_argument('-t', '--text', required=True, help='The text to parse')
    parser.add_argument('--skip-duplicates', action='store_true', help='Skip multiple URLs from the same domain')

    # Parse the arguments
    args = parser.parse_args()

    # Parse the URLs
    urls = parse_m3u_urls(args.text, args.skip_duplicates)

    # Print the URLs
    for url in urls:
        print(url)

if __name__ == "__main__":
    main()