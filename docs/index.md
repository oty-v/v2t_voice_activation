# v2t_voice_activation Documentation

Welcome to the official documentation for **v2t_voice_activation**! This library allows for voice-activated transcription and keyword detection. It integrates the **Porcupine** keyword detection engine for wake-word detection and the **Groq API** for transcribing audio to text.

## Table of Contents
1. [Introduction](#introduction)
2. [Technologies Used](#technologies-used)
3. [Installation](#installation)
4. [Prerequisites](#prerequisites)
5. [Usage](#usage)
6. [Configuration Options](#configuration-options)
7. [Troubleshooting](#troubleshooting)
8. [License](#license)

## Introduction

The **v2t_voice_activation** library provides a powerful solution for voice-based transcription and automation. With it, you can set up a system that listens for a custom wake-word, records audio when the keyword is detected, transcribes the audio, and saves the transcriptions to a file.

## Technologies Used

This library utilizes the following technologies:
- **Porcupine**: A lightweight wake-word detection engine.
- **Groq API**: A service for transcribing audio to text.
- **PyAudio**: A Python library for capturing audio from your microphone.
- **Numpy**: A library for processing audio signals.
- **Pydub**: Used for converting audio files into the appropriate format.
- **Threading**: To handle background tasks like listening for keywords while recording and transcribing audio.

## Installation

To install the **v2t_voice_activation** library, clone the repository and install the required dependencies:

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/v2t_voice_activation.git
cd v2t_voice_activation
```

## Prerequisites

Before using this library, ensure that you have the following:

### 1. API Keys

You will need two API keys for the library to function properly:

- **Groq API Key**: For transcription services.
- **Porcupine API Key**: For wake-word detection.

#### How to Get the API Keys:

- **Groq API Key**:
  1. Go to the [Groq website](https://groq.com/).
  2. Sign up for an account.
  3. Once signed up, navigate to the Groq dashboard to generate your API key.

- **Porcupine API Key**:
  1. Visit the [Porcupine website](https://picovoice.ai/porcupine/).
  2. Sign up for an account.
  3. After signing in, navigate to the dashboard to generate your Porcupine API key.

### 2. Porcupine Model File & Keyword File

For **Porcupine** to detect your custom keyword, you'll need the following files:

- **Keyword File (sora.ppn)**: A file that contains the wake-word you're detecting (e.g., "Sora").
- **Model File (porcupine_params_ru.pv)**: The file required for Porcupine to process the audio.

#### How to Get the Required Files:

- **Porcupine Model File (porcupine_params_ru.pv)**:
  - Download the model for the Russian language from the [Porcupine GitHub repository](https://github.com/Picovoice/porcupine) or the [Porcupine documentation page](https://picovoice.ai/docs/).
  
- **Keyword File (sora.ppn)**:
  - Create a custom keyword file using the [Picovoice Console](https://console.picovoice.ai/).
    1. Sign in to the console.
    2. Create a new project.
    3. Select your preferred language (e.g., Russian).
    4. Generate the `.ppn` keyword file for your custom wake word.
  - Alternatively, you can find pre-existing keyword models in the Picovoice resources.

## Usage

### 1. Initialize the Library

To start using the library, you need to initialize it with the necessary API keys and file paths:

```python
from v2t_voice_activation import AutoTranscription

# Your API keys
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

## 2. Workflow

### Start Listening
Call `auto_transcription.start()` to begin listening for the keyword. The library will wait for the specified wake word to be detected.

### Record Audio and Transcribe
Once the keyword is detected, the library will start recording audio until silence is detected. Afterward, the recorded audio will be converted to a `.wav` file and sent to the Groq API for transcription.

### Saving Transcription
The transcription result will be saved in a text file (default: `result.txt`).

### Stop Listening
Call `auto_transcription.end()` to stop the process at any time.

## Example

```python
auto_transcription.start()

# After the keyword is detected and transcription is completed
# The result will be printed:
# "Transcription finished. Result: [Transcribed text]"
```

## Configuration Options

When initializing the `AutoTranscription` class, you can configure the following parameters:

- **RATE**: The sample rate for audio recording (default: `16000`).
- **CHUNK**: The number of frames per buffer (default: `512`).
- **SILENCE_THRESHOLD**: The volume threshold to detect silence (default: `20`).
- **SILENCE_DURATION**: The duration of silence (in seconds) before stopping the recording (default: `2`).
- **OUTPUT_FILENAME**: The name of the output file for recorded audio (default: `audio.m4a`).
- **WAV_FILENAME**: The name of the output file for converted WAV audio (default: `audio.wav`).
- **LANGUAGE**: The language for transcription (default: `"ru"` for Russian).
- **RESULT_PATH**: The path to save the transcription result (default: `result.txt`).

## Troubleshooting

Here are some common issues and solutions:

### No Sound Detected:
- Ensure that your microphone is set up and works correctly.
- Check if the silence threshold is properly configured for your environment.

### Transcription Error:
- Ensure that the Groq API key and Porcupine API key are correct.
- Verify that the audio file is in the correct format (WAV).

### Keyword Detection Not Working:
- Make sure you're using the correct model file (`porcupine_params_ru.pv`) and keyword file (`sora.ppn`).
- If you're using a custom keyword, check that the `.ppn` file is correctly formatted.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
