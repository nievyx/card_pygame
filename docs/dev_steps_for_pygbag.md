# 1 - Add a main.py to root
```python
from src.main import main

main()
```

# 2 - If your .venv is inside the project folder:

card_pygame/.venv/

rename it temporarily:
```commandline
mv .venv ../card_pygame_venv
```

Then run:
```
python -m pygbag .
```

# 3 - Disable Sound
```
python -m pygbag . --disable-sound-format-error
```
That lets you continue testing the browser build without fixing sound yet.

(Better long-term fix

Convert your .mp3(or .wav in this case) sound file to .ogg.)

Later, you can convert the whole SFX folder with ffmpeg:

find src/assets/sfx -type f \( -name "*.wav" -o -name "*.mp3" -o -name "*.MP3" \) -print

Then convert them one by one to .ogg, or bulk-convert. After that, update your Python references to point to .ogg.

## If it was successful
```commandline
packing 196 files complete

    caching template https://pygame-web.github.io/cdn/0.9.3/default.tmpl
    cached locally at D:\dev\repos\uni\card_pygame\build\web-cache\27613e24ba16d44f2a5c88150c6d64e5.tmpl
    result files will be in D:\dev\repos\uni\card_pygame\build\web

urllib.request.urlretrieve("https://pygame-web.github.io/cdn/0.9.3/default.tmpl", "D:\dev\repos\uni\card_pygame\build\web-cache\27613e24ba16d44f2a5c88150c6d64e5.tmpl")
urllib.request.urlretrieve("https://pygame-web.github.io/cdn/0.9.3/favicon.png", "D:\dev\repos\uni\card_pygame\build\web-cache\29a2a48092f8c1a6595a20019f830691.png")

        caching icon https://pygame-web.github.io/cdn/0.9.3/favicon.png
        cached locally at D:\dev\repos\uni\card_pygame\build\web-cache\29a2a48092f8c1a6595a20019f830691.png

WARNING: wasm mimetype unsupported on that system, trying to correct
Not using SSL
Serving HTTP on 127.0.0.1 port 8000 (http://localhost:8000/) ...

```
> NOTE : In future move images/sound files out of src/assets
> & fix files to share one asset path

```
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
ASSET_DIR = BASE_DIR / "assets"
```
# 4 - Fix loading hang

For browser, it needs to pause each frame with:
```
await asyncio.sleep(0)
```
Edit src/game/game_controller.py

At the top, add:
```python
import asyncio
```
Then replace your start() method with this:
```python
def start(self) -> None:
    while self.running:
        self.handle_events()
        self.update()
        self.draw()
        pygame.display.flip()
    pygame.quit()


async def start_async(self) -> None:
    while self.running:
        self.handle_events()
        self.update()
        self.draw()
        pygame.display.flip()

        await asyncio.sleep(0)

    pygame.quit()
```
So you keep the original desktop version, and add a browser version.


# 5 - Make game not full screen 

Because browser fullscreen can behave weirdly inside pygbag.
Use your configured width/height first, 
then worry about fullscreen later.

In game_controller.py, currently have:
(should be in config for cleaner code)
```python
fullscreen = 1
```
For browser testing,  change that to:
```python

fullscreen = 0
```


# 6 - Stop the server with Ctrl + C, then delete the build folder:

rm -rf build

Then upgrade pygbag:
```python
python -m pip install --upgrade pygbag
```
Then rerun:
```python
python -m pygbag --disable-sound-format-error .
```
Open dev pygbag:
```
http://localhost:8000/?-i
```
If it still says BrowserFS not found

Try installing/running pygbag inside your project virtual environment instead of your global Python 3.14 install.

# 7 - add annotations to remove pygame surface type hint block
```python
from __future__ import annotations
```
run
```commandline
grep -R "pygame.Surface" src
```
fix card_renderer.py
```python
from __future__ import annotations  # Keeps pygame.Surface type hints from being evaluated in pygbag.
```

# 8 - Add a PEP 723 dependency block to your root main.py

app does not explicitly tell pygbag that it needs pygame-ce

```python
"""
Created for pygbag. This file is not required for the normal desktop game.
"""

# /// script
# dependencies = [
#   "pygame-ce",
# ]
# ///

import asyncio
from src.main import main_async

asyncio.run(main_async())
```
# 9 - Change src/main.py to this:
```python
from src.utils.config import Config
from src.game.game_controller import Game


def create_game():
    Config.load_game_data()
    return Game(config=Config())


def main():
    game = create_game()
    game.start()


async def main_async():
    game = create_game()
    await game.start_async()


if __name__ == '__main__':
    main()
```
The key fix is:
```python
return Game(config=Config())
```
not:
```python
return Game(config=Config)
```
Then rerun:
```python
python -m pygbag --disable-sound-format-error .
```
Open:
```
http://localhost:8000/?-i
```

# 10 - Quick test fix

Find wherever you hide the mouse cursor. Search:
```
grep -R "set_visible" src
```
You’ll probably find something like:
```
pygame.mouse.set_visible(False)
```
For the browser version, comment it out:

# pygame.mouse.set_visible(False)

or change it to:
```
pygame.mouse.set_visible(True)
```
Then rerun pygbag.

Why this is happening

On desktop, your game likely does this:

hide normal cursor
draw custom cursor at mouse position

But in browser, the real mouse position may not be syncing the same way, so your custom cursor gets stuck in the middle.

Better long-term fix

In your custom cursor file, probably:
```
src/ui/cursor.py
```
make browser mode skip the custom cursor.

Something like:
```
import sys

IS_BROWSER = sys.platform == "emscripten"
```
Then:
```
if not IS_BROWSER:
    pygame.mouse.set_visible(False)
```
And when drawing:
```
if IS_BROWSER:
    return
For now
```
Do the quick version first:
```
grep -R "set_visible" src
```
Change False to True or comment it out.

Then rerun:

python -m pygbag --disable-sound-format-error .

# 11 - import sys # For Pygbag version
import pygame
from src.ui import THEME

IS_BROWSER = sys.platform == 'emscripten' # Check for Browser for Pygbag Version

class Cursor:
    def __init__(self):
        debug = 0
        if not debug and not IS_BROWSER:
            pygame.mouse.set_visible(False)
        self.size = (32,32)

# 12 - self.clock = pygame.time.Clock()

That object just helps you cap FPS with:

self.clock.tick(60)

So your Game.__init__() should have:

pygame.init()
self.clock = pygame.time.Clock()

Then both loops can use it:

# desktop
self.clock.tick(60)
# browser
self.clock.tick(60)
await asyncio.sleep(0)

# 13 - Remove custom cursor
Desktop: draw your custom cursor
Browser: use the normal cursor

```python
 # New check for if game running in browser before drawing custom cursor.
        import sys
        IS_BROWSER = sys.platform == 'emscripten'

        if not IS_BROWSER:
            self.cursor.draw(self.screen)
```
# 14 - asset filename issue.

The crash is:

FileNotFoundError:
src/assets/monsters/Calm.png

But earlier your packaged file list showed:

src/assets/monsters/calm.png

Lowercase c.

On Windows desktop, this often works because Windows file paths are usually case-insensitive. In the browser/Linux-like pygbag filesystem, paths are case-sensitive.

So:

Calm.png

and:
```
calm.png
```
are different files.

Fix this specific one

Search where Calm.png is referenced:
```
grep -R "Calm.png" src
```
Then change it to:
```
calm.png
```
Or rename the actual file to match the code:
```
mv "src/assets/monsters/calm.png" "src/assets/monsters/Calm.png"
```


# 15 -

# 16 -


