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
├── assests/                 # audios and images and videos
└── src/
    ├── __init__.py
    ├── pac-man.py              # Execution entry point
    ├── config_parser.py     # Reads/parses JSON config and ignores comments (#)
    ├── highscore.py         # System to save the top 10 scores
    ├── 
    ├── engine/
    │   ├── game_engine.py   # Main game loop
    |   ├── load_gifs.py     # convert gifs to frames
    |   ├── main_menu.py     # Screen navigation (Menu, Game, Pause, GameOver)
    │   └── splash_screen.py # draw splash screen  
    ├── models/
    │   ├── ghost.py         # Ghost object and AI logic
    │   ├── maze.py          # Maze grid, walls, and Pacgums
    │   ├── move_pacman.py   # Manage Pac-Man animations and movement inside the maze
    │   └── screen_maze.py    # Display the pause menu and Ask the player for their name and Run one game level and manage Pac-Man, ghost.
    │
    └── helper_func/
        ├── draw_line.py      # Draw a line between two points on a surface.
        ├── draw_pixel.py     # Draw one pixel on a surface.
        └── draw_rect.py      # Draw a filled rectangle on a surface.
```

## Description of Key Directories & Files

- **`config.json`**: Central setup file for game settings.
- **`Makefile`**: Automation scripts for common development tasks (`install`, `run`, `debug`, `clean`, `lint`).
- **`project_management/`**: Folder dedicated to planning artifacts (Gantt charts, risk matrices, etc.).
- **`src/`**: Source code container:
  - **`engine/`**: Handles the game loop and state management transitions.
  - **`models/`**: Defines business logic, game entities (Pacman, Ghosts, Maze), and game state.
  - **`views/`**: Handles UI rendering and graphics interface.





**Parsing:**
parser has 4 main stages:
-  config.json
1. Extract / clean the file
2. Convert JSON text → Python data
3. Validate + repair invalid configuration
4. Return a clean validated configuration

```
          config.json
                │
                ▼
          extract_data()
                │
                ▼
          remove comments
                │
                ▼
           json.loads()
                │
                ▼
            read_data()
                │
                ▼
        ┌────────────────┐
        │  parse_data()  │
        └────────────────┘
                │
   ┌────────────┼────────────────┐
   ▼            ▼                ▼
level list    < 10 levels    bad level
  check       → add          → replace
    │            │                 │
    └────────────┼─────────────────┘
                 ▼
            check_levels()
                 │
                 ▼
           Validate(**data)
            
        Validate model checks:
              highscore_filename: The name of the high-score file.
              lives: The number of lives for the player.
              pacgum: The number of pac-gums in the game.
              points_per_pacgum: The points given for one pac-gum.
              points_per_super_pacgum: The points given for one super pac-gum.
              points_per_ghost: The points given for one ghost.
              seed: The seed used to create random values.
              level_max_time: The maximum time allowed for one level.
              level: The list of game levels. It must contain at least 10 levels.
                 │
        ┌────────┴──────────┐
        ▼                   ▼
      valid               invalid
        │                    │
        ▼                    ▼
  model_dump()          use default 
                 │
                 ▼
          clean configuration

```
