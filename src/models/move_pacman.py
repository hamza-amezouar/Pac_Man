from src.engine.load_gifs import load_gif_frames
from src.models.maze import Maze_screen
import pygame


class Pacman_face(Maze_screen):

    def __init__(self, screen_w, screen_h, maze_w, maze_h, screen):
        super().__init__(screen_w, screen_h, maze_w, maze_h, screen)

    pacman_up = load_gif_frames("src/models/pacman_face/pacman/down.gif")
    pacman_down = load_gif_frames("src/models/pacman_face/pacman/down.gif")
    pacman_left = load_gif_frames("src/models/pacman_face/pacman/left.gif")
    pacman_right = load_gif_frames("src/models/pacman_face/pacman/right.gif")

    def draw_face(self, pacman_pos):
        pacman_size =  self.cell_size - 15
        pacman_image = pygame.transform.scale(self.pacman_right[0],
                                              (pacman_size , pacman_size))
        self.screen.blit(pacman_image, (pacman_pos[0] - 18, pacman_pos[1] - 18))
