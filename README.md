# card_pygame
> note: Readme might not reflect games current state
## Install
```
pip install -r requirements.txt
```
## Run
```
python main.py
```
## Pygame image errors
> NOTE: To fix 'libpng warning: iCCP: known incorrect sRGB profile'
> 
Windows: Open image in Paint3D and resave

Or to temp fix
```
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
```

or create a 
```python
from PIL import Image
import os

folder = "your_image_folder"

for filename in os.listdir(folder):
    if filename.endswith(".png"):
        path = os.path.join(folder, filename)
        img = Image.open(path)
        img.save(path)
```

## Controls
- Click "Start" to deal cards
- Click 'How To Play' for non-existent instructions
  - Click "Back" to return to menu


> Image from pre v0.0.2
![Capture](././demo.PNG)

> Image from pre v0.0.2
![Capture](././menu_demo.PNG)
---

## 🧪 My Implementation Notes 
<details open>

### Buttons
- Created in main.py
- Drawn only in menu state
- Use isOver() for clicks

### State System
- current_state = "menu"
- switches on button click

[//]: # (### Problems I hit)

[//]: # (- &#40;write bugs here&#41;)

[//]: # (- &#40;what fixed them&#41;)

### Improvements for later
- Better UI layout
- Animations
- Sound
- .exe via:
```
pyinstaller --onefile --windowed main.py
```
</details>

## Folder Structure 

```
project/
│
├── src/          ← code 
├── cards/        ← assets
├── script/       ← dev scripts (relocatable run.bat etc)
│
│
├── README.md
├── requirements.txt
├── run.bat       <- Windows script to run game (root-based script)
├── run.sh       <- Linux script to run game (root-based script) (untested)
```

``` 
    src/
    │
    ├── main.py
    │
    ├── ui/
    │   ├── button.py
    │
    ├── game/
    │   ├── state.py
    │   ├── logic.py
    │
```

``` 
    scripts/
    │
    ├── run.bat
    │
    ├── run.sh (untested)
```