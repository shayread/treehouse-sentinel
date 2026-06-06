import argparse
from pathlib import Path
from util import constants
from audio_processor.audio_processor import AudioProcessor

'''
Entry point for the treehouse sentinel. Launches the data-gathering script
'''

def parse_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "-t",
        "--timeout-hours",
        type=int, 
        help="Optional parameter for the number of hours before the sentinel powers down", 
        required=False
    )
    return arg_parser.parse_args()

def main():
    # Initialize args, dependencies, and .db file
    args = parse_args()
    Path(constants.TABLE_STORAGE_PATH).touch()

    # Begin audio processing loop
    try:
        audio_processor = AudioProcessor()
        audio_processor.gather_data(args.timeout_hours) if args.timeout_hours else audio_processor.gather_data()
        print("Shutting down the sentinel...")
    except KeyboardInterrupt:
        print("Shutting down the sentinel at the user's request...")

if __name__ == "__main__":
    main()
