from audio_processor.audio_processor import AudioProcessor
from database.manager.bird_identifications_manager import BirdIdentificationsManager
from pathlib import Path
from util import constants
from audio_processor.audio_processor import AudioProcessor
import argparse

'''
Entry point for the treehouse sentinel. Launches the data-gathering script
'''

DEFAULT_CLIP_LENGTH_SECONDS = 60
DEFAULT_SAMPLE_RATE = 48000
DEFAULT_CHANNELS = 2
DEFAULT_CONFIDENCE_VALUE_THRESHOLD = 0.9

def parse_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "-th",
        "--timeout-hours",
        type=int, 
        help=("Optional parameter for the number of hours before the sentinel stops collecting data "
             "(default is 24)"), 
        required=False
    )
    arg_parser.add_argument(
        "-ci",
        "--clip-interval",
        type=int, 
        help="Optional parameter for the duration of each evaluated audio clip in seconds (default is 60)", 
        required=False
    )
    arg_parser.add_argument(
        "-sr",
        "--sample-rate",
        type=int, 
        help="Optional parameter for the sample rate of your recording device in kHz (default is 48000)", 
        required=False
    )
    arg_parser.add_argument(
        "-c",
        "--channels",
        type=int, 
        help="Optional parameter for the number of channels you wish to record with (default is 2 for stereo audio)", 
        required=False
    )
    arg_parser.add_argument(
        "-cvt",
        "--confidence-value-threshold",
        type=float, 
        help=("Optional parameter for the confidence value threshold the model must breach before saving an "
             "identification. Ranges from 0 to 1.0 (0 - 100%% confidence, default is 0.9)"), 
        required=False
    )
    return arg_parser.parse_args()

def main():
    # Initialize args
    args = parse_args()
    clip_interval = args.clip_interval if args.clip_interval else DEFAULT_CLIP_LENGTH_SECONDS
    sample_rate = args.sample_rate if args.sample_rate else DEFAULT_SAMPLE_RATE
    channels = args.channels if args.channels else DEFAULT_CHANNELS
    confidence_value_threshold = args.confidence_value_threshold if args.confidence_value_threshold else DEFAULT_CONFIDENCE_VALUE_THRESHOLD

    # Initialize files
    Path(constants.TABLE_STORAGE_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(constants.TABLE_STORAGE_PATH).touch()
    Path(constants.LATEST_AUDIO_CLIP_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(constants.LATEST_AUDIO_CLIP_PATH).touch()

    # Begin audio processing loop
    try:
        audio_processor = AudioProcessor(clip_interval, sample_rate, channels, confidence_value_threshold)
        audio_processor.gather_data(args.timeout_hours) if args.timeout_hours else audio_processor.gather_data()
        print("\nData collection timeout reached. Shutting down the sentinel...")
    except KeyboardInterrupt:
        print("\nShutting down the sentinel at the user's request...")

if __name__ == "__main__":
    main()
