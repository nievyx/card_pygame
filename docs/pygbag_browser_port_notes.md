# Pygbag Browser Port Notes — Niamh's Monster Cards

## Current status

The Pygame game now runs in the browser with pygbag.

It currently reaches the menu, starts gameplay, and plays for at least a couple of rounds. It is not fully production-ready yet, but the main browser port works.

Current branch:

```bash
web-pygbag
```

Run command:

```bash
python -m pygbag --disable-sound-format-error .
```

Debug URL:

```text
http://localhost:8000/?-i
```

Normal URL:

```text
http://localhost:8000/
```

---

## Important changes made

### 1. Added root `main.py`

Pygbag requires a root-level `main.py`, even though the real game entry point is `src/main.py`.

Root `main.py` should look like this:

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

The PEP 723 dependency block is important because it tells pygbag to load `pygame-ce`.

---

### 2. Updated `src/main.py`

Make sure this line uses `Config()` with brackets:

```python
return Game(config=Config())
```

Correct version:

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
    """
    Main entry point for Pygbag async game.
    Browser version.
    """
    game = create_game()
    await game.start_async()


if __name__ == '__main__':
    main()
```

The bug was:

```python
return Game(config=Config)
```

That passed the class instead of an instance and caused:

```text
Config.create_players() missing 1 required positional argument: 'self'
```

---

### 3. Added async browser loop

In `src/game/game_controller.py`, add a browser version of the game loop:

```python
async def start_async(self):
    """Pygbag version: play Pygame in browser."""
    import asyncio

    while self.running:
        self.handle_events()
        self.update()
        self.draw()
        pygame.display.flip()

        self.clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()
```

Also make sure `Game.__init__()` creates a clock:

```python
self.clock = pygame.time.Clock()
```

This does **not** need an `IS_BROWSER` check.

---

### 4. Cursor browser fix

The custom cursor causes problems in browser.

Where needed:

```python
import sys

IS_BROWSER = sys.platform == "emscripten"
```

In the cursor class:

```python
if not debug and not IS_BROWSER:
    pygame.mouse.set_visible(False)
```

In `Game.draw()`, skip drawing the custom cursor in browser:

```python
if not IS_BROWSER:
    self.cursor.draw(self.screen)
```

This lets the browser/Pygame normal cursor work instead of the custom cursor getting stuck.

---

### 5. Type hint compatibility fix

Pygbag crashed on:

```text
AttributeError: module 'pygame' has no attribute 'Surface'
```

Fix: add this to files with `pygame.Surface` used in type hints:

```python
from __future__ import annotations
```

Known files:

```text
src/assets/image_cache.py
src/ui/cards/card_renderer.py
```

Only needed for type hints like:

```python
def get_card_frame(self, monster) -> pygame.Surface:
    ...
```

Not needed for actual surface creation like:

```python
pygame.Surface(...)
```

---

## Current known issues

### 1. Audio disabled for now

You are running pygbag with:

```bash
--disable-sound-format-error
```

because the project currently contains `.wav`, `.mp3`, and `.MP3` audio files.

Later, convert audio to `.ogg`.

Example future command, once `ffmpeg` is installed:

```bash
python scripts/convert_audio_to_ogg.py
```

The previous script failed because `ffmpeg` was not installed or not available on PATH.

For now, keep using:

```bash
python -m pygbag --disable-sound-format-error .
```

---

### 2. Browser filesystem is case-sensitive

Windows lets this work:

```text
Calm.png
calm.png
```

Pygbag/browser does **not**.

You fixed at least one issue where code expected:

```text
Calm.png
```

but the actual file was:

```text
calm.png
```

Future crashes may look like:

```text
FileNotFoundError: No such file or directory: '/data/data/card_pygame/assets/src/assets/monsters/SomeName.png'
```

Fix by making the filename and code reference match exactly.

Likely suspects:

```text
calm.png / Calm.png
chimera.png / Chimera.png
octopot.png / Octopot.png
evilGod.png / EvilGod.png
plant.png / Plant.png
```

Search for a reference:

```bash
grep -R "SomeName.png" src
```

To rename case-only files on Windows, use a temporary name:

```bash
mv "src/assets/monsters/calm.png" "src/assets/monsters/calm_tmp.png"
mv "src/assets/monsters/calm_tmp.png" "src/assets/monsters/Calm.png"
```

---

### 3. Crashes on round 3

The game worked but crashed around round 3.

Most likely causes:

```text
missing or mis-cased monster image
missing or mis-cased face image
sound file issue
specific wave/card/monster only appearing later
```

Next time, run with:

```text
http://localhost:8000/?-i
```

Play until crash, then copy the traceback.

---

### 4. Font warnings are not urgent

You saw warnings like:

```text
system font 'consolas' couldn't be found
Using the default font instead
```

This is not currently blocking the game.

Later, fix by bundling a `.ttf` font and loading it directly instead of relying on system fonts.

---

### 5. Build output should probably be ignored

Add to `.gitignore`:

```gitignore
build/
.venv/
__pycache__/
*.pyc
```

Do not commit `build/` unless intentionally storing generated web output.

---

## Suggested next session plan

1. Start server:

```bash
python -m pygbag --disable-sound-format-error .
```

2. Open debug mode:

```text
http://localhost:8000/?-i
```

3. Play until the round 3 crash.

4. Copy the traceback.

5. Fix the exact missing file or error.

6. Commit the working browser milestone:

```bash
git status
git add main.py src/main.py src/game/game_controller.py src/ui/cursor.py src/ui/cards/card_renderer.py src/assets/image_cache.py src/assets/monsters
git commit -m "Add working pygbag browser version"
```

---

## Milestone reached

You successfully got:

```text
Pygame desktop game
→ pygbag browser build
→ pygame-ce loading
→ menu rendering
→ gameplay running in browser
```

Next work is bug-fixing and polish, not setup.

ges is your website branch.