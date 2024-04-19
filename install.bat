@echo off
python -m ensurepip --upgrade
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
start /b python src/main.py
pause