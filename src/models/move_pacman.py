from src.engine.load_gifs import load_gif_frames
from src.models.maze import Maze_screen
import pygame
from typing import Tuple, List, Dict, Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.engine.game_engine import Engine


class Pacman_face(Maze_screen):
    """
    Manage Pac-Man animations and movement inside the maze.
    """

    def __init__(self, screen_w: int, screen_h: int, maze_w: int, maze_h: int,
                 screen: pygame.surface.Surface, data: Dict[str, Any],
                 engine: "Engine", level: int):
        """
        Initialize Pac-Man and load its animation frames.

        Args:
            screen_w: The width of the game screen.
            screen_h: The height of the game screen.
            maze_w: The number of maze columns.
            maze_h: The number of maze rows.
            screen: The Pygame surface used to draw the game.
            data: The game configuration data.
            engine: The game engine instance.
            level: The current game level.

        Returns:
            None.
        """

        super().__init__(screen_w, screen_h, maze_w, maze_h, screen, data,
                         engine, level)

        self.pacman_up = load_gif_frames("assists/images/pacman/up.gif")
        self.pacman_down = load_gif_frames("assists/images/pacman/down.gif")
        self.pacman_left = load_gif_frames("assists/images/pacman/left.gif")
        self.pacman_right = load_gif_frames("assists/images/pacman/right.gif")
        self.index = 0
        self.last_animation_time = 0
        self.animation_delay = 250
        self.frames = self.pacman_right

    def draw_face(self, pacman_pos: List[int],
                  direction: Optional[str]) -> None:
        """
        Draw Pac-Man with the correct animation for its direction.

        Args:
            pacman_pos: The current X and Y position of Pac-Man.
            direction: The movement direction (up, down, left, right,
                blocked, or None).

        Returns:
            None.
        """

        pacman_size = self.cell_size - 15
        current_time = pygame.time.get_ticks()
        if direction is None:
            self.frames = self.pacman_right
            self.index = 0
        elif direction == "up":
            self.frames = self.pacman_up
        elif direction == "down":
            self.frames = self.pacman_down
        elif direction == "left":
            self.frames = self.pacman_left
        elif direction == "right":
            self.frames = self.pacman_right
        elif direction == "blocked":
            self.index = 0

        if direction is not None and direction != "blocked":
            if current_time - self.last_animation_time >= self.animation_delay:
                self.index = (self.index + 1) % len(self.frames)
                self.last_animation_time = current_time

        pacman_image = pygame.transform.scale(self.frames[self.index],
                                              (pacman_size, pacman_size))
        self.screen.blit(pacman_image, (pacman_pos[0] - pacman_size // 2,
                                        pacman_pos[1] - pacman_size // 2))

    def target_pacman(
            self, current_pos: List[int], direction: str,
            walls: List[List[Dict[str, bool]]]) -> Optional[Tuple[int, int]]:
        """
        Find the next position Pac-Man can move to.

        Args:
            current_pos: The current X and Y position of Pac-Man.
            direction: The direction Pac-Man wants to move.
            walls: The wall information for every maze cell.

        Returns:
            The target X and Y position if the path is free.
            None if there is a wall or the position is outside the maze.
        """

        c_x = int((current_pos[0] - self.start_x) // self.cell_size)
        c_y = int((current_pos[1] - self.start_y) // self.cell_size)

        if not (0 <= c_x < self.maze_w and 0 <= c_y < self.maze_h):
            return None
        if direction == "up":
            if not walls[c_y][c_x]['N']:
                target = (current_pos[0], current_pos[1] - self.cell_size)
                return target
            else:
                return None
        elif direction == "down":
            if not walls[c_y][c_x]['S']:
                return (current_pos[0], current_pos[1] + self.cell_size)
        elif direction == "left":
            if not walls[c_y][c_x]['W']:
                return (current_pos[0] - self.cell_size, current_pos[1])
        elif direction == "right":
            if not walls[c_y][c_x]['E']:
                return (current_pos[0] + self.cell_size, current_pos[1])
        return None

    def move_pacman(self, current_pos: List[int], target: Tuple[int, int],
                    speed: int) -> bool:
        """
        Move Pac-Man towards the target position.

        Args:
            current_pos: The current X and Y position of Pac-Man.
            target: The destination X and Y position.
            speed: The number of pixels Pac-Man moves each update.

        Returns:
            True if Pac-Man reaches the target position, otherwise False.
        """

        if target is None:
            return True
        if current_pos[1] > target[1]:
            current_pos[1] = max(target[1], current_pos[1] - speed)

        elif current_pos[1] < target[1]:
            current_pos[1] = min(target[1], current_pos[1] + speed)

        if current_pos[0] < target[0]:
            current_pos[0] = min(target[0], current_pos[0] + speed)

        elif current_pos[0] > target[0]:
            current_pos[0] = max(target[0], current_pos[0] - speed)

        return tuple(current_pos) == target
