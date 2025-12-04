#!/bin/bash

# Has to be run from main project directory
cd ./application
python3 -m venv ./venv
source venv/bin/activate
pip install PySide6
python3 application/app.py
