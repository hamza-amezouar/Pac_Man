from src.engine.load_gifs import load_gif_frames
from src.models.maze import Maze_screen
from typing import List, Dict, Any, Tuple, Set, Optional, TYPE_CHECKING
import random
import pygame


if TYPE_CHECKING:
    from src.models.screen_maze import Update_game


class Ghosts(Maze_screen):
    """
    Manage the ghosts in the maze.

    This class controls ghost movement, images, paths, and behavior.
    It also handles chasing Pac-Man and scared mode.
    """

    def __init__(self, screen_w: int, screen_h: int, maze_w: int, maze_h: int,
                 screen: pygame.surface.Surface, walls: List[List[Dict[str,
                                                                       bool]]],
                 data: Dict[str, Any], update_game: "Update_game", level: int):
        """
        Initialize the ghosts and load their images.

        Args:
            screen_w: The width of the game screen.
            screen_h: The height of the game screen.
            maze_w: The width of the maze.
            maze_h: The height of the maze.
            screen: The Pygame surface used to draw the ghosts.
            walls: The walls of the maze.
            data: The game settings.
            update_game: Manage all game levels and show the final high scores.
            level: The current game level.

        Returns:
            None.
        """
        super().__init__(screen_w, screen_h, maze_w, maze_h, screen, data,
                         update_game, level)
        
        self.current_frame = 0
        self.old_cell = (0, 0)
        self.walls = walls
        self.Scared_Mode = False
        self.pacgums_pos = [(0, 0), (0, self.maze_h - 1), (self.maze_w - 1, 0),
                            (self.maze_w - 1, self.maze_h - 1)]

        self.ghost_image = load_gif_frames("assists/images/redghost.gif")

    def calculate_ghost_path(
            self, current_pos: Tuple[int, int],
            goal_pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Find a path between the ghost and its target.

        Uses the BFS algorithm to find a path through the maze.

        Args:
            current_pos: The current position of the ghost.
            goal_pos: The target position in the maze.

        Returns:
            A list of positions that the ghost must follow.
            If no path is found, returns the current position.
        """
        queue = []
        visited: Set[Tuple[int, int]] = set()
        parrent = {}
        path = []

        queue.append((current_pos))
        visited.add((current_pos))

        while queue:
            (x, y) = queue.pop(0)
            if (x, y) == goal_pos:
                break
            corr = self.walls[y][x]
            if not corr['N'] and 0 <= y - 1:
                if not (x, y - 1) in visited:
                    queue.append((x, y - 1))
                    parrent[(x, y - 1)] = (x, y)
                    visited.add((x, y - 1))

            if not corr['S'] and y < self.maze_h - 1:
                if not (x, y + 1) in visited:
                    queue.append((x, y + 1))
                    parrent[(x, y + 1)] = (x, y)
                    visited.add((x, y + 1))

            if not corr['W'] and 0 <= x - 1:
                if not (x - 1, y) in visited:
                    queue.append((x - 1, y))
                    parrent[(x - 1, y)] = (x, y)
                    visited.add((x - 1, y))

            if not corr['E'] and x < self.maze_w - 1:
                if not (x + 1, y) in visited:
                    queue.append((x + 1, y))
                    parrent[(x + 1, y)] = (x, y)
                    visited.add((x + 1, y))
        pos = goal_pos
        if pos not in parrent:
            return [current_pos]
        while pos != current_pos:
            path.append(pos)
            pos = parrent[pos]
        path.append(current_pos)
        return path[::-1]

    def update_ghost_image(self, current_pos: Tuple[int, int],
                           goal_pos: Tuple[int, int],
                           ghost_data: Dict[str, Any]) -> str:
        """
        Choose the ghost image based on its movement direction.

        Args:
            current_pos: The current position of the ghost.
            goal_pos: The next position of the ghost.
            ghost_data: Information about the ghost.

        Returns:
            The direction name used to select the ghost image.
        """
        current_x, current_y = current_pos
        goal_x, goal_y = goal_pos
        if current_x > goal_x:
            return "right"

        elif current_x < goal_x:
            return "left"

        elif current_y > goal_y:
            return "up"

        elif current_y < goal_y:
            return "down"
        else:
            return str(ghost_data["final_mode"])

    def init_ghosts(self) -> Dict[str, Dict[str, Any]]:
        """
        Create the initial data for all ghosts.

        Returns:
            A dictionary containing the positions, colors, speeds,
            and movement information of each ghost.
        """
        ghosts_data = {
            "red": {
                "my_pos": (self.maze_w - 1, self.maze_h - 1),
                "pos": (self.maze_w - 1, self.maze_h - 1),
                "current_pos": 0,
                "move_now": 0,
                "old_path": [],
                "color": "red",
                "current_frame": 0,
                "final_mode": "right",
                "total_speed": 30,
                "remain": False,
                "was_eaten": False,
                "add_score": False,
                "goal_pos": (0, 0)
            },
            "blue": {
                "my_pos": (0, 0),
                "pos": (0, 0),
                "current_pos": 0,
                "move_now": 0,
                "old_path": [],
                "color": "blue",
                "current_frame": 0,
                "final_mode": "right",
                "total_speed": 30,
                "remain": False,
                "was_eaten": False,
                "add_score": False,
                "goal_pos": (0, 0)
            },
            "yellow": {
                "my_pos": (self.maze_w - 1, 0),
                "pos": (self.maze_w - 1, 0),
                "current_pos": 0,
                "move_now": 0,
                "old_path": [],
                "color": "yellow",
                "current_frame": 0,
                "final_mode": "right",
                "total_speed": 30,
                "remain": False,
                "was_eaten": False,
                "add_score": False,
                "goal_pos": (0, 0)
            },
            "pink": {
                "my_pos": (0, self.maze_h - 1),
                "pos": (0, self.maze_h - 1),
                "current_pos": 0,
                "move_now": 0,
                "old_path": [],
                "color": "pink",
                "current_frame": 0,
                "final_mode": "right",
                "total_speed": 30,
                "remain": False,
                "was_eaten": False,
                "add_score": False,
                "goal_pos": (0, 0)
            }
        }
        return ghosts_data

    def chase(self, current_pos: Tuple[int, int], goal_pos: Tuple[int, int],
              total_steps: int, specter: Dict[str, Any]) -> None:
        """
        Move and draw a ghost while it chases its target.

        Args:
            current_pos: The current position of the ghost.
            goal_pos: The target position of the ghost.
            total_steps: The number of steps needed to reach the target.
            specter: Information about the ghost.

        Returns:
            None.
        """
        specter["total_speed"] = 30
        image_mode = self.update_ghost_image(current_pos, goal_pos, specter)
        images = load_gif_frames(
            f"assists/images/ghosts/{specter['color']}{image_mode}.gif")
        specter["final_mode"] = image_mode

        current_x, current_y = current_pos
        goal_x, goal_y = goal_pos
        start_pixel_x = self.start_x + (current_x *
                                        self.cell_size) + self.cell_size // 2
        start_pixel_y = self.start_y + (current_y *
                                        self.cell_size) + self.cell_size // 2

        goal_pixel_x = self.start_x + (goal_x *
                                       self.cell_size) + self.cell_size // 2
        goal_pixel_y = self.start_y + (goal_y *
                                       self.cell_size) + self.cell_size // 2

        progress = specter["move_now"] / total_steps

        self.pixel_x = start_pixel_x + (goal_pixel_x -
                                        start_pixel_x) * progress
        self.pixel_y = start_pixel_y + (goal_pixel_y -
                                        start_pixel_y) * progress
        size = self.cell_size - 10

        if current_pos == goal_pos:

            specter["current_frame"] -= 1
        if specter["current_frame"] >= len(
                images) or specter["current_frame"] < 0:
            specter["current_frame"] = 0

        specter["pos"] = (int(self.pixel_x), int(self.pixel_y))

        self.screen.blit(
            pygame.transform.scale(images[specter["current_frame"]],
                                   (size, size)),
            (self.pixel_x - size // 2, self.pixel_y - size // 2))
        if self.old_cell != (start_pixel_x, start_pixel_y):
            self.current_frame = (self.current_frame + 1) % len(
                self.ghost_image)
        self.old_cell = (start_pixel_x, start_pixel_y)

    def ghosts_brain(self, specter: Dict[str, Any], direction: Optional[str],
                     pacman_pos: List[int]) -> Tuple[int, int]:
        """
        Choose a target position based on the ghost's behavior.

        Each ghost uses a different rule to choose where to move.

        Args:
            specter: Information about the ghost.
            direction: The current direction of Pac-Man.
            pacman_pos: The pixel position of Pac-Man.

        Returns:
            The target position as maze coordinates (x, y).
        """

        x = int((pacman_pos[0] - self.start_x) // self.cell_size)
        y = int((pacman_pos[1] - self.start_y) // self.cell_size)
        if specter["color"] == "pink" and direction:
            g_x, g_y = specter["pos"]
            if abs(x - g_x) + abs(y - g_y) <= 3:

                return (x, y)

            if direction == "up":
                if y - 6 >= 0:
                    y -= 6
            elif direction == "down":
                if y + 6 < self.maze_h:
                    y += 6
            elif direction == "left":
                if x - 6 >= 0:
                    x -= 6
            elif direction == "right":
                if x + 6 < self.maze_w:
                    x += 6

            if (x, y) == specter["pos"]:
                return (x, y)
        elif specter["color"] == "blue" and direction:
            X, Y = (x, y)
            if direction == "up":
                if Y - 7 >= 0:
                    Y -= 7
                else:
                    Y = 0
            elif direction == "down":
                if Y + 7 < self.maze_h:
                    Y += 7
                else:
                    Y = self.maze_h - 1
            elif direction == "right":
                if X + 7 < self.maze_w:
                    X += 7
                else:
                    X = self.maze_w - 1
            elif direction == "left":
                if X - 7 >= 0:
                    X -= 7
                else:
                    X = 0
            if (X, Y) != (x, y):
                x, y = (X, Y)
        elif specter["color"] == "yellow" and direction:
            g_x, g_y = specter["pos"]
            if abs(x - g_x) + abs(y - g_y) <= 1:
                return (x, y)
            X = random.randint(0, self.maze_w - 1)
            Y = random.randint(0, self.maze_h - 1)
            x, y = (X, Y)
        return (x, y)

    def is_caught(self, data_ghosts: Dict[str, Dict[str, Any]],
                  pacman_pos: List[int]) -> int:
        """
        Check if a ghost catches Pac-Man based on precise pixel distance.
        """
        # if self.old_pacman_cell == pacman_pos:
        #     return 0
        p_x, p_y = pacman_pos[0], pacman_pos[1]
        collision_threshold = self.cell_size // 2
        for color in data_ghosts.keys():
            g_x, g_y = data_ghosts[color]["pos"]
            distance = ((g_x - p_x) ** 2 + (g_y - p_y) ** 2) ** 0.5
            if distance < collision_threshold:
                return 1
        return 0

    def is_eat_super_pacgums(self, pacman_pos: List[int]) -> bool:
        """
        Check if Pac-Man eats a super pac-gum.

        Args:
            pacman_pos: The pixel position of Pac-Man.

        Returns:
            True if Pac-Man eats a super pac-gum, otherwise False.
        """
        x = int((pacman_pos[0] - self.start_x) // self.cell_size)
        y = int((pacman_pos[1] - self.start_y) // self.cell_size)
        if (x, y) in self.pacgums_pos:
            self.pacgums_pos.remove((x, y))
            return True
        return False

    def scared(self,
               current_pos: Tuple[int, int],
               goal_pos: Tuple[int, int],
               total_steps: int, specter: Dict[str, Any],
               start_ticks: int) -> None:
        """
        Draw a ghost in scared mode.

        Changes the ghost's appearance and speed while scared.
        It also handles the timer and the animation when a ghost is eaten.

        Args:
            current_pos: The current position of the ghost.
            goal_pos: The target position of the ghost.
            total_steps: The number of steps needed to reach the target.
            specter: Information about the ghost.
            start_ticks: The time when scared mode started.

        Returns:
            None.
        """

        goal_timestamp = 12
        current_ticks = pygame.time.get_ticks()
        elapsed_time = current_ticks - start_ticks
        remaining_time = goal_timestamp - (elapsed_time / 1000)
        if remaining_time < 0:
            self.Scared_Mode = False
        if remaining_time < 3:
            if specter["remain"]:
                specter["remain"] = False
            else:
                specter["remain"] = True
        if specter["remain"]:
            images = load_gif_frames("assists/images/ghosts/scard1.gif")
        else:
            images = load_gif_frames("assists/images/ghosts/scard.gif")
        if specter["was_eaten"]:
            mode = self.update_ghost_image(current_pos, goal_pos, specter)
            images = load_gif_frames(f"assists/images/ghosts/eyes/{mode}.png")
            specter["total_speed"] = 5
        else:
            specter["total_speed"] = 20
        current_x, current_y = current_pos
        goal_x, goal_y = goal_pos
        start_pixel_x = self.start_x + (current_x *
                                        self.cell_size) + self.cell_size // 2
        start_pixel_y = self.start_y + (current_y *
                                        self.cell_size) + self.cell_size // 2

        goal_pixel_x = self.start_x + (goal_x *
                                       self.cell_size) + self.cell_size // 2
        goal_pixel_y = self.start_y + (goal_y *
                                       self.cell_size) + self.cell_size // 2

        progress = specter["move_now"] / total_steps

        self.pixel_x = start_pixel_x + (goal_pixel_x -
                                        start_pixel_x) * progress
        self.pixel_y = start_pixel_y + (goal_pixel_y -
                                        start_pixel_y) * progress
        size = self.cell_size - 10

        if current_pos == goal_pos:
            specter["current_frame"] -= 1
        if specter["current_frame"] >= len(
                images) or specter["current_frame"] < 0:
            specter["current_frame"] = 0

        specter["pos"] = (int(self.pixel_x), int(self.pixel_y))

        self.screen.blit(
            pygame.transform.scale(images[specter["current_frame"]],
                                   (size, size)),
            (self.pixel_x - size // 2, self.pixel_y - size // 2))
        if self.old_cell != (start_pixel_x, start_pixel_y):
            self.current_frame = (self.current_frame + 1) % len(
                self.ghost_image)
        self.old_cell = (start_pixel_x, start_pixel_y)

    def was_eaten_ghosts(self, ghosts_data: Dict[str, Dict[str, Any]],
                         pacman_pos: List[int], update_game: "Update_game") -> None:
        """
        Check if Pac-Man eats a ghost.

        If a ghost is in the same maze cell as Pac-Man, mark it as eaten.

        Args:
            ghosts_data: A dictionary containing information about all ghosts.
            pacman_pos: The pixel position of Pac-Man.

        Returns:
            None.
        """

        x = pacman_pos[0]
        y = pacman_pos[1]
        collision_threshold = self.cell_size // 2
        for specter in ghosts_data:
            g_x = ghosts_data[specter]["pos"][0]
            g_y = ghosts_data[specter]["pos"][1]
            distance = ((g_x - x) ** 2 + (g_y - y) ** 2) ** 0.5
            if distance < collision_threshold:
                ghosts_data[specter]["was_eaten"] = True
                if not ghosts_data[specter]["add_score"]:
                    self.update_game.score += self.data["points_per_ghost"]
                    ghosts_data[specter]["add_score"] = True

    def create_random_path(self, pacman_pos: List[int],
                           specter: Dict[str, Any]) -> None:
        """Assigns random escape positions to ghosts
        based on Pac-Man's location.

        Determines Pac-Man's current maze quadrant and generates random target
        positions for each ghost in the opposite quadrant. Ensures that each
        ghost receives a unique escape position.

        Args:
            pacman_pos (List[int]): Pac-Man's current pixel coordinates (x, y).
            ghosts_data: Dictionary containing ghost information, updated with
                each ghost's randomly generated scared position.

        Returns:
            None
        """
        x = int((pacman_pos[0] - self.start_x) // self.cell_size)
        y = int((pacman_pos[1] - self.start_y) // self.cell_size)
        current_x = int((specter["pos"][0] - self.start_x) // self.cell_size)
        current_y = int((specter["pos"][1] - self.start_y) // self.cell_size)
        if x > (self.maze_w // 2) and y > (self.maze_h // 2):

            c_x = random.randint(0, self.maze_w // 2)
            c_y = random.randint(0, self.maze_h // 2)
            if not specter["scared_pos"]:
                while len(
                    self.calculate_ghost_path(
                        (current_x, current_y), (c_x, c_y)
                        )) == 1:
                    c_x = random.randint(0, self.maze_w // 2)
                    c_y = random.randint(0, self.maze_h // 2)
                specter["scared_pos"] = (c_x, c_y)

            elif specter["scared_pos"] == (current_x, current_y):
                while len(
                    self.calculate_ghost_path(
                        (current_x, current_y), (c_x, c_y)
                        )) == 1:
                    c_x = random.randint(0, self.maze_w // 2)
                    c_y = random.randint(0, self.maze_h // 2)
                specter["scared_pos"] = (c_x, c_y)

        elif x > (self.maze_w // 2) and y <= (self.maze_h // 2):
            c_x = random.randint(0, self.maze_w // 2)
            c_y = random.randint(self.maze_h // 2, self.maze_h - 1)

            if not specter["scared_pos"]:
                while len(
                    self.calculate_ghost_path(
                        (current_x, current_y), (c_x, c_y)
                        )) == 1:
                    c_x = random.randint(0, self.maze_w // 2)
                    c_y = random.randint(self.maze_h // 2, self.maze_h - 1)
                specter["scared_pos"] = (c_x, c_y)

            elif specter["scared_pos"] == (current_x, current_y):
                while len(
                    self.calculate_ghost_path(
                        (current_x, current_y), (c_x, c_y)
                        )) == 1:

                    c_x = random.randint(0, self.maze_w // 2)
                    c_y = random.randint(self.maze_h // 2, self.maze_h - 1)
                specter["scared_pos"] = (c_x, c_y)

        elif x <= (self.maze_w // 2) and y > (self.maze_h // 2):

            c_x = random.randint(self.maze_w // 2, self.maze_w - 1)
            c_y = random.randint(0, self.maze_h // 2)

            if not specter["scared_pos"]:
                while len(
                    self.calculate_ghost_path(
                        (current_x, current_y), (c_x, c_y)
                        )) == 1:

                    c_x = random.randint(self.maze_w // 2, self.maze_w - 1)
                    c_y = random.randint(0, self.maze_h // 2)
                specter["scared_pos"] = (c_x, c_y)

            elif specter["scared_pos"] == (current_x, current_y):
                while len(
                    self.calculate_ghost_path(
                        (current_x, current_y), (c_x, c_y)
                        )) == 1:

                    c_x = random.randint(self.maze_w // 2, self.maze_w - 1)
                    c_y = random.randint(0, self.maze_h // 2)
                specter["scared_pos"] = (c_x, c_y)

        elif x <= (self.maze_w // 2) and y <= (self.maze_h // 2):

            c_x = random.randint(self.maze_w // 2, self.maze_w - 1)
            c_y = random.randint(self.maze_h // 2, self.maze_h - 1)

            if not specter["scared_pos"]:
                while len(
                    self.calculate_ghost_path(
                        (current_x, current_y), (c_x, c_y)
                        )) == 1:

                    c_x = random.randint(self.maze_w // 2, self.maze_w - 1)
                    c_y = random.randint(self.maze_h // 2, self.maze_h - 1)
                specter["scared_pos"] = (c_x, c_y)

            elif specter["scared_pos"] == (current_x, current_y):
                while len(
                    self.calculate_ghost_path(
                        (current_x, current_y), (c_x, c_y)
                        )) == 1:

                    c_x = random.randint(self.maze_w // 2, self.maze_w - 1)
                    c_y = random.randint(self.maze_h // 2, self.maze_h - 1)
                specter["scared_pos"] = (c_x, c_y)
