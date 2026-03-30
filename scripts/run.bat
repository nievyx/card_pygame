@echo off

cd /d "%~dp0.."

if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate

python -m pip install -r requirements.txt

python -m src.main

pause