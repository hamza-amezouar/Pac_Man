import pygame

from src.engine.load_gifs import load_gif_frames
from src.models.maze import  Maze_screen


class Ghosts(Maze_screen):
    def __init__(self, screen_w, screen_h, maze_w, maze_h, screen, walls):
        super().__init__(screen_w, screen_h, maze_w, maze_h, screen)
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.maze_w = maze_w
        self.maze_h = maze_h
        self.screen = screen
        self.walls = walls
        self.current_frame = 0
        self.old_cell = (0, 0)
        self.ghost_image = load_gif_frames("assists/images/redghost.gif")
        self.pacman_image = pygame.image.load("assists/images/oacmn.gif").convert_alpha()

    def calculate_ghost_path(self, current_pos, goal_pos):
        queue = []
        visited = set()
        parrent = {}
        path = []
        c_x = int((goal_pos[0] - self.start_x) // self.cell_size)
        c_y = int((goal_pos[1] - self.start_y) // self.cell_size)
        goal_pos = (c_x, c_y)
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
        if not pos in parrent:
            return [current_pos]
        while pos != current_pos:
            path.append(pos)
            pos = parrent[pos]
        path.append(current_pos)
        return path[::-1]
        
    def update_ghost_image(self, current_pos , goal_pos, ghost_data):
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
            return ghost_data["final_mode"]
    
    def init_ghosts(self):
        ghosts_data = {
            "red": {"pos": (self.maze_w - 1, self.maze_h - 1), "current_pos": 0, "move_now": 0, "old_path": [], "color": "red", "current_frame": 0, "final_mode": "right"},
            "blue": {"pos": (0, 0), "current_pos": 0, "move_now": 0, "old_path": [], "color": "blue", "current_frame": 0, "final_mode": "right"},
            "yellow": {"pos": (self.maze_w - 1, 0), "current_pos": 0, "move_now": 0, "old_path": [], "color": "yellow", "current_frame": 0, "final_mode": "right"},
            "pink": {"pos": (0, self.maze_h - 1), "current_pos": 0, "move_now": 0, "old_path": [], "color": "pink", "current_frame": 0, "final_mode": "right"}
            }
        return ghosts_data

    def chase(self, current_pos, goal_pos, total_steps, ghost_data):

        image_mode = self.update_ghost_image(current_pos , goal_pos, ghost_data)
        images = load_gif_frames(f"assists/images/ghosts/{ghost_data["color"]}{image_mode}.gif")
        ghost_data["final_mode"] = image_mode
        current_x, current_y = current_pos
        goal_x, goal_y = goal_pos
        start_pixel_x = self.start_x + (current_x * self.cell_size) + self.cell_size // 2
        start_pixel_y = self.start_y + (current_y * self.cell_size) + self.cell_size // 2

        goal_pixel_x = self.start_x + (goal_x * self.cell_size) + self.cell_size // 2
        goal_pixel_y = self.start_y + (goal_y * self.cell_size) + self.cell_size // 2


        progress = ghost_data["move_now"] / total_steps
        
        self.pixel_x = start_pixel_x + (goal_pixel_x - start_pixel_x) * progress
        self.pixel_y = start_pixel_y + (goal_pixel_y - start_pixel_y) * progress
        size = self.cell_size - 10

        if current_pos == goal_pos:
            ghost_data["current_frame"] -= 1
        if ghost_data["current_frame"] >= len(images) or ghost_data["current_frame"] < 0:
            ghost_data["current_frame"] = 0

        self.screen.blit(
            pygame.transform.scale(images[ghost_data["current_frame"]], (size, size)),
            (self.pixel_x - size // 2, self.pixel_y - size // 2)
        )
        if self.old_cell != (start_pixel_x, start_pixel_y):
            self.current_frame = (self.current_frame + 1) % len(self.ghost_image)
        self.old_cell = (start_pixel_x, start_pixel_y)