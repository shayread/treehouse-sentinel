import time
import sounddevice
from database.manager.bird_identifications_manager import BirdIdentificationsManager

class AudioProcessor:

    CONFIDENCE_VALUE_THRESHOLD = 0.9

    def verify_connected_devices(self):
        devices = sounddevice.query_devices()
        devices
        if not devices:
            raise RuntimeError("No connected audio devices detected. Please connect a microphone to launch the sentinel")
        else:
            print(f"Detected {len(devices)} connected audio devices: \n{devices}")
        return

    def record_clip(self):
        return

    def process_clip(self, recording):
        return

    def gather_data(self, timeout_hours=24):
        self.verify_connected_devices()
        bird_identifications_manager = BirdIdentificationsManager()
        initial_time = time.monotonic()
        elapsed_time = 0

        while elapsed_time < timeout_hours * 60 * 60:
            recording = self.record_clip()
            species, confidence = self.process_clip(recording)

            if confidence >= self.CONFIDENCE_VALUE_THRESHOLD:
                # TODO: Fetch weather & temp via API
                bird_identifications_manager.create_identification(species, 'test', 'test', 98)

            elapsed_time = time.monotonic() - initial_time
        
        print("Data collection period complete! Terminating in-use resources...")
        bird_identifications_manager.close()
        return
