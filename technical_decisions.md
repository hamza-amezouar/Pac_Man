# Technical Decisions

## 1. Choosing Pygame Instead of MLX

### Context

The project subject allows MLX or a similar graphical library, provided that the graphical operations used have equivalents in MLX. We considered MLX and **Pygame** and chose Pygame because we found its Python-oriented workflow, event handling, window management, learning resources, and debugging experience more convenient for our game.

### Respecting the Graphics Constraint

We were aware that choosing Pygame did **not** mean we could freely use every Pygame feature. In particular, instead of relying on Pygame's built-in rectangle drawing function, we implemented basic drawing helpers:

- `src/helper_func/draw_pixel.py`
- `src/helper_func/draw_line.py`
- `src/helper_func/draw_rect.py`

These helpers made us work directly with basic graphical primitives. **Important:** implementing a custom rectangle helper alone does not prove that every graphical operation in the full project satisfies the subject's MLX-equivalence rule; all used operations still need to be reviewed before evaluation.

### Outcome

Pygame provided a development environment we preferred while encouraging us to think carefully about the permitted rendering operations.

## 2. Modular Software Architecture

We separated responsibilities across the game engine, menus and instructions, maze and character models, configuration, highscores, and drawing helpers. This allowed the two teammates to implement different parts of the game in parallel and integrate them through Git.

Relevant paths include `src/engine/`, `src/models/`, `src/helper_func/`, `src/config_parser.py`, and `src/highscore.py`.

## 3. Smooth Ghost Movement with Linear Interpolation

**Problem:** Directly advancing ghosts between maze cells looked like teleportation.

**Decision:** Keep navigation based on maze cells, but interpolate the on-screen position between the centers of two cells. With `t` representing progress between 0 and 1:

```text
start_pixel_x = maze_start_x + current_x * cell_size + cell_size / 2
start_pixel_y = maze_start_y + current_y * cell_size + cell_size / 2

t = current_step / total_steps
pixel_x = start_pixel_x + (goal_pixel_x - start_pixel_x) * t
pixel_y = start_pixel_y + (goal_pixel_y - start_pixel_y) * t
```

**Why:** This separates the logical movement on the grid from the smooth visual movement on the screen.

**Relevant code:** `src/models/ghosts.py` (`chase`).

## 4. Dynamic Scared-Mode Escape Targets

**Problem:** Scared ghosts needed to flee Pac-Man instead of continuing their usual behavior.

**Decision:** Use Pac-Man's position to select an escape destination in an opposing region of the maze. For example, if Pac-Man is in the upper-right region, ghosts can head toward the lower-left region. Randomized destinations help avoid one fixed escape path.

**Why:** This provides a dynamic response to the player's location.

**Relevant code:** `src/models/ghosts.py` (`create_random_path`).

## 5. Git Branches for Parallel Development

Each member worked on their own branch and merged changes into `main`. This enabled parallel work but also exposed us to merge conflicts. We learned how to inspect and resolve conflicts rather than abandoning either person's changes.

## 6. Using Pydantic for Configuration Validation

**Problem:** Parsing and validating configuration data with repeated `if/else` statements made the code lengthy and difficult to maintain.

**Decision:** Use **Pydantic** models to describe the configuration structure and enforce validation rules. The `Level` and `Validate` models use typed fields and constraints, while a model validator checks that the number of Pac-Gums fits within a level.

**Why:** Centralizing validation rules reduces repetitive conditional checks and makes invalid configuration values easier to detect and handle.

**Relevant code:** `src/config_parser.py` (`Level`, `Validate`, and `Parse`).

## 7. Using Bitwise Operations to Decode Maze Walls

**Problem:** The maze generator represents each cell's walls as a number, while maze rendering needs to know whether a wall exists in each of the four directions.

**Decision:** Decode the numerical wall representation using **bitwise AND (`&`)** and direction masks: North = 1, East = 2, South = 4, and West = 8. Convert each result to a Boolean value.

```python
directions = {"N": 1, "E": 2, "S": 4, "W": 8}
for direction, value in directions.items():
    cell_direction[direction] = bool(cell & value)
```

**Why:** A single numerical value can encode several walls. Bitwise checks extract each direction efficiently and produce the `True`/`False` values used by the drawing logic.

**Relevant code:** `src/models/maze.py` (`get_walls()` and `draw_maze()`).

## 8. Smooth Pac-Man Movement Using Incremental Pixel Updates

**Problem:** Moving Pac-Man directly from one maze cell to the next would make its motion appear abrupt.

**Decision:** Keep movement constrained by the maze grid, but move Pac-Man toward the next valid cell in **small pixel increments**. First, `target_pacman()` checks the walls and identifies an allowed destination. Then, `move_pacman()` updates the current pixel position by a specified speed, using `min()` and `max()` to avoid overshooting the target.

**Why:** This keeps collision and navigation decisions cell-based while making the visible movement gradual. Unlike ghost movement, Pac-Man's implementation uses incremental position updates rather than an interpolation-progress fraction.

**Relevant code:** `src/models/move_pacman.py` (`target_pacman()` and `move_pacman()`).
