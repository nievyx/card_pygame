"""
Created for pygbag.
This file is not required for the normal desktop game.
"""

# PEP 723 dependency block
# /// script
# dependencies = [
#   "pygame-ce",
# ]
# ///

import asyncio
from src.main import main_async

asyncio.run(main_async())