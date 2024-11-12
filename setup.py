from setuptools import setup, find_packages

setup(
    name="v2t_voice_activation",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pyaudio",
        "pvporcupine",
        "pydub",
        "groq",
        "requests",
    ],
    author="Mikhail Ostrovsky",
    author_email="oty998@gmail.com",
    description="A library for converting speech to text. With activation via voice command.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/oty-v/v2t_voice_activation",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "v2t-voice-activation=v2t_voice_activation.cli:main",
        ],
    },
)
