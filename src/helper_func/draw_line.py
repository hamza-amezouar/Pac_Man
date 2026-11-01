from src.helper_func.draw_pixel import ft_draw_pixel
from typing import Tuple
import pygame


def ft_draw_line(surface: pygame.surface.Surface, color: Tuple[int, int, int],
                 start: Tuple[int, int], end: Tuple[int,
                                                    int], size: int) -> None:
    """
    Draw a line between two points on a surface.

    Args:
        surface: The surface where the line is drawn.
        color: The RGB color of the line.
        start: The starting point of the line.
        end: The ending point of the line.
        size: The thickness of the line.

    Returns:
        None.
    """
    s_x, s_y = start
    e_x, e_y = end
    d_x = abs(e_x - s_x)
    d_y = abs(e_y - s_y)
    step = max(d_x, d_y)

    if step == 0:
        ft_draw_pixel(surface, start, color)
        return

    step_x = 1 if s_x <= e_x else -1
    step_y = 1 if s_y <= e_y else -1
    incm_x = step_x * d_x / step
    incm_y = step_y * d_y / step
    current_x: float = float(s_x)
    current_y: float = float(s_y)

    for _ in range(step + 1):
        for thick in range(size):
            if d_x >= d_y:
                ft_draw_pixel(surface,
                              (round(current_x), round(current_y + thick)),
                              color)
            elif d_y >= d_x:
                ft_draw_pixel(surface,
                              (round(current_x + thick), round(current_y)),
                              color)
        current_x += incm_x
        current_y += incm_y
