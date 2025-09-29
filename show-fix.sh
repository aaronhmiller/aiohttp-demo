#!/bin/bash
source venv/bin/activate
pip uninstall -y -r <(pip freeze)
pip cache purge
mv venv/pip.conf.bak venv/pip.conf
pip install -r requirements.txt
python app.py
grype venv --name venv
