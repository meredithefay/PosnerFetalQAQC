"""Select directory using filedialog, select relevant files

Written by Meredith Fay, PhD for Posner lab
Duke University
Last updated 2023-12-21

"""

# Automatically install relevant libraries
import subprocess
import sys
import tkinter as tk
import os

packages = []

def install(packages):
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Select directory
dir = tk.filedialog.askdirectory()  # Raises window to interactively select a file
os.chdir(dir)