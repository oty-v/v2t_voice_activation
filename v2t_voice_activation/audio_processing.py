import os
import numpy as np
import wave
import pyaudio
from pydub import AudioSegment

class AudioProcessor:
    def __init__(self, rate=16000, chunk=512, silence_threshold=20, silence_duration=2, output_filename="audio.m4a", wav_filename="audio.wav"):
        self.rate = rate
        self.chunk = chunk
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        self.output_filename = output_filename
        self.wav_filename = wav_filename

        # Initialize PyAudio
        self.p = pyaudio.PyAudio()

    def record_audio(self, stop_flag):
        print("Recording started...")
        frames = []
        silence_counter = 0

        stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=self.rate, input=True, frames_per_buffer=self.chunk)
        
        try:
            while not stop_flag.is_set():
                data = stream.read(self.chunk)
                audio_data = np.frombuffer(data, dtype=np.int16)
                frames.append(data)

                rms = np.sqrt(np.mean(audio_data**2))
                print(f"Volume level: {rms}")

                if rms < self.silence_threshold:
                    silence_counter += 1
                    print(f"Silence detected. Silence counter: {silence_counter}")
                else:
                    silence_counter = 0  # Reset counter if sound is above threshold

                if silence_counter > (self.rate / self.chunk * self.silence_duration):
                    print("Recording finished due to silence.")
                    break
        finally:
            # Ensure the stream is closed even if an error occurred
            stream.stop_stream()
            stream.close()

        # Save audio to file
        with wave.open(self.output_filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(frames))

        if os.path.getsize(self.output_filename) > 0:
            print(f"File saved as {self.output_filename}")
        else:
            print(f"Error: {self.output_filename} is empty.")

    def convert_to_wav(self):
        if os.path.getsize(self.output_filename) == 0:
            print(f"Error: {self.output_filename} is empty.")
            return False

        if not os.path.exists(self.output_filename):
            print(f"File {self.output_filename} does not exist.")
            return False

        print(f"Converting {self.output_filename} to WAV...")
        try:
            audio = AudioSegment.from_file(self.output_filename)
            if len(audio) == 0:
                print(f"Error: {self.output_filename} does not contain audio.")
                return False
            audio.export(self.wav_filename, format="wav")
            print(f"Converted to {self.wav_filename}")
            return True
        except Exception as e:
            print(f"Error during conversion: {e}")
            return False
