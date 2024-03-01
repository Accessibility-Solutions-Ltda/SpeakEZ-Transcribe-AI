@echo off
python -m venv .venv
.venv\Scripts\activate
python -m ensurepip --upgrade
python -m pip install --upgrade pip
python -m pip install pyqt6
pause