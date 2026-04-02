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
## Controls
- Click "Start" to deal cards
- Click "Back" to return to menu

> Image from v0.0.2
![Capture](././demo.PNG)

> Image from v0.0.1
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

### Problems I hit
- (write bugs here)
- (what fixed them)

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