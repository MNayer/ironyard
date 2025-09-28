#!/bin/bash

user_name=${USER}
working_directory=$(pwd)
exec_path=${working_directory}/scripts/ironyard.sh
service_path=/etc/systemd/system/ironyard.service

echo "[*] Setup systemd service at '${service_path}'."

echo "[+] Password required to create service."
jinja2 \
  -D user_name=${user_name} \
  -D working_directory=${working_directory} \
  -D exec_path=${exec_path} \
  templates/ironyard.service | sudo tee ${service_path}

sudo systemctl enable --now ironyard.service
