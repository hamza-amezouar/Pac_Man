import pygame
from typing import Tuple


def ft_draw_pixel(surface: pygame.surface.Surface, pos: Tuple[int, int],
                  color: Tuple[int, int, int]) -> None:
    """
    Draw one pixel on a surface.

    Args:
        surface: The surface where the pixel is drawn.
        pos: The position of the pixel (x, y).
        color: The RGB color of the pixel.

    Returns:
        None.
    """
    surface.set_at(pos, color)
