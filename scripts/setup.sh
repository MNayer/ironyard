#!/bin/bash

set -e

if cat /proc/cpuinfo | grep -i raspberry &> /dev/null; then
  echo "[*] Run Raspberry Pi setup."

  # Base packages
  sudo apt-get update
  sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv

  # Make sure SPI is enabled
  echo "[+] Password required to enable SPI in config."
  config_path=/boot/firmware/config.txt
  cat ${config_path} | sed 's/.*dtparam=spi=.*/dtparam=spi=on/' | tee ${config_path}
fi

python3 -m venv --system-site-packages env
source env/bin/activate

# Install python requirements
python3 -m pip install -r requirements.txt

# Install browsers for scraping
playwright install

echo "[*] Setup complete!"
