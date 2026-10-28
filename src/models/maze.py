from mazegenerator.mazegenerator import MazeGenerator
from src.config_parser import Parse
from src.helper_func.draw_line import ft_draw_line
from typing import Tuple, List, Dict, Any, TYPE_CHECKING
import pygame
import random
import time

if TYPE_CHECKING:
    from src.engine.game_engine import Engine

class Maze(MazeGenerator):

    def __init__(self,
                 size: Tuple[int, int] = (15, 15),
                 perfect: bool = False,
                 seed: int = 0,
                 level: int = 1) -> None:
        self._level = level
        if level != 1:
            seed = 0
        super().__init__(size=size, perfect=perfect, seed=seed)

    def get_walls(self) -> List[List[Dict[str, bool]]]:
        cells = self.maze
        directions = {"N": 1, "E": 2, "S": 4, "W": 8}

        column_direction = []
        for row in cells:
            row_direction = []
            for cell in row:
                cell_direction = {}
                for direction, value in directions.items():
                    cell_direction[direction] = bool(cell & value)
                row_direction.append(cell_direction)
            column_direction.append(row_direction)

        return column_direction

    @property
    def get_width(self) -> Any:
        return self._width

    @property
    def get_height(self) -> Any:
        return self._height


class Maze_screen:
    def __init__(self, screen_w, screen_h, maze_w: int, maze_h: int,
                 screen: pygame.surface.Surface, data:Parse, engine:"Engine",level):
        self.engine = engine
        self.level = level
        self.data = data
        self.screen = screen
        self.width = screen_w
        self.height = screen_h
        self.maze_w = maze_w
        self.maze_h = maze_h
        padding_x = 50
        padding_y = 150

        available_width = self.width - (2 * padding_x)
        available_height = self.height - (2 * padding_y)

        self.cell_size = min(available_width // self.maze_w,
                             available_height // self.maze_h)

        self.maze_pixel_w = self.maze_w * self.cell_size
        self.maze_pixel_h = self.maze_h * self.cell_size
        self.start_x = (self.width - self.maze_pixel_w) // 2
        self.start_y = (self.height - self.maze_pixel_h) // 2
        self.pacman_pos = []
    
        self.super_size = round(self.cell_size * 0.70)
        self.pacgum_size = round(self.cell_size * 0.30)
    
        pacgums_img = pygame.image.load("assists/images/pacgum.png")
        super_pacgum_img = pygame.image.load("assists/images/super_pacgum.png")
        self.pacgums = pygame.transform.scale(pacgums_img, (self.pacgum_size, self.pacgum_size))
        self.super_pacgum = pygame.transform.scale(super_pacgum_img, (self.super_size, self.super_size))

    def draw_maze(self, walls: List[List[Dict[str, bool]]]):
        # top wall
        ft_draw_line(self.screen, (2, 255, 200),
                         (self.start_x, self.start_y),
                         (self.start_x + self.maze_pixel_w, self.start_y), 5)
        # left wall
        ft_draw_line(self.screen, (2, 255, 200),
                         (self.start_x, self.start_y),
                         (self.start_x, self.start_y + self.maze_pixel_h), 5)
        i = 0
        for y in range(self.maze_h):
            for x in range(self.maze_w):
                cell_x = self.start_x + x * self.cell_size
                cell_y = self.start_y + y * self.cell_size

                if walls[y][x]['N'] and walls[y][x]['E'] and walls[y][x][
                        'S'] and walls[y][x]['W']:
                    i += 1
                    ft_draw_line(self.screen, (255, 100, 100),
                                    (cell_x + 5, cell_y + 5 ),
                                    (cell_x + self.cell_size,
                                    cell_y + 5 ),
                                    self.cell_size)

                if walls[y][x]['E']:
                    ft_draw_line(
                        self.screen, (2, 255, 200),
                        (cell_x + self.cell_size, cell_y),
                        (cell_x + self.cell_size, cell_y + self.cell_size), 5)
                    
                if walls[y][x]['S']:
                    ft_draw_line(
                        self.screen, (2, 255, 200),
                        (cell_x, cell_y + self.cell_size),
                        (cell_x + self.cell_size + 4, cell_y + self.cell_size), 5)

                if i == 14:
                    if not self.pacman_pos:
                        cell_x = cell_x - self.cell_size
                        self.pacman_pos = [
                            cell_x + self.cell_size // 2,
                            cell_y + self.cell_size// 2
                        ]
                    i += 1

    def existing_pacgums(self, pacgum, walls):
        valid_cells = []
        super_pacgum = [(0, 0), (self.maze_w - 1, 0), (0, self.maze_h - 1),
                        (self.maze_w - 1, self.maze_h - 1)]
        i = 0
        for y in range(self.maze_h):
            for x in range(self.maze_w):
                if walls[y][x]['N'] and walls[y][x]['E'] and walls[y][x][
                        'S'] and walls[y][x]['W']:
                    i += 1
                    continue
                elif (x, y) in super_pacgum:
                    continue
                elif i == 13:
                    x += 1
                else:
                    valid_cells.append((x, y))
        pacgum -= 4           
        pacgums = random.sample(valid_cells, pacgum)
        total_pacgums = super_pacgum + pacgums
        return total_pacgums

    def draw_all_pacgums(self, pacgums):
        for c_x, c_y in pacgums:
            offset = (self.cell_size - self.super_size) // 2
            if c_x == 0 and c_y == 0:
                self.screen.blit(self.super_pacgum, (self.start_x + offset, self.start_y + offset))
            elif c_x == self.maze_w - 1 and c_y == 0:
                self.screen.blit(self.super_pacgum, (self.start_x + self.cell_size * c_x + offset, self.start_y + offset))
            elif c_x == 0 and c_y == self.maze_h - 1:
                self.screen.blit(self.super_pacgum, (self.start_x + offset, self.start_y + c_y * self.cell_size + offset))
            elif c_x == self.maze_w - 1 and c_y == self.maze_h - 1:
                self.screen.blit(self.super_pacgum, (self.start_x + c_x * self.cell_size + offset, self.start_y + c_y * self.cell_size + offset ))
            else:
                offset = (self.cell_size - self.pacgum_size) // 2
                self.screen.blit(self.pacgums, (self.start_x + c_x * self.cell_size + offset , self.start_y + c_y * self.cell_size + offset))

    def eats_pacgums(self, pacgums):
        super_pacgum = [(0, 0), (self.maze_w - 1, 0), (0, self.maze_h - 1),
                                (self.maze_w - 1, self.maze_h - 1)]
        for c_x, c_y in pacgums:
            cell_x =  int(self.start_x + c_x * self.cell_size + (self.cell_size // 2))
            cell_y = int(self.start_y + c_y * self.cell_size + (self.cell_size // 2))
            if self.pacman_pos == [cell_x, cell_y]:
                if (c_x, c_y) in super_pacgum :
                    self.engine.score += self.data["points_per_super_pacgum"]
                else:
                    self.engine.score += self.data["points_per_pacgum"]
                pacgums.remove((c_x, c_y))

    def menu_maze(self, start_ticks):
        font = pygame.font.Font("assists/fonts/PixeloidSansBold-1jpBg.ttf", 18)
        time_font = pygame.font.Font("assists/fonts/PixeloidSansBold-1jpBg.ttf", 20)
        goal_timestamp = self.engine.time
        current_ticks = pygame.time.get_ticks()
        elapsed_time = current_ticks - start_ticks
        remaining_time = goal_timestamp - (elapsed_time / 1000)
        time_text = time_font.render(f"Time: {int(remaining_time)}", True ,(255, 0, 0))
        if int(remaining_time) == -1:
           exit(0)
        score_text = font.render(f"Score: {self.engine.score}", True, (255, 255, 255))
        level_text = font.render(f"Level: {self.level} / {len(self.data['level'])}", True, (255, 255, 255))
        self.screen.blit(time_text, ((self.start_x + self.maze_pixel_w // 2) - 50 , self.start_y - 120 ))
        self.screen.blit(score_text, (self.start_x, self.start_y // 2 + 45))
        self.screen.blit(level_text, (self.start_x + (self.cell_size * self.maze_w) - 150, self.start_y // 2 + 45))

