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

> **To be completed by mbidlal.** Add real challenges from maze rendering, Pac-Man movement, the instructions screen, the Makefile, or other work. For each challenge, describe:
>
> - What went wrong and why it mattered.
> - What you tried or researched.
> - The solution you actually implemented.
> - The relevant file or function.
>
> Do not invent issues merely to fill this section.
