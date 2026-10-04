from PIL import Image, ImageSequence
import pygame


def load_gif_frames(gif_path: str) -> list[pygame.surface.Surface]:
    """Extracts and converts frames
    from an animated GIF into Pygame surfaces.

    Args:
        gif_path (str):
        The file path to the animated GIF image.

    Returns:
        list[pygame.surface.Surface]:
        A list of Pygame Surface objects representing each frame of the GIF.
    """
    git = Image.open(gif_path)
    frames = []
    for frame in ImageSequence.Iterator(git):
        frame_rgba = frame.convert("RGBA")
        pygame_image = pygame.image.fromstring(frame_rgba.tobytes(),
                                               frame_rgba.size, "RGBA")
        frames.append(pygame_image)
    return frames
