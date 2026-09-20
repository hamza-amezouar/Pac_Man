from PIL import Image, ImageSequence
import pygame
def load_gif_frames(gif_path):
    
        git = Image.open(gif_path)
        frames = []
        for frame in ImageSequence.Iterator(git):
            frame_rgba = frame.convert("RGBA")
            pygame_image = pygame.image.fromstring(frame_rgba.tobytes(), frame_rgba.size, "RGBA")
            frames.append(pygame_image)
        return frames