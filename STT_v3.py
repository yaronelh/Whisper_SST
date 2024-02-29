# Created by Yaron Elharar
# version: 0.51
#
# Other optimizations to consider 
# https://cookbook.openai.com/examples/whisper_processing_guide


import pyaudio
import wave
import os
import whisper
import keyboard
import pyperclip
import pyautogui
import threading
import torch
import tkinter as tk
from tkinter import Toplevel
import time
import queue
import re 

message_queue = queue.Queue()
FORMAT = pyaudio.paInt16
exit_flag = False
overlay_window = None
overlay_visible = False
model = None
is_recording = False
model_last_used_time = None
temp_directory = "temp"
original_clipboard = None

# 1. Which model do you want to use?
#   Size	    Parameters	English-only    model	    Multilingual model	Required VRAM	Relative speed
#   tiny	    39 M	    tiny.en	        tiny	    ~1 GB	                            ~32x
#   base	    74 M	    base.en	        base	    ~1 GB	                            ~16x
#   small	    244 M	    small.en	    small	    ~2 GB	                            ~6x
#   medium	    769 M	    medium.en	    medium	    ~5 GB	                            ~2x
#   large	    1550 M	    N/A         	large	    ~10 GB	                            1x
#   large-v2	1550 M	    N/A 	        large-v2    ?                                   ?
#   large-v3	1550 M	    N/A            	large-v3    ?                                   ?

SelectedModel = "base.en"
selected_language = "en"  # Default to English

# 2. Testing what to use, GPU or CPU 
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Is a compatible GPU available: {torch.cuda.is_available()}")
print("Loading Whisper model...")

# 3. This needs to be set to your own microphone rate and chunk 
CHANNELS = 1
RATE = 48000
CHUNK = 1024


# 4. Choose which shortcuts will activate the recordings.
# If you want to know the scan code of a particular key run this command "python -m keyboard", and update the numbers accordingly
# The numbers below 78 and 74 are the plus and minus scan code of the numpad on my particular keyboard 

keyboard.add_hotkey(78, lambda: toggle_recording("en"), suppress=True)
keyboard.add_hotkey(74, lambda: toggle_recording("he"), suppress=True)

# List of available languages languages https://github.com/openai/whisper/blob/main/whisper/tokenizer.py


##
## Beyond this point change only if you know what your doing 
##

start_time = time.time()  # Start time capture
model = whisper.load_model(SelectedModel).to(device)
end_time = time.time()  # End time capture
print(f"Model loading took {end_time - start_time} seconds")

# Ensure temporary directory exists
if not os.path.exists(temp_directory):
    os.makedirs(temp_directory)

# Toggle recording state with language selection
def toggle_recording(language):
    global is_recording, original_clipboard, selected_language
    if not is_recording:
        # Save the current clipboard content before starting recording
        original_clipboard = pyperclip.paste()
        # Update the selected language based on the hotkey pressed
        selected_language = language
    is_recording = not is_recording
    print(f"Recording {'started' if is_recording else 'stopped'} in {selected_language}")

# Wait for exit signal
def listen_for_exit():
    global exit_flag
    keyboard.wait('esc')
    exit_flag = True
    print("Exit signal received.")

