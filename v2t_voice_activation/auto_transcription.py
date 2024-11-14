import threading
import numpy as np
import pyaudio
from .audio_processing import AudioProcessor
from .transcription_service import TranscriptionService
from .keyword_detection import KeywordDetector
from groq import Groq

class AutoTranscription:
    def __init__(self, 
                 groq_api_key, 
                 porcupine_api_key, 
                 keyword_path="keyword.ppn", 
                 model_file_path="porcupine_params_ru.pv",
                 rate=16000,
                 chunk=512,
                 silence_threshold=20,
                 silence_duration=2,
                 output_filename="audio.m4a",
                 wav_filename="audio.wav",
                 language="ru",
                 result_path="result.txt",
                 microphone_activation_threshold=40,
                 noise_duration=2):
        # Initialize components with default parameters if not provided
        self.audio_processor = AudioProcessor(
            rate,
            chunk,
            silence_threshold,
            silence_duration,
            output_filename,
            wav_filename
        )
        self.transcription_service = TranscriptionService(
            groq_client=Groq(api_key=groq_api_key),
            language=language,
            result_path=result_path
        )
        self.keyword_detector = KeywordDetector(
            keyword_path,
            porcupine_api_key,
            model_file_path
        )
        self.stop_flag = threading.Event()
        self.microphone_activate_flag = threading.Event()
        self.pyaudio_instance = pyaudio.PyAudio()  # PyAudio instance for stream control
        self.microphone_activation_threshold = microphone_activation_threshold,
        self.noise_duration = noise_duration

    def start(self):
        self.stop_flag.clear()
        self.microphone_activate_flag.clear()
        listener_thread = threading.Thread(target=self._listen_for_keyword)
        listener_thread.daemon = True  # Ensure the thread ends when the main process ends
        listener_thread.start()

    def end(self):
        self.stop_flag.set()

    def _listen_for_keyword(self):
        noise_counter = 0
        stream = self.pyaudio_instance.open(
            format=pyaudio.paInt16, channels=1, rate=self.audio_processor.rate,
            input=True, frames_per_buffer=self.audio_processor.chunk
        )

        try:
            print("Listening... say the keyword to activate recording.")
            while not self.stop_flag.is_set():
                data = stream.read(self.audio_processor.chunk)
                audio_data = np.frombuffer(data, dtype=np.int16)
                rms = np.sqrt(np.mean(audio_data**2))
                
                if rms > self.microphone_activation_threshold:
                    self.microphone_activate_flag.set()
                elif noise_counter > (self.audio_processor.rate / self.audio_processor.chunk * self.noise_duration):
                    self.microphone_activate_flag.clear()
                    noise_counter = 0
                    
                if self.microphone_activate_flag.is_set():
                    noise_counter += 1
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
