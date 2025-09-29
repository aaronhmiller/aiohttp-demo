#!/bin/bash
source venv/bin/activate
pip uninstall -y -r <(pip freeze)
pip cache purge
mv venv/pip.conf venv/pip.conf.bak
pip install -r requirements.txt
python app.py
