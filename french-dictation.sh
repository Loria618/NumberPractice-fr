#!/bin/bash

# Change to the directory containing the script
cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Run the Python script
python3 french-dictation.py

# Get current date in YYYYMMDD format
date=$(date +%Y%m%d)

# Create the text file name for dictation
textfile="${date}_numbers_dictation.txt"
logfile="${date}_numbers_log.txt"

# Create empty dictation file
touch "$textfile"

# Open the generated MP3 file
# open french_numbers_dictation.mp3

# Open the log file with TextEdit
open -a TextEdit "$logfile"

# Open the dictation file with TextEdit
open -a TextEdit "$textfile"

# Deactivate virtual environment
deactivate