import pvporcupine

class KeywordDetector:
    def __init__(self, keyword_path, porcupine_api_key, model_file_path):
        try:
            # Initialize Porcupine with API key and paths
            self.porcupine = pvporcupine.create(
                keyword_paths=[keyword_path],
                access_key=porcupine_api_key,
                model_path=model_file_path
            )
        except Exception as e:
            # Handle initialization error
            print(f"Error initializing Porcupine: {e}")
            self.porcupine = None

    def detect_keyword(self, audio_data):
        if self.porcupine is None:
            print("Porcupine was not initialized.")
            return None
        if audio_data is None or len(audio_data) == 0:
            print("Error: Audio data is empty.")
            return None
        try:
            # Process audio data and check for the keyword
            result = self.porcupine.process(audio_data)
            return result
        except Exception as e:
            # Handle error during keyword detection
            print(f"Error processing audio data: {e}")
            return None

    def __del__(self):
        if self.porcupine:
            self.porcupine.delete()
            print("Porcupine resources released.")
