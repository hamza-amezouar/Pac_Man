# Challenges and Solutions

## hamezoua — Smooth Ghost Movement

**Challenge:** Pac-Man and the ghosts needed to move within the same running game. Initially, ghost positions jumped directly from one maze cell to another, making the movement appear abrupt.

**Investigation:** After searching for techniques to make grid-based movement smoother, hamezoua explored converting cell coordinates into pixel coordinates and interpolating between positions.

**Solution:** Use **linear interpolation** between the centers of adjacent maze cells. A movement-progress fraction determines the ghost's intermediate pixel position, while navigation remains cell-based.

**Relevant code:** `src/models/ghosts.py` — `chase()`.

## hamezoua — Dynamic Scared Mode

**Challenge:** Ghosts in scared mode needed to move away from Pac-Man dynamically rather than following their normal chase behavior.

**Solution:** Choose escape targets based on Pac-Man's region of the maze. When Pac-Man is in one region, ghosts can target an opposing region; for example, upper-right versus lower-left.

**Relevant code:** `src/models/ghosts.py` — `create_random_path()`.

## Both Members — Git Merge Conflicts

**Challenge:** We developed features on separate branches, but merging into `main` produced conflicts. Initially, we lacked the Git experience needed to resolve them confidently, which slowed integration.

**Investigation:** We spent time learning how Git branches and merges work, why conflicts happen, and how to review conflicting changes without losing work.

**Solution:** We applied what we learned to resolve the conflicts and continued integrating the project.

**Outcome:** We improved our practical understanding of collaborative development, version control, and the importance of communicating during integration.

## mbidlal — Challenges and Resolutions

## mbidlal — Simplifying Data Parsing with Pydantic

**Challenge:** Initially, data parsing was implemented using multiple `if/else` conditions. This made the code very long, repetitive, and difficult to maintain, since the same validation logic was repeated several times.

**Investigation:** After looking for a cleaner way to handle data parsing and validation, mbidlal discovered Pydantic, a Python library that simplifies data validation using models.

**Solution:** Replace the repetitive `if/else` logic with **Pydantic models** to organize and validate the data more efficiently. This reduced code duplication and made the implementation cleaner, more readable, and easier to maintain.

## mbidlal — Maze Wall Rendering Using Bitwise Operations

**Challenge:** While implementing maze rendering, mbidlal discovered that the `mazegenerator-2.1.0-py3-none-any` library represented walls using numerical values rather than simple Boolean values. However, the rendering logic needed `True` when a wall existed and `False` when there was no wall.

**Investigation:** mbidlal explored how the library encoded wall information and researched bitwise operations to extract individual wall states from the numerical values.

**Solution:** Use **bitwise operations** to check whether specific walls exist. By applying bitwise AND (`&`) with the appropriate wall masks, the numerical values could be converted into Boolean conditions: `True` for an existing wall and `False` for an absent wall.

**Outcome:** This made it possible to correctly identify and render the maze walls while keeping the wall detection logic simple and efficient.

## mbidlal — Smooth Pac-Man Movement

**Challenge:** Pac-Man initially moved directly from one maze cell to another, making the movement look abrupt instead of smooth.

**Investigation:** mbidlal explored how to separate grid-based movement logic from the visual position of Pac-Man to achieve smoother movement between cells.

**Solution:** Use **linear interpolation** between adjacent maze cells to calculate intermediate pixel positions. This allowed Pac-Man to move smoothly on the screen while keeping the movement logic based on the maze grid.

**Outcome:** Pac-Man's movement became more fluid and visually consistent with the game's animation.
