from mazegenerator.mazegenerator import MazeGenerator
import pygame
from typing import Tuple, List, Dict, Any


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

    def ft_greed(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, (255, 11, 255), (x, 0),
                             (x, self.height), 5)
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, (255, 11, 255), (0, y),
                             (self.width, y), 5)

    def __init__(self, screen_w, screen_h, maze_w: int, maze_h: int,
                 screen: pygame.surface.Surface):
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
        self.pacman_pos = ()

    def draw_maze(self, walls: List[List[Dict[str, bool]]]) -> Tuple[int, int]:
        # top wall
        pygame.draw.line(self.screen, (2, 255, 200),
                         (self.start_x, self.start_y),
                         (self.start_x + self.maze_pixel_w, self.start_y), 5)
        # left wall
        pygame.draw.line(self.screen, (2, 255, 200),
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
                    pygame.draw.line(
                        self.screen, (255, 100, 100),
                        (cell_x, cell_y + self.cell_size // 2),
                        (cell_x + self.cell_size, cell_y + self.cell_size // 2),
                        self.cell_size)

                if walls[y][x]['E']:
                    pygame.draw.line(
                        self.screen, (2, 255, 200),
                        (cell_x + self.cell_size, cell_y),
                        (cell_x + self.cell_size, cell_y + self.cell_size), 5)
                if walls[y][x]['S']:
                    pygame.draw.line(
                        self.screen, (2, 255, 200),
                        (cell_x, cell_y + self.cell_size),
                        (cell_x + self.cell_size, cell_y + self.cell_size), 5)
                if i == 14:
                    self.pacman_pos = (cell_x - self.cell_size // 2,
                                       cell_y + self.cell_size // 2)
                    i += 1

    def draw_super_pacgum(self, pacgum):
        
        for y in range(self.maze_h):
            for x in range(self.maze_w):
                if x == 0 and y == 0:

                    pygame.draw.circle(self.screen,(228, 208, 10),
                                     (self.start_x + self.cell_size //2,
                                      self.start_y + self.cell_size// 2), self.cell_size // 2 - 15)
                #     pacgum -= 1
                # if x == self.maze_w - 1 and y == 0:
                #     self.screen.blit(self.super_pacgum,
                #                        (self.start_x + self.cell_size * x +
                #                         self.cell_size // 2,
                #                         self.start_y + self.cell_size // 2))
                #     pacgum -= 1
                # if x == 0 and y == self.maze_h - 1:
                #     self.screen.blit(self.super_pacgum,
                #         (self.start_x + self.cell_size // 2, self.start_y +
                #          y * self.cell_size + self.cell_size // 2))
                #     pacgum -= 1
                # if x == self.maze_w - 1 and y == self.maze_h - 1:
                #     self.screen.blit(self.super_pacgum,
                #         (self.start_x + x * self.cell_size +
                #          self.cell_size // 2, self.start_y +
                #          y * self.cell_size + self.cell_size // 2))
                #     pacgum -= 1
        return pacgum

    def draw_pacgums(self, pacgum, walls):
        valid_cells = []
        pacgum = self.draw_super_pacgum(pacgum)
        i = 0
        for y in range(self.maze_h):
            for x in range(self.maze_w):
                if walls[y][x]['N'] and walls[y][x]['E'] and walls[y][x][
                        'S'] and walls[y][x]['W']:
                    i += 1
                    continue
                elif x == 0 and y == 0:
                    continue
                elif x == self.maze_w - 1 and y == 0:
                    continue
                elif x == 0 and y == self.maze_h - 1:
                    continue
                elif x == self.maze_w - 1 and y == self.maze_h - 1:
                    continue
                elif i == 13:
                    x += 1
                else:
                    valid_cells.append((x, y))
        print(valid_cells)
        exit(0)
