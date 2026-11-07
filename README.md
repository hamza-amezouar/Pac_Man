*This project has been created as part of the 42 curriculum by hamezoua, mbidlal.*

# Pac-Man — Ghosts! More Ghosts!

A Python recreation of the classic Pac-Man arcade game, developed for the 42 curriculum.

> **Play the packaged game:** [Pac-Man on itch.io](YOUR_ITCH_IO_GAME_URL) *(replace this placeholder with the published game URL).* 

## Description

This project recreates Pac-Man as a graphical, multi-level arcade game. The player navigates generated mazes, collects pacgums, avoids autonomous ghosts, and tries to earn a place on a persistent highscore leaderboard. The game combines a Pygame interface with an externally supplied A-Maze-ing maze generator, configurable rules, and a modular Python codebase.

The main learning goals are object-oriented design, integration with a third-party package, configuration validation, event-driven game logic, persistent data, and collaborative software development.

## Features

- Graphical main menu, instructions screen, game view, pause screen, and highscore display.
- Ten configured levels with adjustable maze dimensions and pacgum counts.
- Four-direction Pac-Man movement and autonomous ghost behavior.
- Normal pacgums, super-pacgums, lives, score tracking, and a per-level timer.
- Fixed-seed maze generation for the first level and generator-controlled subsequent levels.
- JSON-based top-ten highscore persistence.
- Configuration validation with documented fallback values.
- Evaluation-oriented level advancement shortcut (see **Controls**).

## Instructions

### Requirements

