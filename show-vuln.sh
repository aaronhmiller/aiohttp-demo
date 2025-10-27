#!/bin/bash
sudo systemctl start systemd-resolved
source venv/bin/activate
pip uninstall -y -r <(pip freeze)
pip cache purge
mv venv/pip.conf venv/pip.conf.bak
pip install -r requirements.txt
python app.py
grype venv --name venv --sort-by severity | grep -E "^NAME|aiohttp"
