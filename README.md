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
