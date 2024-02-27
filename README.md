# Voice Typing using Whisper on Windows

An implementation of OpenAI Whisper to have on-click dictations using shortcuts similar to Windows Voice Typing.
When you click the plus button you will be able to dictate whatever you want the computer to write, and once clicking the plus button again the computer will insert the text where your cursor is currently is.

## Description

This project utilizes OpenAI's Whisper model to transcribe audio input in real-time. It supports multiple languages and showcases the integration of various libraries including PyAudio, PyAutoGUI, and others to capture audio, process it, and output the transcription.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.11
- A compatible GPU for CUDA (if you wish to use GPU acceleration)

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

**If you're gonna use a Nvidia GPU:**  

**Torch (PyTorch):** An open-source machine learning library developed by Facebook's AI Research lab. It provides a flexible deep learning framework and is widely used for applications in computer vision, natural language processing, and other areas of artificial intelligence.

```
pip install torch
```


### Step 5: Install CUDA (Optional)
If you wish to utilize Nvidia GPU acceleration with Torch, ensure your system has CUDA installed. This will significantly improve processing speed. CUDA installation can vary based on your system, choose your setup from the options on these pages.

```
You can install CUDA from here.
https://developer.nvidia.com/cuda-downloads

And cuDNN from here
https://developer.nvidia.com/cudnn
```

###  Additional instructions.

The code provides shortcuts for two languages, but you can change the shortcuts or languages to fit your needs.
by changing this line.

```
keyboard.add_hotkey('+', lambda: toggle_recording("en"), suppress=True)
keyboard.add_hotkey('-', lambda: toggle_recording("he"), suppress=True)
```

You can find the list of [whispers supported languages here](https://github.com/openai/whisper/blob/main/whisper/tokenizer.py)

**You can also change the whisper model you want to use by changing this section of code:**
```
# Which model do you want to use?
#   Size	    Parameters	English-only    model	    Multilingual model	Required VRAM	Relative speed
#   tiny	    39 M	    tiny.en	        tiny	    ~1 GB	                            ~32x
#   base	    74 M	    base.en	        base	    ~1 GB	                            ~16x
#   small	    244 M	    small.en	    small	    ~2 GB	                            ~6x
#   medium	    769 M	    medium.en	    medium	    ~5 GB	                            ~2x
#   large	    1550 M	    N/A         	large	    ~10 GB	                            1x
#   large-v2	1550 M	    N/A 	        large-v2    ?                                   ?
#   large-v3	1550 M	    N/A            	large-v3    ?                                   ?

SelectedModel = "small"
selected_language = "en"  # Default to English
print("Loading Whisper model...")
model = whisper.load_model(SelectedModel)
```

Which model to choose is a balance between speed and accuracy, choose whatever works for your machine.

** Note that when running the script for the first time, you would not have any model installed. So the model will be automatically downloaded to your computer. In addition each time you change a model, and it doesn't exist, the first thing the script will do is download the model.

