# Created by Yaron Elharar
# version: 0.58 
# Last updated: 27/03/2025 (DD/MM/YYYY)


import pyaudio
import wave
import os
import keyboard
import pyperclip
import pyautogui
import threading
import torch
import tkinter as tk
import time
import queue
import re
from faster_whisper import WhisperModel
from tkinter import Toplevel

torch.set_float32_matmul_precision('medium')
torch.backends.cudnn.benchmark = True
torch.set_num_threads(4)  # Adjust based on your CPU
torch.set_num_interop_threads(1)

if torch.cuda.is_available():
    torch.cuda.empty_cache()
    torch.backends.cudnn.benchmark = True

message_queue = queue.Queue()
FORMAT = pyaudio.paInt16
exit_flag = False
overlay_window = None
overlay_visible = False
model = None
is_recording = False
model_last_used_time = time.perf_counter()
appdata_dir = os.path.expandvars("%APPDATA%")
temp_directory = os.path.join(appdata_dir, "temp-231r57")
original_clipboard = None
capitalize_first_use = 0

# 1. Which model do you want to use?
#   Size	    Parameters	English-only    model	    Multilingual model	Required VRAM	Relative speed
#   tiny	    39 M	    tiny.en	        tiny	    ~1 GB	                            ~32x
#   base	    74 M	    base.en	        base	    ~1 GB	                            ~16x
#   small	    244 M	    small.en	    small	    ~2 GB	                            ~6x
#   medium	    769 M	    medium.en	    medium	    ~5 GB	                            ~2x
#   large	    1550 M	    N/A         	large	    ~10 GB	                            1x
#   large-v2	1550 M	    N/A 	        large-v2    ?                                   ?
#   large-v3	1550 M	    N/A            	large-v3    ?                                   ?

#SelectedModel = "base.en"
#SelectedModel = "medium" #if you need to write in Hebrew 
SelectedModel = "small.en" #if you need to write in Hebrew 
selected_language = "en"  # Default to English

# 2. Testing what to use, GPU or CPU 
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Is a compatible GPU available: {torch.cuda.is_available()}")
print("Loading Whisper model...")

# 3. This needs to be set to your own microphone rate and chunk 
CHANNELS = 1
RATE = 16000  # Instead of 48000
CHUNK = 1024   # Instead of 4096


# 4. Choose the languages that will be transcript
# List of available languages languages https://github.com/openai/whisper/blob/main/whisper/tokenizer.py

first_language = 'en'
second_language = 'he'

# 5. Choose which shortcuts will activate the recordings.
# If you want to know the scan code of a particular key run this command "python -m keyboard", and update the numbers accordingly
# The numbers below 78 and 74 are the plus and minus scan code of the numpad on my particular keyboard 

first_language_hotkey = 78
#first_language_hotkey = "+"
#second_language_hotkey = 74  

#exit_program_key = "F12" # I've written F12 for my own needs, but you can return it to 'esc' to use the escape button 


##Okay, let's see how we can handle it basically the same thingdon't see any difference 
## Beyond this point change only if you know what your doing 
##

keyboard.add_hotkey(first_language_hotkey, lambda: toggle_recording(first_language), suppress=True)
#keyboard.add_hotkey(second_language_hotkey, lambda: toggle_recording(second_language), suppress=True)


start_time = time.perf_counter()  # Start time capture
model = WhisperModel(SelectedModel,device="cuda",compute_type="float16",cpu_threads=4,num_workers=1)
#model = WhisperModel(SelectedModel,device="cuda",compute_type="int8",cpu_threads=4,num_workers=1) 
end_time = time.perf_counter()  # End time capture
print(f"Model loading took {end_time - start_time} seconds")
print("Model will remain loaded until the application is closed.")

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
#def listen_for_exit():
#    global exit_flag
##    exit_flag = True
#    print(f"Exit signal received. {exit_program_key}")

# Transcribe audio to text, modified to accept language parameter
def save_and_transcribe(frames, selected_language):
    global model, model_last_used_time, original_clipboard, device, capitalize_first_use
    if not frames:
        print("No audio data recorded.")
        return
    start_time1 = time.perf_counter()  # Start time capture
    temp_audio_file_path = os.path.join(temp_directory, "recording.wav")
    with wave.open(temp_audio_file_path, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    end_time1 = time.perf_counter()  # End time capture
    print(f"Preparing audio file took: {end_time1 - start_time1} seconds")
    
    if model is None:
        model = WhisperModel(SelectedModel,device="cuda",compute_type="float16",cpu_threads=4,num_workers=2)
    

    print("Transcribing...")
    start_time = time.perf_counter()  # Start time capture
    segments, info = model.transcribe(temp_audio_file_path, language=selected_language,without_timestamps=True,beam_size=1)
    #segments, info = model.transcribe(temp_audio_file_path,beam_size=1,language=selected_language)
    transcribed_text = " ".join([segment.text for segment in segments])
    print(f"Transcription: {transcribed_text}")
    end_time = time.perf_counter()  # End time capture
    transcribed_text = re.sub(r'^\s+', '', transcribed_text)
    transcribed_text = re.sub(r'\.+$', ' ', transcribed_text)

    #regular expression to lowercase some common words that need to be lower case when in the middle of a sentence 
    if capitalize_first_use == 0 and (time.perf_counter() - model_last_used_time < 50):
        capitalize_first_use += 1
        print("111")
    elif (time.perf_counter() - model_last_used_time < 10):
        t = time.perf_counter() - model_last_used_time

        transcribed_text = re.sub('^(?!I |I.*?''|I'')\w', convert_to_lower, transcribed_text)
        capitalize_first_use += 1
        print(f"222  -- {t}")
    else:
        capitalize_first_use = 0
        print("3")

    print(f"Transcription took {end_time - start_time} seconds")
    message_queue.put(transcribed_text)

    # After pasting the transcription, restore the original clipboard content 
    def restore_clipboard():
        global original_clipboard
        pyperclip.copy(original_clipboard)
        original_clipboard = None  # Clear the stored clipboard content after restoring

    # Schedule the clipboard restoration to ensure it happens after the paste operation
    root.after(100, restore_clipboard)
    
    # reset timer of when the last time the model was used
    print(f"model_last_used_time Test: {model_last_used_time}")
    model_last_used_time = time.perf_counter()

# Replacement function to convert uppercase letter to lowercase checking 
def convert_to_lower(match_obj):
    if match_obj.group() is not None:
        return match_obj.group().lower()


def process_queue_messages():
    while not message_queue.empty():
        start_time = time.perf_counter()  # Start time capture
        message = message_queue.get()
        # Perform Tkinter operations or clipboard operations with the message
        pyperclip.copy(message)
        pyautogui.hotkey('ctrl', 'v')
        message_queue.task_done()
        end_time = time.perf_counter()  # End time capture
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
    global exit_flag, model
    exit_flag = True
    keyboard.unhook_all_hotkeys()
    
    # Properly unload the model when exiting
    if model:
        print("Unloading Whisper model on exit...")
        model = None
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    
    if overlay_window:
        overlay_window.destroy()

# Unload model if unused
def unload_model_if_unused():
    # This function is kept for compatibility but will not unload the model automatically
    # The model will only be unloaded when the application exits
    pass

def main_application_logic():
    global root
    root = tk.Tk()
    root.withdraw()  # This hides the main Tkinter window
    #threading.Thread(target=listen_for_exit, daemon=True).start()
    threading.Thread(target=record_audio, daemon=True).start()
    # Removed the thread that would unload the model automatically
    # threading.Thread(target=unload_model_if_unused, daemon=True).start()

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
