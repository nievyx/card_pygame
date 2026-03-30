#!/bin/bash

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m src.main