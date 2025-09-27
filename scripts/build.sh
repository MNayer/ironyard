#!/bin/bash

# Base packages
sudo apt-get update
sudo apt-get install -y \
  python3 \
  python3-pip \
  python3-venv

python3 -m venv --system-site-packages env
source env/bin/activate

# Install python requirements
python3 -m pip install -r requirements.txt

# Install browsers for scraping
playwright install
