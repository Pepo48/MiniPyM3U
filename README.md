# MiniPyM3U

This project is a Python script that checks M3U files and compares channel names based on a similarity ratio.

## Installation

To install the required dependencies, run the following command:

```sh
pip install -r requirements.txt
```

## Usage

Run the script with the required arguments:
```sh
python m3u.py -f file1.m3u file2.m3u -c channel1 channel2 -o output.m3u
```

### Arguments
* -f, --files: The M3U files to check
* -c, --channel-names: The channel names to compare, e.g. TNT Sports, BT Sports, Premier Sports, Peacock, Sky Sports, SuperSport, BBC One
* -r, --similarity-ratio: The similarity ratio (default is 65)
* -o, --output-file: The output M3U file
* -d, --debug: Enable debug info

To use this package, run the `app.py` script:
```sh
python app.py
```

This will open a GUI where you can select an M3U file to process. The processed file will be saved as `output.m3u` in the project root directory.

## Testing

To run the tests, use the `test.m3u` file in the `tests` directory.

## Contributing

Contributions are welcome. Please open an issue to discuss your idea before making a pull request.

## License

This project is licensed under the terms of the MIT license.