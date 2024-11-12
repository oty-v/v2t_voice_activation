import os

class TranscriptionService:
    def __init__(self, groq_client, language="ru", result_path="result.txt"):
        self.client = groq_client
        self.language = language
        self.result_path = result_path

    def transcribe_audio(self, wav_filename):
        if not os.path.exists(wav_filename):
            print(f"Error: file {wav_filename} not found.")
            return None
        
        try:
            with open(wav_filename, "rb") as file:
                transcription = self.client.audio.transcriptions.create(
                    file=file,
                    model="whisper-large-v3-turbo",
                    language=self.language,
                    response_format="verbose_json",
                )
                
                # Write transcription text to a file
                try:
                    with open(self.result_path, "w", encoding="utf-8") as text_file:
                        text_file.write(transcription.text)
                    print(f"Transcription saved to {self.result_path}")
                except Exception as e:
                    print(f"Error writing transcription to file: {e}")
                    return f"Error writing to file: {e}"
                
                return transcription.text
        except Exception as e:
            print(f"Error during transcription: {e}")
            return f"Error during transcription: {e}"
