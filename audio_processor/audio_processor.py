from birdnetlib import Recording
from birdnetlib.analyzer import Analyzer
from database.manager.bird_identifications_manager import BirdIdentificationsManager
from scipy.io.wavfile import write
from util import constants
import sounddevice as sd
import time

class AudioProcessor:

    ANALYZER = Analyzer()

    def __init__(self, clip_interval, sample_rate, channels, confidence_value_threshold):
        self.clip_interval = clip_interval
        self.sample_rate = sample_rate
        self.channels = channels
        self.confidence_value_threshold = confidence_value_threshold

    def initialize_connected_devices(self):
        devices = sd.query_devices()
        if not devices:
            raise RuntimeError("No connected audio devices detected. Please connect a microphone to launch the sentinel")
        else:
            print(f"Detected {len(devices)} connected audio devices:\n")
            for index, device in enumerate(devices): 
                print(f"{index + 1}: {device['name']}")
            device_number = int(input("\nPlease enter the number of the device you would like to use for audio recording, then press enter to continue:\n"))
            sd.default.device = device_number - 1
        return

    def record_clip(self):
        recording = sd.rec(
            frames=int(self.clip_interval * self.sample_rate), 
            samplerate=self.sample_rate,
            channels=self.channels
        )
        sd.wait()
        write(constants.LATEST_AUDIO_CLIP_PATH, self.sample_rate, recording)
        return

    def detect_species_in_clip(self):
        # TODO: Retrieve latitude and longitude for location data
        recording = Recording(
            analyzer=self.ANALYZER,
            path=constants.LATEST_AUDIO_CLIP_PATH,
            min_conf=self.confidence_value_threshold
        )
        recording.analyze()
        return recording.detections

    def gather_data(self, timeout_hours=24):
        self.initialize_connected_devices()
        bird_identifications_manager = BirdIdentificationsManager()
        initial_time = time.monotonic()
        elapsed_time = 0

        while elapsed_time < timeout_hours * 60 * 60:
            self.record_clip()
            detections = self.detect_species_in_clip()
            for detection in detections:
                print(f"Detected {detection['common_name']} with {detection['confidence']} confidence")
                # TODO: Fetch weather & temp via API
                bird_identifications_manager.create_identification(detection['common_name'], 'test', 'test', 98, 2026, 5, 11, 12)

            elapsed_time = time.monotonic() - initial_time
        
        print("Data collection period complete! Terminating in-use resources...")
        bird_identifications_manager.close()
        return
