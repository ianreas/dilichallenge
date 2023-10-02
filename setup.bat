@echo off

REM Create a virtual environment named "env"
python -m venv env

REM Activate the virtual environment
call env\Scripts\activate

REM Install required packages
pip install -r requirements.txt

REM Download the spaCy model
python -m spacy download en_core_web_sm

REM Run the main script
python script.py