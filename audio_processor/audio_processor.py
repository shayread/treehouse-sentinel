import time
import sounddevice as sd
from database.manager.bird_identifications_manager import BirdIdentificationsManager

class AudioProcessor:

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
        return recording

    def process_clip(self, recording):
        return

    def gather_data(self, timeout_hours=24):
        self.initialize_connected_devices()
        bird_identifications_manager = BirdIdentificationsManager()
        initial_time = time.monotonic()
        elapsed_time = 0

        while elapsed_time < timeout_hours * 60 * 60:
            recording = self.record_clip()
            species, confidence = self.process_clip(recording)

            if confidence >= self.confidence_value_threshold:
                # TODO: Fetch weather & temp via API
                bird_identifications_manager.create_identification(species, 'test', 'test', 98)

            elapsed_time = time.monotonic() - initial_time
        
        print("Data collection period complete! Terminating in-use resources...")
        bird_identifications_manager.close()
        return
