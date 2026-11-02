import pygame
from typing import Tuple, Any


def custom_rect(surface: pygame.surface.Surface, color: Tuple[int, int, int],
                rect_coords: Any) -> None:
    """
    Draw a filled rectangle on a surface.

    Args:
        surface: The surface where the rectangle is drawn.
        color: The RGB color of the rectangle.
        rect_coords: The rectangle position and size. It can be a
            pygame.Rect object or a tuple (x, y, width, height).

    Returns:
        None.
    """

    if isinstance(rect_coords, pygame.Rect):
        x_start = rect_coords.x
        y_start = rect_coords.y
        width = rect_coords.width
        height = rect_coords.height
    else:
        x_start, y_start, width, height = rect_coords
        x_start, y_start, width, height = rect_coords
    x_end = x_start + width
    y_end = y_start + height
    x_start = x_start
    y_start = y_start
    for y in range(y_start, y_end):
        for x in range(x_start, x_end):
            surface.set_at((x, y), color)
