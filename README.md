# French Number Listening Practice

A tool for generating French number listening practice materials.

## Features
- Generates random numbers and sentences in French
- Converts text to speech
- Creates practice audio file with appropriate spacing
- Automatically generates answer sheets
- Provides blank sheets for practice

## Requirements

### Python Dependencies
- num2words
- pydub
- edge-tts

### System Requirements
- Python 3.x
- ffmpeg (for audio processing)

### Installation

1. Install Python dependencies:
pip install num2words pydub edge-tts

2. Install system dependencies:
On macOS (using Homebrew):
brew install ffmpeg

### Quick Install (Alternative)
Clone the repository and install all dependencies:
git clone https://github.com/Loria618/NumberPractice-fr.git
cd NumberPractice-fr
pip install -r requirements.txt

## File Structure
1. `french-dictation.py`: Main Python script for content generation
   - Generates `french_numbers_dictation.mp3` in the same directory
   - Note: The audio file will be overwritten with each execution
2. `french-dictation.sh`: Shell script for execution and file management
   - Creates two text files in the same directory:
     - `[system_date]_numbers_dictation.txt`
     - `[system_date]_numbers_log.txt`
   - Files are named with the current system date
3. `french-practice.command`: Shortcut for easy access

Note: Please place files 1 and 2 in the same directory. File 3 can be placed on the desktop for convenient access.

## Usage
1. Double click the .command file
2. The script will generate:
   - An MP3 file with French numbers/sentences
   - An answer sheet (txt file)
   - A blank practice sheet (txt file)
3. Files will automatically open for practice

## Troubleshooting

### Audio Issues
If you encounter audio processing issues:
1. Ensure ffmpeg is properly installed
2. Check system audio settings
3. Verify file permissions

### Package Installation Issues
If you face problems installing dependencies:
1. Upgrade pip: `pip install --upgrade pip`
2. Install packages individually if batch installation fails
3. Check Python version compatibility
