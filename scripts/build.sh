#!/bin/bash

python3 -m venv env
source env/bin/activate

# Install python requirements
python3 -m pip install -r requirements.txt

# Install browsers for scraping
playwright install
