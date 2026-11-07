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

## Additional Decisions — mbidlal

**To be completed by mbidlal:** Explain the actual reasoning behind maze rendering, Pac-Man movement, and any other choices they made. Avoid adding decisions that were not actually discussed or implemented.
