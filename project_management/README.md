# Project Management — Pac-Man

This directory documents the collaborative development of the 1337/42 Pac-Man project by **hamezoua** and **mbidlal** over approximately **one month**.

## Approach

We divided responsibilities by feature, worked in parallel in a shared GitHub repository using individual branches, and merged our changes into `main`. We encountered and resolved merge conflicts, learning more about Git during integration. We validated the game through manual testing rather than an automated test suite.

We chose **Pygame** over MLX for its Python-focused development workflow, while taking the subject's MLX-equivalent graphical-operation restriction into account. We implemented custom pixel, line, and rectangle drawing helpers. This choice and its limitations are explained in [Technical Decisions](technical_decisions.md).

## Documents

| Document | Purpose |
| --- | --- |
| [Task Distribution](timeline.md) | Team responsibilities and collaboration |
| [Technical Decisions](technical_decisions.md) | Library selection, architecture, ghost movement and scared-mode decisions |
| [Risk Analysis](risk_analysis.md) | Actual issues, possible risks, and mitigations |
| [Challenges and Solutions](challenges.md) | Technical obstacles, resolutions, and space for mbidlal's account |

## Testing and Validation

Both teammates manually tested their work and the integrated game. We used hands-on gameplay and debugging to investigate issues; we do **not** claim an automated test suite or a complete recorded acceptance-test matrix. The project subject's evaluation requirements should still be checked before submission.

## Delivery Status
 itech.io link here

