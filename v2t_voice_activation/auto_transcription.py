import threading
import numpy as np
import pyaudio
from .audio_processing import AudioProcessor
from .transcription_service import TranscriptionService
from .keyword_detection import KeywordDetector
from groq import Groq

class AutoTranscription:
    def __init__(self, groq_api_key, porcupine_api_key, **kwargs):
        # Initialize components with default parameters if not provided
        self.audio_processor = AudioProcessor(
            rate=kwargs.get("RATE", 16000),
            chunk=kwargs.get("CHUNK", 512),
            silence_threshold=kwargs.get("SILENCE_THRESHOLD", 20),
            silence_duration=kwargs.get("SILENCE_DURATION", 2),
            output_filename=kwargs.get("OUTPUT_FILENAME", "audio.m4a"),
            wav_filename=kwargs.get("WAV_FILENAME", "audio.wav")
        )
        self.transcription_service = TranscriptionService(
            groq_client=Groq(api_key=groq_api_key),
            language=kwargs.get("LANGUAGE", "ru"),
            result_path=kwargs.get("RESULT_PATH", "result.txt")
        )
        self.keyword_detector = KeywordDetector(
            keyword_path=kwargs.get("KEYWORD_PATH", "keyword.ppn"),
            porcupine_api_key=porcupine_api_key,
            model_file_path=kwargs.get("MODEL_FILE_PATH", "porcupine_params_ru.pv")
        )
        self.stop_flag = threading.Event()
        self.pyaudio_instance = pyaudio.PyAudio()  # PyAudio instance for stream control

    def start(self):
        self.stop_flag.clear()
        listener_thread = threading.Thread(target=self._listen_for_keyword)
        listener_thread.daemon = True  # Ensure the thread ends when the main process ends
        listener_thread.start()

    def end(self):
        self.stop_flag.set()

    def _listen_for_keyword(self):
        stream = self.pyaudio_instance.open(
            format=pyaudio.paInt16, channels=1, rate=self.audio_processor.rate,
            input=True, frames_per_buffer=self.audio_processor.chunk
        )

        try:
            print("Listening... say the keyword to activate recording.")
            while not self.stop_flag.is_set():
                data = stream.read(self.audio_processor.chunk)
                audio_data = np.frombuffer(data, dtype=np.int16)

                if self.keyword_detector.detect_keyword(audio_data) >= 0:
                    print("Keyword detected!")
                    stream.stop_stream()

                    # Record and transcribe audio after keyword detection
                    self.audio_processor.record_audio(self.stop_flag)
                    if self.audio_processor.convert_to_wav():
                        transcription_result = self.transcription_service.transcribe_audio(self.audio_processor.wav_filename)
                        if transcription_result:
                            print("Transcription completed. Result:", transcription_result)

                    # Restart listening after transcription is finished
                    print("Listening again...")
                    stream.start_stream()  # Resume stream for listening
        finally:
            # Close the stream and release resources
            stream.close()
            self.pyaudio_instance.terminate()
