# Voice Typing using Whisper on Windows

An implementation of OpenAI Whisper to have on-click dictations using shortcuts similar to Windows Voice Typing.
When you click the plus button you will be able to dictate whatever you want the computer to write, and once clicking the plus button again the computer will insert the text where your cursor is currently is.

## Description

This project utilizes OpenAI's Whisper model to transcribe audio input in real-time. It supports multiple languages and showcases the integration of various libraries including PyAudio, PyAutoGUI, and others to capture audio, process it, and output the transcription.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.7 or later
- A compatible GPU for CUDA (if you wish to use GPU acceleration)
- Linux/Windows/MacOS operating system

## Installation

### Step 1: Clone the repository

Start by cloning the project to your local machine:

```
git clone https://your-repository-link-here
cd your-project-folder
```
### Step 2: Set up a Python virtual environment
It's recommended to use a virtual environment for Python projects. This keeps dependencies required by different projects separate by creating isolated environments for them. To set up a virtual environment, run:

```
python3 -m venv venv
```

### Step 3: Activate the virtual environment
Activate the virtual environment with:

```
venv\Scripts\activate
```

### Step 4: Install the requirements
Install the required Python libraries with:

Run the pip command for each of those, make sure you're in your virtual environment.

```
pip install PyAudio
pip install whisper
pip install keyboard
pip install pyperclip
pip install pyautogui
pip install tk
```

**PyAudio:** Provides Python bindings for PortAudio, a cross-platform audio I/O library. It allows you to easily use Python to play and record audio on a variety of platforms.
**Whisper:** An automatic speech recognition (ASR) system developed by OpenAI. It is trained on a large dataset of diverse audio and can perform tasks such as multilingual speech recognition, speech translation, and language identification. It's designed to be robust to accents, background noise, and technical language.
**Keyboard:** A Python library that allows you to work with keyboard events. You can use it to detect key presses or simulate key presses, making it useful for creating hotkeys, automating tasks, or creating interactive applications.
**Pyperclip:** A cross-platform Python module for copying and pasting text to and from the clipboard. It allows you to programmatically control the clipboard on Windows, macOS, and Linux.
**PyAutoGUI:** A Python module for GUI automation. It allows you to control the mouse and keyboard to automate interactions with other applications. It can be used for tasks such as opening files, entering text, saving documents, etc.
**Tk (Tkinter):** Tkinter is Python's standard GUI (Graphical User Interface) package. It is a thin object-oriented layer on top of Tcl/Tk. Tkinter is included with standard Linux, Microsoft Windows, and macOS installs of Python. The tk package is used to install Tkinter in environments where it might not be available by default.

 if you're gonna use a GPU:
**Torch (PyTorch):** An open-source machine learning library developed by Facebook's AI Research lab. It provides a flexible deep learning framework and is widely used for applications in computer vision, natural language processing, and other areas of artificial intelligence.
```
pip install torch
```
