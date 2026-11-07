# Timeline and Progress

## Project Duration

The Pac-Man project took approximately **one month (four weeks)**. Although the game's basic concept is familiar, its implementation involved multiple interconnected systems: maze rendering, player and ghost movement, game state management, menus, scoring, and persistent highscores.

We worked on different modules in parallel. The week-by-week breakdown below is a **phase-based approximation**, not a verified day-by-day history or original dated plan.

## Development Timeline

| Approximate period | Phase | Main activities |
| --- | --- | --- |
| Week 1 | Planning and setup | Reviewed requirements, discussed architecture, compared Pygame with MLX, chose Pygame with custom drawing primitives, created the GitHub repository and individual branches. |
| Week 2 | Core gameplay | Developed maze drawing, Pac-Man movement, ghost behavior and game-loop components in parallel. |
| Week 3 | Interfaces and features | Worked on menus, instructions, highscores, scared mode, visual assets, and ongoing feature integration. |
| Week 4 | Integration and validation | Merged branches, learned to resolve Git conflicts, manually tested gameplay, fixed problems, and prepared documentation. |

## Progress Tracking

| Milestone | Status | Notes |
| --- | --- | --- |
| GitHub repository and individual branches | Completed | Shared repository and separate development branches |
| Maze rendering and Pac-Man movement | Implemented | mbidlal's primary responsibility |
| Ghost movement and scared mode | Implemented | hamezoua's primary responsibility |
| Game engine, menus and highscores | Implemented | Feature development and integration |
| Integration into `main` | Completed | Merge conflicts occurred and were resolved |
| Manual testing | Performed | Both members tested the game manually |
| Root README and project management | In progress / being finalized | Documentation prepared for review |
| Packaging and Itch.io publication | Not yet confirmed | Update after deployment |

## Changes and Obstacles

The main technical challenge in ghost movement was the abrupt jump between maze cells. We used **linear interpolation** to make movement appear smooth while retaining cell-based navigation. For scared mode, we selected escape targets in regions opposite Pac-Man.

Merging individual branches also caused **Git conflicts**. We spent additional time learning Git and resolving the conflicts before continuing integration.

## Validation

We performed manual gameplay testing during development and after integrating work. We have not documented automated tests or individual test pass/fail records.

## Schedule Accuracy

Exact start/end dates, original estimates, and measured delays were not recorded here. The four-week table should be treated as a retrospective summary rather than a historical Gantt chart.
