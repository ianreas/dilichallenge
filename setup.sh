#!/bin/bash

#Install required packages
pip3 install -r requirements.txt

#Download the spaCy model
python3 -m spacy download en_core_web_sm

#Run
python3 script.py