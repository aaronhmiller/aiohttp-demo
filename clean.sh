#!/bin/bash
source venv/bin/activate
pip uninstall -y -r <(pip freeze)
pip cache purge
