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

    def draw_face(self):
        pacman_size =  self.cell_size - 20
        pacman_image = pygame.transform.scale(self.pacman_right[0],
                                              (pacman_size , pacman_size))
        center_x = self.start_x + self.maze_pixel_w // 2
        center_y = self.start_y + self.maze_pixel_h // 2

        pacman_x = center_x - pacman_size // 2
        pacman_y = center_y - pacman_size // 2
        
        width_image = ((self.width - self.maze_pixel_w) // 2) + ((self.maze_w // 2) * self.cell_size + 6) + self.cell_size
        height_image = (self.height - self.maze_pixel_h) // 2  + ((self.maze_h // 2) * self.cell_size + 5) 
        self.screen.blit(pacman_image, (pacman_x, pacman_y))
