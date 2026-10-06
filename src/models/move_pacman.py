from PIL import Image, ImageSequence
import pygame
from src.models.maze import Screen


def load_gif_frames(gif_path: str):

    git = Image.open(gif_path)
    frames = []
    for frame in ImageSequence.Iterator(git):
        frame_rgba = frame.convert("RGBA")
        pygame_image = pygame.image.fromstring(frame_rgba.tobytes(),
                                               frame_rgba.size, "RGBA")
        frames.append(pygame_image)
    return frames


class Pacman_face(Screen):

    def __init__(self, maze_w, maze_h):
        super().__init__(maze_w, maze_h)

    pacman_up = load_gif_frames("src/models/pacman_face/right.gif")
    pacman_down = load_gif_frames("src/models/pacman_face/down.gif")
    pacman_left = load_gif_frames("src/models/pacman_face/left.gif")
    pacman_right = load_gif_frames("src/models/pacman_face/right.gif")

    def draw_face(self, pacman_pos):
        pacman_size =  self.cell_size - 15
        pacman_image = pygame.transform.scale(self.pacman_right[0],
                                              (pacman_size , pacman_size))
        self.screen.blit(pacman_image, (pacman_pos[0] - 18, pacman_pos[1] - 10))
