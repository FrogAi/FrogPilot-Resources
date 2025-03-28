import os
import subprocess
import tkinter as tk

from tkinter import filedialog

def run(cmd, cwd=None):
  return subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True).stdout.strip()

def browse_files():
  root = tk.Tk()
  root.withdraw()
  file_paths = filedialog.askopenfilenames(title="Select files to fix permissions")
  return file_paths

def set_executable_permission(repo_path):
  file_paths = browse_files()

  if not file_paths:
    print("No files selected. Exiting.")
    return

  branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo_path)

  for file_path in file_paths:
    relative_file_path = os.path.relpath(file_path, repo_path)
    print(f"Setting executable permission for: {relative_file_path}")
    run(["git", "update-index", "--chmod=+x", relative_file_path], cwd=repo_path)
    run(["git", "add", relative_file_path], cwd=repo_path)
    run(["git", "commit", "-m", f"Set executable permission for {os.path.basename(file_path)}"], cwd=repo_path)

  run(["git", "push", "origin", branch], cwd=repo_path)
  print("Permission changes committed and pushed successfully.")

if __name__ == "__main__":
  repo_path = r"C:\Users\Owner\Documents\GitHub\FrogPilot"
  set_executable_permission(repo_path)