- Python **3.11 or 3.12** (`pyproject.toml` requires `>=3.11,<3.13`).
- [`uv`](https://docs.astral.sh/uv/) for dependency management.
- A graphical desktop environment capable of running Pygame.

The repository includes the assigned `mazegenerator-2.1.0-py3-none-any.whl` package, which `uv` installs as a local dependency. Other dependencies are declared in `pyproject.toml` and locked in `uv.lock`.

### Install and run

From the repository root:

```bash
make install
make run
```

`make install` runs `uv sync`; `make run` executes `uv run python3 pac-man.py config.json`.

To launch the game with a different configuration file:

```bash
uv run python3 pac-man.py path/to/custom-config.json
```

The entry point expects a JSON configuration filename as a command-line argument. Run commands from the repository root because asset paths are relative to it.

### Development commands

| Command | Purpose |
| --- | --- |
| `make install` | Synchronize dependencies with `uv` |
| `make run` | Launch the game with `config.json` |
| `make lint` | Run Flake8 and mypy checks |
| `make clean` | Remove Python and test/type-checking caches |
| `make debug` | Invoke the Python debugger (see note below) |

**Debug note:** The current `debug` Makefile rule invokes `uv run python3 -m pdb` without a script argument. To debug the actual game, use `uv run python3 -m pdb pac-man.py config.json` directly.

### Controls

| Input | Action |
| --- | --- |
| Arrow keys / W, A, S, D | Move Pac-Man |
| Space | Open the pause menu during gameplay |
| P | Advance the current level (evaluation shortcut) |
| Mouse | Select menu items and on-screen buttons |
| Enter | Submit the name on the highscore entry screen |
| Backspace | Remove the last character from the entered name |
| Q | Quit from supported screens |

The pause menu provides resume and navigation options. The `P` shortcut is included to make it easier to inspect level progression during evaluation; it should not be confused with the normal pause control.

## Configuration

The game reads a JSON file passed on the command line. The parser in `src/config_parser.py` ignores blank lines and lines beginning with `#`, then validates the data using Pydantic models. Extra/unknown keys are ignored by the model. The game configuration includes global parameters and a `level` array.

### Configuration fields

| Key | Purpose | Parser fallback | Shipped `config.json` |
| --- | --- | --- | --- |
| `highscore_filename` | JSON file used for leaderboard persistence | `highscore.json` | `highscore.json` |
| `lives` | Initial player lives | `3` | `2` (invalid; replaced by `3`) |
| `pacgum` | Global pacgum setting | `42` | `10` |
| `points_per_pacgum` | Score per normal pacgum | `10` | `10` |
| `points_per_super_pacgum` | Score per power pellet | `50` | `50` |
| `points_per_ghost` | Score for eating an eligible ghost | `200` | `14` |
| `seed` | First-level maze seed | `42` | `55` |
| `level_max_time` | Time limit per level, in seconds | `90` | `90` |
| `level` | Array of level configurations | Ten 15 × 15 levels, each with `pacgum: 42` | Ten configured levels |

Each entry in `level` has `width`, `height`, and `pacgum` fields. The Pydantic `Level` model restricts width and height to **15–30**, requires `pacgum > 4`, and rejects pacgum counts greater than `width * height - 19`. The main model requires **at least ten levels** and positive score, seed, and time settings. The current `lives` validation is `> 2`, so the shipped value of `2` is corrected to the fallback value `3`.

Example of a minimal level entry:

```json
{
  "width": 15,
  "height": 15,
  "pacgum": 42
}
```

The parser attempts to repair invalid fields and levels, append default levels when fewer than ten are supplied, and use fallback configuration when JSON decoding fails. A missing configuration argument or a missing/wrong-extension configuration file results in a clear command-line error. Not every possible malformed input is guaranteed to recover: the README describes the current implementation, not an unverified guarantee of crash-free handling.

## Highscore

Highscores are persisted in the JSON file specified by `highscore_filename` (by default, `highscore.json`). The `Engine` loads the file at startup; if it is missing or contains invalid JSON, it starts with an empty list and prints a warning.

When the player submits a name on the score-entry screen, the game appends a `{ "player name": score }` record, sorts the records by score in descending order, keeps the **top ten**, and writes the result back to the JSON file. The highscore screen displays ranks, names, scores, and profile images.

Example record format:

```json
[
  {"PLAYER1": 340},
  {"PLAYER2": 230}
]
```

**Why JSON?** It is human-readable, needs no database server, and is simple to load and update for a local top-ten leaderboard. The name-entry handler currently limits input to ten characters and accepts letters/digits plus spaces; further validation of existing score-file contents is not implemented at load time.

## Maze Generation

The project uses the **assigned external A-Maze-ing package** distributed as `mazegenerator-2.1.0-py3-none-any.whl`. The game does not implement its own maze-generation algorithm.

`src/models/maze.py` defines `Maze`, a subclass of `mazegenerator.mazegenerator.MazeGenerator`. It calls the package constructor with `size`, `perfect`, and `seed`; `perfect` defaults to `False` for the game's corridor layout. The first level uses the configured seed. For later levels, the wrapper sets the seed argument to `0` before calling the generator.

The wrapper's `get_walls()` method translates the generated cell bitmasks into directional wall flags (`N`, `E`, `S`, `W`). `Maze_screen` then uses those flags to draw walls, position game elements, and size the maze within the game window. This separates maze generation from rendering and gameplay interactions.

## Implementation

The program starts in `pac-man.py`, creates an `Engine` with a 1920 × 1080 display, and calls `run_engine()`. The engine loads validated configuration and highscores, initializes Pygame, and dispatches between the main menu, gameplay, instructions, and leaderboard screens.

Gameplay is coordinated in `src/models/screen_maze.py`: it prepares each level, creates the maze and game entities, processes Pygame events, updates movement and collision interactions, manages pauses and level transitions, and handles end-of-game score entry. `src/models/move_pacman.py` contains Pac-Man movement behavior; `src/models/ghosts.py` contains ghost-related behavior; `src/models/maze.py` adapts maze data and draws the maze. The UI uses GIF/image assets and local fonts under `assists/`.

Scores are accumulated during play using configuration-defined values. Highscore persistence is deliberately separated from the main menu drawing code, although the engine and gameplay flow coordinate loading, saving, and display.

## General Software Architecture

The project follows a modular, object-oriented organization with a central engine and separate gameplay, rendering, and configuration responsibilities.

```text
pac-man.py
    |
    v
Engine (src/engine/game_engine.py)
    |-- Parse / Pydantic validation (src/config_parser.py)
    |-- Main menu (src/engine/main_menu.py)
    |-- Instructions (src/engine/instruction.py)
    |-- Highscore display (src/highscore.py)
    `-- Gameplay orchestration (src/models/screen_maze.py)
            |-- Maze / Maze_screen (src/models/maze.py)
            |       `-- external A-Maze-ing MazeGenerator
            |-- Pac-Man movement (src/models/move_pacman.py)
            |-- Ghost behavior (src/models/ghosts.py)
            `-- Drawing helpers (src/helper_func/)
```

### Repository structure

```text
.
├── pac-man.py
├── config.json
├── highscore.json
├── Makefile
├── pyproject.toml
├── uv.lock
├── mazegenerator-2.1.0-py3-none-any.whl
├── assists/
│   ├── fonts/
│   └── images/
├── src/
│   ├── __init__.py
│   ├── config_parser.py
│   ├── highscore.py
│   ├── engine/
│   │   ├── game_engine.py
│   │   ├── instruction.py
│   │   ├── load_gifs.py
│   │   └── main_menu.py
│   ├── helper_func/
│   │   ├── draw_line.py
│   │   ├── draw_pixel.py
│   │   └── draw_rect.py
│   └── models/
│       ├── ghosts.py
│       ├── maze.py
│       ├── move_pacman.py
│       └── screen_maze.py
└── README.md
```

`project_management/` is planned as a separate documentation directory and should be added before submission.

## Project Management

This is a two-person 42 project developed by **hamezoua** and **mbidlal**. The work is organized around configuration and validation, maze integration, game mechanics, user interface, persistence, and integration/testing. The dedicated project-management documentation will contain the team's actual planning, task allocation, progress tracking, risks, and testing evidence.

**Project-management documents:** [View project management](./project_management/) *(directory and contents to be added before submission).* 

## Packaging and Distribution

The project includes `pyinstaller` as a declared dependency, but the supplied repository snapshot does not contain a verified packaging script or specification. Add the final packaging configuration to the repository root and update this section once the build has been tested.

**itch.io game page:** [Play Pac-Man](YOUR_ITCH_IO_GAME_URL) *(replace with the real page after publishing).* 

## Resources

### Documentation and references

- [Python documentation](https://docs.python.org/3/) — Python language and standard library.
- [Pygame documentation](https://www.pygame.org/docs/) — rendering, input events, sprites, and timing.
- [Pydantic documentation](https://docs.pydantic.dev/latest/) — typed configuration models and validation.
- [uv documentation](https://docs.astral.sh/uv/) — dependency installation and environment management.
- [Python `json` module](https://docs.python.org/3/library/json.html) — configuration and highscore serialization.
- [Python Packaging User Guide](https://packaging.python.org/) — Python package and distribution concepts.
- **Assigned A-Maze-ing package** — local `mazegenerator-2.1.0-py3-none-any.whl` supplied for the 42 assignment.
- **42 Pacman subject, version 1.5** — project requirements and evaluation criteria.

### AI usage disclosure

AI was used **only as an aid in thinking through the software architecture**, including how to organize modules and separate responsibilities. AI was **not used to write the project's source code**. The team remained responsible for implementing, reviewing, and understanding the code. AI also assisted in preparing this README documentation based on the supplied project files and the team's explanations.

---

**Authors:** `hamezoua` · `mbidlal`  
**Project:** 42 Pacman — *Ghosts! More ghosts!*
