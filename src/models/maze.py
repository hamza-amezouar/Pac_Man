from mazegenerator.mazegenerator import MazeGenerator
import time
from src.config_parser import Parse
from typing import List
import pygame


class Maze(MazeGenerator):

    def __init__(self, size=(15, 15), perfect=False, seed=0, level=1) -> None:
        self._level = level
        if level != 1:
            seed = 0
        super().__init__(size=size, perfect=perfect, seed=seed)

    def get_walls(self):
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
    def get_width(self):
        return self._width

    @property
    def get_height(self):
        return self._height

    @property
    def get_42(self):
        return self._add_42_to_maze()


class Screen:

    def ft_greed(self):
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, (255, 0, 255), (x, 0),
                             (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, (255, 0, 255), (0, y),
                             (self.width, y))

    def __init__(self, maze_w, maze_h):
        pygame.init()
        info = pygame.display.Info()
        self.width = info.current_w
        self.height = info.current_h

        self.maze_w = maze_w
        self.maze_h = maze_h

        self.screen = pygame.display.set_mode((self.width, self.height))

        padding_x = 50
        padding_y = 150

        available_width = self.width - (2 * padding_x)
        available_height = self.height - (2 * padding_y)

        self.cell_size = min(available_width // self.maze_w,
                             available_height // self.maze_h)

        self.maze_pixel_w = self.maze_w * self.cell_size
        self.maze_pixel_h = self.maze_h * self.cell_size

    def draw_maze(self, walls):

        start_x = (self.width - self.maze_pixel_w) // 2
        start_y = (self.height - self.maze_pixel_h) // 2

        # top wall
        pygame.draw.line(self.screen, (2, 255, 200), (start_x, start_y),
                         (start_x + self.maze_pixel_w, start_y), 5)
        # left wall
        pygame.draw.line(self.screen, (2, 255, 200), (start_x, start_y),
                         (start_x, start_y + self.maze_pixel_h), 5)

        for y in range(self.maze_h):
            for x in range(self.maze_w):
                cell_x = start_x + x * self.cell_size
                cell_y = start_y + y * self.cell_size
                  # 42 background

                if walls[y][x]['N'] and walls[y][x]['E'] and walls[y][x]['S'] and walls[y][x]['W']:
                    pygame.draw.line(self.screen, (255, 100, 100), (cell_x, cell_y + self.cell_size / 2), 
                                     (cell_x + self.cell_size, cell_y + self.cell_size / 2),self.cell_size)
                
                if walls[y][x]['E']:
                    pygame.draw.line(self.screen, (2, 255, 200), (cell_x + self.cell_size, cell_y),
                                     (cell_x + self.cell_size, cell_y + self.cell_size), 5)
                if walls[y][x]['S']:
                    pygame.draw.line(self.screen, (2, 255, 200), (cell_x, cell_y + self.cell_size),
                                     (cell_x + self.cell_size, cell_y + self.cell_size), 5)
                    
    def maze_loop(self, walls):
        self.screen.fill((30, 30, 30))
        run = True
        while run:
            self.screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                pygame.quit()
            self.ft_greed()
            self.draw_maze(walls)
            pygame.display.update()


parse = Parse()
data = parse.get_data()
width = data['level'][0]['width']
height = data['level'][0]['height']
d_seed = data['seed']

maze1 = Maze(size=(20, 20), seed=55, level=1)
walls = maze1.get_walls()
# print(maze1.get_42)

screen = Screen(20, 20)
screen.maze_loop(walls)

