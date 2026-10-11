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
        self.ghost_image = pygame.image.load("assists/images/ghosts/redleft.gif").convert_alpha()
    def chase(self, pacman_pos, step):
        x = self.start_x + step
        y = self.start_y
        self.screen.blit(pygame.transform.scale(self.ghost_image, (40 , 40)), (x, y))