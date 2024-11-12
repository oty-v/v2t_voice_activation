# v2t_voice_activation

**v2t_voice_activation** is a Python library for voice-activated transcription and keyword detection. It allows you to record audio based on specific keyword detection, transcribe the audio, and save the transcription result to a file. The library uses the **Porcupine** keyword detection engine and **Groq API** for transcription services.

## Features
- Detects a custom keyword via the **Porcupine** keyword detection engine.
- Records audio after detecting the keyword.
- Transcribes the recorded audio using the **Groq transcription service**.
- Saves the transcription to a text file.

## Technologies Used
- **Porcupine**: A lightweight and efficient wake-word detection library.
- **Groq API**: For transcribing audio into text.
- **PyAudio**: For capturing audio from the microphone.
- **Numpy**: For audio signal processing.
- **Pydub**: For audio file conversion.
- **Threading**: To handle simultaneous listening and transcription processes.

## Installation

To install the library, clone this repository and install the required dependencies:

```bash
git clone https://github.com/oty-v/v2t_voice_activation.git
cd v2t_voice_activation
pip install .
```

## Overview
This library allows you to perform voice activation for transcription services. It integrates with the Groq API for transcription and the Porcupine engine for wake-word detection. The system listens for a specific wake-word and transcribes audio into text once the keyword is detected.

## 1. API Keys
You need two API keys for the library to work:

- **Groq API Key**: For transcription services.
- **Porcupine API Key**: For wake-word detection.

### How to Get the API Keys

#### Groq API Key:
1. Go to the [Groq website](https://groq.com) and sign up for an API key.
2. Once signed up, you'll be able to generate your API key from the Groq dashboard.

#### Porcupine API Key:
1. Visit the [Porcupine website](https://picovoice.ai) to get an API key.
2. Sign up and generate your API key from the dashboard.

## 2. Porcupine Model File & Keyword File
For the Porcupine engine to detect your custom keyword, you'll need two files:

- **Keyword File**: This file contains the wake-word or keyword you're detecting (e.g., "keyword").
- **Model File**: This file is used by Porcupine to process audio data and detect the keyword.

### How to Get the Required Files

#### Porcupine Model File (porcupine_params_ru.pv):
1. Download the model for Russian language from the [Porcupine GitHub repository](https://github.com/Picovoice/porcupine).
2. Alternatively, you can find the model file on the Porcupine documentation page.

#### Keyword File (keyword.ppn):
1. You can create a custom keyword file using the [Picovoice Console](https://console.picovoice.ai/).
   - Sign in, create a new project, select your preferred language (e.g., Russian), and generate the `.ppn` file.
2. Alternatively, you can find pre-existing keyword models in the Picovoice resources.

## Usage

### Initialize the Library
To start using the library, initialize it with your API keys and file paths:

```python
from v2t_voice_activation import AutoTranscription

groq_api_key = "your_groq_api_key"
porcupine_api_key = "your_porcupine_api_key"

# Initialize the AutoTranscription class
auto_transcription = AutoTranscription(
    groq_api_key=groq_api_key,
    porcupine_api_key=porcupine_api_key,
    keyword_path="path_to_sora.ppn",  # Path to the custom keyword file
    model_file_path="path_to_porcupine_params_ru.pv"  # Path to the Porcupine model file
)

# Start the listening process
auto_transcription.start()

# To stop listening and transcription
auto_transcription.end()

```

This project provides an automatic transcription solution that listens for a keyword, records audio, transcribes it, and saves the transcription result. It uses the Groq API for transcription and includes options to customize the recording and transcription process.

## Workflow

### Start Listening:
- Call `auto_transcription.start()` to begin listening for the keyword.
- Once the keyword is detected, the library will record audio.

### Record Audio and Transcribe:
- After the keyword is detected, audio is recorded until silence is detected.
- The recorded audio is then converted to a `.wav` file and transcribed using the Groq API.

### Saving Transcription:
- The transcription result is saved to a text file (default: `result.txt`).

### Stop Listening:
- Call `auto_transcription.end()` to stop the process at any time.

## Example

```python
auto_transcription.start()

# After the keyword is detected and transcription is completed
# The result will be printed:
# "Transcription finished. Result: [Transcribed text]"
```

# AutoTranscription Configuration and Troubleshooting

## Configuration Options

You can configure the following parameters when initializing the `AutoTranscription` class:

- **RATE**: The sample rate for audio recording (default: 16000).
- **CHUNK**: The number of frames per buffer (default: 512).
- **SILENCE_THRESHOLD**: The volume threshold to detect silence (default: 20).
- **SILENCE_DURATION**: The duration of silence (in seconds) before stopping the recording (default: 2).
- **OUTPUT_FILENAME**: The name of the output file for recorded audio (default: `audio.m4a`).
- **WAV_FILENAME**: The name of the output file for converted WAV audio (default: `audio.wav`).
- **LANGUAGE**: The language for transcription (default: `"ru"` for Russian).
- **RESULT_PATH**: The path to save the transcription result (default: `result.txt`).

## Troubleshooting

### No Sound Detected:
- Ensure your microphone is working properly and is set as the default recording device.
- Check that the silence threshold is correctly configured for your environment.

### Transcription Error:
- Verify that the Groq API key and Porcupine API key are correct.
- Ensure that the audio file is valid and in the supported format.

### Keyword Detection Not Working:
- Make sure the correct model file (`porcupine_params_ru.pv`) and keyword file (`keyword.ppn`) are used.
- If you are using a custom keyword, re-check the keyword file and ensure it's correctly formatted.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
