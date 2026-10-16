import time

import pygame

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
        self.current_pos = -1
        self.ghost_image = pygame.image.load("assists/images/ghosts/redleft.gif").convert_alpha()
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
        while pos != current_pos:
            path.append(pos)
            pos = parrent[pos]
        path.append(current_pos)
        return path[::-1]
        

    def chase(self, current_pos):
        x = current_pos[0]
        y = current_pos[1]
        size = self.cell_size - 10
        pixel_x = self.start_x + (x * self.cell_size) + self.cell_size // 2
        pixel_y = self.start_y + (y * self.cell_size) + self.cell_size // 2
        self.screen.blit(pygame.transform.scale(self.ghost_image, (size , size)), (pixel_x - size // 2, pixel_y - size // 2))