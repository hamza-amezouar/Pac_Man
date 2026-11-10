# Risk Analysis

This register distinguishes **issues that actually occurred** from **potential risks**. It is a qualitative retrospective, not a numerical risk-scoring exercise.

| Risk / issue | Impact | Response or mitigation | Status |
| --- | --- | --- | --- |
| Ghosts jumping visibly between cells | Unnatural movement | Use linear interpolation between grid-cell centers | **Occurred; addressed** |
| Scared ghosts failing to flee dynamically | Less convincing scared behavior | Choose escape targets in regions opposite Pac-Man | **Design challenge; addressed** |
| Git merge conflicts | Delays and difficulty combining changes | Learn Git conflict resolution and integrate branches carefully | **Occurred; resolved** |
| Invalid configuration or missing files | Game may fail to start or behave unexpectedly | Review configuration validation and test error cases manually | **Potential risk; manual testing performed** |
| Packaging or Itch.io publishing issues | Reviewers may not be able to run a distributed build | Verify packaging and release once ready | **Pending confirmation** |

## Risk Review

The most significant confirmed integration issue was Git merge conflicts. Both teammates had to improve their understanding of branches and conflict resolution. The confirmed movement issue was addressed by changing how ghost positions are rendered.

We do not claim formal severity ratings, assigned risk owners, or successful completion of specific unrecorded test cases.
