from pydub import AudioSegment
from tkinter import Tk, filedialog

import os

def convert_audio(input_file, output_file):
  audio = AudioSegment.from_file(input_file)
  audio = audio.set_channels(1)
  audio = audio.set_sample_width(2)
  audio = audio.set_frame_rate(48000)
  audio.export(output_file, format="wav")

def main():
  root = Tk()
  root.withdraw()

  input_file = filedialog.askopenfilename(
    title="Select Audio File",
    filetypes=[("Audio Files", "*.mp3 *.wav *.ogg *.flac *.aac *.m4a")]
  )

  if input_file:
    base, ext = os.path.splitext(input_file)
    output_file = base + "_converted.wav"

    convert_audio(input_file, output_file)
    print(f"Converted {input_file} to {output_file} successfully.")
  else:
    print("No file selected.")

if __name__ == "__main__":
  main()
