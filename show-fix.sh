#!/bin/bash
source venv/bin/activate
pip uninstall -y -r <(pip freeze)
pip cache purge
mv venv/pip.conf.bak venv/pip.conf
pip install --no-cache-dir -r requirements.txt
python app.py
grype venv --name venv --fail-on high
