#!/bin/bash
source venv/bin/activate
pip uninstall -y -r <(pip freeze)
pip cache purge
mv venv/pip.conf venv/pip.conf.bak
pip install -r requirements.txt
echo "curl --path-as-is http://127.0.0.1:8080/static/../private/secrets.txt"
python app.py
