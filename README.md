# Voice Typing using Whisper on Windows
(Written by Yaron Elharar)

OpenAI Whisper for on-click dictations using shortcuts, similar to Windows Voice Typing. When you click the plus button, you will be able to dictate whatever you want the computer to write. Once you click the plus button again, the computer will insert the text where your cursor currently is. This is similar to what Windows Voice Typing does, or, if you're familiar, Dragon NaturallySpeaking. You can directly dictate in 99 different languages.

- English
- Spanish
- French
- German
- Chinese
- Hebrew
- Arabic
- etc.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.11
- A compatible GPU for CUDA (if you wish to use GPU acceleration)

## Installation

### Step 1: Install Python

- Visit the official Python website at https://www.python.org/downloads/ and download the Python v3.11.8 from the "looking for a specific release?" section.
- In the installation process make sure that "Add python.exe to PATH" is checked.

### Step 2: Preparing the environment

Open a CMD command line and navigate to the folder you would like Whisper_SST to be installed in. If your not sure on [how to navigate a CMD (command line)](https://github.com/yaronelh/Whisper_SST/blob/main/How%20do%20i%20navigate%20in%20a%20Windows%20cmd%20(command%20Line).md) you can use this quick guide I prepared.

**Set up a virtual environment**

let's set up a virtual environment for the project, that will make it possible for you to have multiple Python projects running at the same time with different Python versions and setups.
This will isolate Whisper_SST to its own area.

```cmd
python3 -m venv venv
```

### Step 3: Activate the virtual environment
Activate the virtual environment with:

```cmd
venv\Scripts\activate
```

### Step 4: Install the requirements
Install the required Python libraries with:

Run the pip command for each of those, make sure you're in your virtual environment.

```cmd
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

```cmd
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

#### How to change the dictation languages

The code provides shortcuts for two languages (English, and Hebrew), but you can change the shortcuts or languages to fit your needs by changing this line.

```python
keyboard.add_hotkey('+', lambda: toggle_recording("en"), suppress=True)
keyboard.add_hotkey('-', lambda: toggle_recording("he"), suppress=True)
```

You can find the list of [whispers supported languages here](https://github.com/openai/whisper/blob/main/whisper/tokenizer.py)

If you want to use specific keys and you don't know exactly their names, you can get their scan code number and place it instead of the name of the key or its character 
for example, In my case I wanted to use the plus button but only the numpad plus button. Not the other one on the keyboard.

You would run this command, and click on any key on your keyboard to get its scan code.
```cmd
python -m keyboard
```

Then replace the name of the key with its scan code in the Python script 
```python
# 78 numpad plus button on my keyboard, yours may differ.
keyboard.add_hotkey(78 , lambda: toggle_recording("en"), suppress=True)
```

#### how to change the Whisper model you're using 

```python
SelectedModel = "small"
selected_language = "en"  # Default to English
print("Loading Whisper model...")
model = whisper.load_model(SelectedModel)
```

 **Available model sizes**


| Size      | Parameters | English-only model | Multilingual model | Required VRAM | Relative speed |
|-----------|------------|--------------------|--------------------|---------------|----------------|
| tiny      | 39 M       | tiny.en            | tiny               | ~1 GB         | ~32x           |
| base      | 74 M       | base.en            | base               | ~1 GB         | ~16x           |
| small     | 244 M      | small.en           | small              | ~2 GB         | ~6x            |
| medium    | 769 M      | medium.en          | medium             | ~5 GB         | ~2x            |
| large     | 1550 M     | N/A                | large              | ~10 GB        | 1x             |
| large-v2  | 1550 M     | N/A                | large-v2           | ?             | ?              |
| large-v3  | 1550 M     | N/A                | large-v3           | ?             | ?              |


Which model to choose is a balance between speed and accuracy, choose whatever works for your machine.

** Note that when running the script for the first time, you would not have any model installed. So the model will be automatically downloaded to your computer. In addition each time you change a model, and it doesn't exist, the first thing the script will do is download the model.

 ### Running the script

 Since this is all happening in the command line, to run the script you will go to the folder, you installed the script in, activate your Python virtual environment and run the script.

- Run cmd
- navigate to the folder you've installed all the components in.
- Activate the virtual environment.
  ```cmd
  venv\Scripts\activate
  ```
- Run the file.
  ```cmd
  Python STT3.py
  ```

To sum up, if everything worked correctly, every time you click the plus button, a small red circle will appear next to your mouse cursor. And while this circle is on, you can dictate as much as you want. Once you click the plus button again, the circle will disappear, and the dictation will be inserted in the input field you are currently in.

This is a side project for me. I will try to offer support, but no promises. 
If you have any questions about the project posted in the X thread over here >> [https://x.com/YaronElharar/status/1762482033375215816](https://x.com/YaronElharar/status/1762482033375215816)