# Transcribe audio to text, modified to accept language parameter
def save_and_transcribe(frames, selected_language):
    global model, model_last_used_time, original_clipboard, device
    if not frames:
        print("No audio data recorded.")
        return
    start_time1 = time.time()  # Start time capture
    temp_audio_file_path = os.path.join(temp_directory, "recording.wav")
    with wave.open(temp_audio_file_path, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    end_time1 = time.time()  # End time capture
    print(f"Preparing audio file took: {end_time1 - start_time1} seconds")
    
    if model is None:
        model = whisper.load_model(SelectedModel).to(device)
    model_last_used_time = time.time()

    print("Transcribing...")
    start_time = time.time()  # Start time capture
    result = model.transcribe(temp_audio_file_path, language=selected_language)
    end_time = time.time()  # End time capture
    transcribed_text = result['text']
    transcribed_text = re.sub(r'^\s+', '', transcribed_text)
    transcribed_text = re.sub(r'\.+$', ' ', transcribed_text)
    #regular expression to lowercase some common words that need to be lower case when in the middle of a sentence 
    transcribed_text = re.sub('^(?!I |I.*?''|I'')\w', convert_to_lower, transcribed_text)
    print(f"Transcription took {end_time - start_time} seconds")
    print(f"Transcription: {result['text']}")
    message_queue.put(transcribed_text)

    # After pasting the transcription, restore the original clipboard content
    def restore_clipboard():
        global original_clipboard
        pyperclip.copy(original_clipboard)
        original_clipboard = None  # Clear the stored clipboard content after restoring

    # Schedule the clipboard restoration to ensure it happens after the paste operation
    root.after(100, restore_clipboard)

# Replacement function to convert uppercase letter to lowercase
def convert_to_lower(match_obj):
    if match_obj.group() is not None:
        return match_obj.group().lower()


def process_queue_messages():
    while not message_queue.empty():
        start_time = time.time()  # Start time capture
        message = message_queue.get()
        # Perform Tkinter operations or clipboard operations with the message
        pyperclip.copy(message)
        pyautogui.hotkey('ctrl', 'v')
        message_queue.task_done()
        end_time = time.time()  # End time capture
        print(f" pasting process took {end_time - start_time} seconds")
    # Schedule this function to run again after a short delay
    root.after(100, process_queue_messages)


# Record audio
def record_audio():
    global is_recording, selected_language
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("Ready. Press '+' to start/stop recording. Press 'ESC' to exit.")

    frames = []
    while not exit_flag:
        if is_recording:
            if overlay_window: show_overlay()
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
        else:
            # If not recording, sleep for a short time to prevent high CPU usage
            time.sleep(0.1)  # Sleep for 100 milliseconds

        if not is_recording and frames:
            save_and_transcribe(frames, selected_language)  # Pass the selected language for transcription
            hide_overlay()
            frames = []

    stream.stop_stream()
    stream.close()
    p.terminate()

# Create and manage overlay window
def create_overlay():
    global overlay_window
    overlay_window = Toplevel()
    overlay_window.overrideredirect(True)
    overlay_window.attributes("-topmost", True)
    overlay_window.attributes("-transparentcolor", "white")
    canvas = tk.Canvas(overlay_window, width=16, height=16, bg="white", highlightthickness=0)
    canvas.pack()
    canvas.create_oval(2, 2, 14, 14, fill="red")
    overlay_window.withdraw()

# Update overlay position
def update_overlay_position():
    if overlay_window and overlay_visible:
        x, y = pyautogui.position()
        overlay_window.geometry(f"+{x+20}+{y+20}")
        overlay_window.after(100, update_overlay_position)

# Show overlay
def show_overlay():
    global overlay_visible
    if not overlay_window:
        create_overlay()
    overlay_visible = True
    overlay_window.deiconify()
    update_overlay_position()

# Hide overlay
def hide_overlay():
    global overlay_visible
    overlay_visible = False
    if overlay_window:
        overlay_window.withdraw()

# Exit application
def exit_application():
    global exit_flag
    exit_flag = True
    keyboard.unhook_all_hotkeys()
    if overlay_window:
        overlay_window.destroy()

# Unload model if unused
def unload_model_if_unused():
    global model, model_last_used_time
    if model and model_last_used_time and (time.time() - model_last_used_time > 120):
        print("Unloading Whisper model due to inactivity...")
        model = None
    if not exit_flag:
        threading.Timer(30, unload_model_if_unused).start()

def main_application_logic():
    global root
    root = tk.Tk()
    root.withdraw()  # This hides the main Tkinter window
    threading.Thread(target=listen_for_exit, daemon=True).start()
    threading.Thread(target=record_audio, daemon=True).start()
    threading.Thread(target=unload_model_if_unused, daemon=True).start()

    create_overlay()

    # Schedule the first call to process queue messages
    root.after(100, process_queue_messages)

    # Check for exit flag and exit application if set
    def check_exit():
        if exit_flag:
            exit_application()
            root.destroy()  # This will stop the Tkinter event loop
        else:
            root.after(100, check_exit)

    # Schedule the first call to check for exit
    root.after(100, check_exit)

    root.mainloop()  # Start the Tkinter event loop

if __name__ == "__main__":
    main_application_logic()
