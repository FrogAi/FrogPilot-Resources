from pydub import AudioSegment
from tkinter import Tk, filedialog

import os
import shutil

TARGET_DBFS = -14.0

def match_target_amplitude(sound, target_dBFS):
  change_in_dBFS = target_dBFS - sound.dBFS
  return sound.apply_gain(change_in_dBFS)

def convert_audio(input_file):
  audio = AudioSegment.from_file(input_file)

  base, ext = os.path.splitext(input_file)
  backup_file = base + "_original" + ext

  if not os.path.exists(backup_file):
    shutil.copy2(input_file, backup_file)

  audio = audio.set_channels(1)
  audio = audio.set_sample_width(2)
  audio = audio.set_frame_rate(48000)

  normalized_audio = match_target_amplitude(audio, TARGET_DBFS)
  normalized_audio.export(input_file, format="wav")

def main():
  root = Tk()
  root.withdraw()

  input_files = filedialog.askopenfilenames(
    title="Select Audio Files",
    filetypes=[("Audio Files", "*.mp3 *.wav *.ogg *.flac *.aac *.m4a")]
  )

  if input_files:
    for input_file in input_files:
      convert_audio(input_file)
      print(f"Converted and overwrote {input_file} successfully.")
  else:
    print("No files selected.")

if __name__ == "__main__":
  main()
