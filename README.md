# card_pygame

![Capture](./././assets/demo.PNG)

## Requirements / dependencies

To run project, the follow  is required: 
- Python 3.13 recommend
- Pygame

Install dependencies with:
```bash
pip install -r requirements.txt
```

## How to Run
Game must be ran from project root directory:

### Windows

Run:

```bash
run.bat
```

or manually:
```bash
pip install -r requirements.txt
python -m src.main
```

## How to Play

Wave Mode
- Player starts with 5 cards, dealt at random, including chances to get rare cards.
- Enemy starts with 3 cards.
- Select one of your cards from the bottom to attack
- use either:
    - Either regular attack with by then click an enemy attack 
    - or select a spell before attacking to deal magic damage
- AI enemy will then take its turn.
- Winner eliminates all opposing players cards.
- Winning rounds will reward an additional card and increase the wave count.

## Controls
- Mouse click: select cards / buttons
- Start button: Starts the game
- How to playL opens instructions
- Back button: returns to menu

## Code Structure

<details open>
<summary>Click to collapse</summary>

```text
src/
├── main.py
│
├── game/
│   ├── game_controller.py
│   ├── game_state.py
│   ├── monster.py
│   ├── player.py
│   ├── spell.py
│   └── battle/
│       └── system.py
│
├── ui/
│   ├── components/
│   │   ├── battle_log.py
│   │   ├── card_view.py
│   │   └── spell_menu.py
│   ├── screens/
│   │   ├── battle_screen.py
│   │   ├── how_to_screen.py
│   │   └── menu_screen.py
│   └── theme/
│       ├── button.py
│       ├── cursor.py
│       ├── panel.py
│       └── theme.py
│
├── sound/
│   ├── music.py
│   └── sfx.py
│
└── utils/
    └── config.py
```
</details>

## File Purposes

| File | Purpose                                                                                                  |
|---|----------------------------------------------------------------------------------------------------------|
| `src/main.py` | Entry point. Loads config, creates the game object, and starts the game.                                 |
| `src/game/game_controller.py` | Main game controller. Handles screen switching and the overall game loop.                                |
| `src/ui/screens/battle_screen.py` | Main battle screen. Handles player clicks, drawing the battle UI, spell menu, and battle result display. |
| `src/game/battle/system.py` | Core battle rules. Handles turns, attacks, spell use, round resolution, and battle winner logic.         |
| `src/game/monster.py` | Defines the card/monster objects used in battle.                                                         |
| `src/game/spell.py` | Defines spell behaviour such as damage and healing.                                                      |
| `src/utils/config.py` | Loads game data, assets, players, enemies, cards, and backgrounds.                                       |


