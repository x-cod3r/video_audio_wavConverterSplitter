import os
import tkinter as tk
from tkinter import filedialog
import moviepy.editor as mp

def convert_to_wav(input_file, sample_rate, max_splits, split_duration):
    output_file = os.path.splitext(input_file)[0] + '.wav'

    if input_file.endswith('.mp3'):
        clip = mp.AudioFileClip(input_file)
    else:
        clip = mp.VideoFileClip(input_file) if input_file.endswith(('.mp4', '.avi', '.mkv')) else mp.AudioFileClip(input_file)

    audio = clip.audio if hasattr(clip, "audio") else clip
    audio = audio.set_fps(sample_rate)
    audio.write_audiofile(output_file, codec='pcm_s16le')

    # Split the audio into smaller files based on the desired duration
    split_duration = split_duration  # Split duration in seconds

    output_clip = mp.AudioFileClip(output_file)
    duration = output_clip.duration

    num_splits = min(max_splits, int(duration // split_duration))
    for i in range(num_splits):
        start_time = i * split_duration
        end_time = (i + 1) * split_duration
        split_output_file = f"{os.path.splitext(output_file)[0]}_{i}.wav"
        split_audio = output_clip.subclip(start_time, end_time)
        split_audio = split_audio.set_fps(sample_rate)  # Set sample rate for the split audio
        split_audio.write_audiofile(split_output_file, codec='pcm_s16le')

    output_clip.close()

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Video/Audio Files", "*.mp4 *.avi *.mkv *.mp3")])
    entry_file_path.delete(0, tk.END)
    entry_file_path.insert(tk.END, file_path)

def start_conversion():
    input_file = entry_file_path.get()
    sample_rate = int(entry_sample_rate.get())
    max_splits = int(entry_max_splits.get())
    split_duration = int(entry_split_duration.get())
    convert_to_wav(input_file, sample_rate, max_splits, split_duration)
    lbl_status.config(text="Conversion completed successfully!")

# Create the main window
window = tk.Tk()
window.title("Video/Audio Converter")
window.geometry("400x350")

# Create the GUI components
lbl_file_path = tk.Label(window, text="Input File:")
lbl_file_path.pack()
entry_file_path = tk.Entry(window, width=50)
entry_file_path.pack()
btn_browse = tk.Button(window, text="Browse", command=browse_file)
btn_browse.pack()

lbl_sample_rate = tk.Label(window, text="Sample Rate (Hz):")
lbl_sample_rate.pack()
entry_sample_rate = tk.Entry(window, width=10)
entry_sample_rate.pack()

lbl_max_splits = tk.Label(window, text="Max Splits:")
lbl_max_splits.pack()
entry_max_splits = tk.Entry(window, width=10)
entry_max_splits.pack()

lbl_split_duration = tk.Label(window, text="Split Duration (seconds):")
lbl_split_duration.pack()
entry_split_duration = tk.Entry(window, width=10)
entry_split_duration.pack()

btn_convert = tk.Button(window, text="Convert", command=start_conversion)
btn_convert.pack()

lbl_status = tk.Label(window, text="")
lbl_status.pack()

# Start the GUI event loop
window.mainloop()
