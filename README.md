# Pacman Project Architecture

Below is the directory tree and description for the Pacman project:

```text
pacman_project/
├── config.json              # Configuration file
├── Makefile                 # Contains commands (install, run, debug, clean, lint)
├── pyproject.toml / requirements.txt
├── README.md                # In English as required
├── .gitignore
├── project_management/      # Documentation & project management folder (Gantt, Risk Analysis...)
└── src/
    ├── __init__.py
    ├── main.py              # Execution entry point
    ├── config_parser.py     # Reads/parses JSON config and ignores comments (#)
    ├── highscore.py         # System to save the top 10 scores
    ├── maze_adapter.py      # Adapter for the external A-Maze-ing library
    ├── engine/
    │   ├── game_engine.py   # Main game loop
    │   └── state_manager.py # Screen navigation (Menu, Game, Pause, GameOver)
    ├── models/
    │   ├── entity.py        # Base Entity class
    │   ├── pacman.py        # Player object
    │   ├── ghost.py         # Ghost object and AI logic
    │   ├── maze.py          # Maze grid, walls, and Pacgums
    │   └── game_state.py    # Score, lives, timer, and Cheat Mode
    └── views/
        ├── renderer.py      # Renders graphical elements using the graphics library
        └── ui.py            # User interface (Main Menu, HUD, Game Over screen)
```

## Description of Key Directories & Files

- **`config.json`**: Central setup file for game settings.
- **`Makefile`**: Automation scripts for common development tasks (`install`, `run`, `debug`, `clean`, `lint`).
- **`project_management/`**: Folder dedicated to planning artifacts (Gantt charts, risk matrices, etc.).
- **`src/`**: Source code container:
  - **`engine/`**: Handles the game loop and state management transitions.
  - **`models/`**: Defines business logic, game entities (Pacman, Ghosts, Maze), and game state.
  - **`views/`**: Handles UI rendering and graphics interface.





  parcing :

               config.json
                  │
                  ▼
          Read JSON dictionary
                  │
                  ▼
        Validate each setting
           using Pydantic
                  │
        ┌─────────┴─────────┐
        │                   │
      valid               invalid
        │                   │
        ▼                   ▼
   use given value     warning + default
        │                   │
        └─────────┬─────────┘
                  ▼
          Final configuration