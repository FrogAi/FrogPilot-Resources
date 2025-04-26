import numpy as np
import os
import pyloudnorm as pyln
import resampy
import shutil
import soundfile as sf

from tkinter import Tk, filedialog

TARGET_LUFS = -15.0
TARGET_RATE = 48000

def loudness_normalize(input_file):
  data, rate = sf.read(input_file)
  if data.ndim > 1:
    data = data.mean(axis=1)

  meter = pyln.Meter(rate)
  loudness = meter.integrated_loudness(data)
  data = pyln.normalize.loudness(data, loudness, TARGET_LUFS)

  peak = np.abs(data).max()
  if peak > 1.0:
    data /= peak

  if rate != TARGET_RATE:
    data = resampy.resample(data, rate, TARGET_RATE)

  sf.write(input_file, np.clip(data, -1.0, 1.0).astype(np.float32), TARGET_RATE, subtype='PCM_16')

def backup_file(path):
  backup = f"{os.path.splitext(path)[0]}_original{os.path.splitext(path)[1]}"
  if not os.path.exists(backup):
    shutil.copy2(path, backup)

def process_file(path):
  backup_file(path)
  loudness_normalize(path)
  print(f"Normalized {path} to {TARGET_LUFS} LUFS.")

def main():
  root = Tk()
  root.withdraw()

  paths = filedialog.askopenfilenames(title="Select Audio Files", filetypes=[("Audio Files", "*.aac *.flac *.m4a *.mp3 *.ogg *.wav")])
  for path in paths:
    process_file(path)

if __name__ == "__main__":
  main()
