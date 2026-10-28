import pygame
from src.helper_func.draw_pixel import ft_draw_pixel

def ft_draw_line(surface, color, start, end, size):
    s_x, s_y = start
    e_x, e_y = end
    d_x =  abs(e_x - s_x)
    d_y = abs(e_y - s_y)
    step = max (d_x, d_y)

    if step == 0:
        ft_draw_pixel(surface, start, color)
        return
    
    step_x = 1 if s_x <= e_x else -1
    step_y = 1 if s_y <= e_y else -1
    incm_x = step_x * d_x / step
    incm_y = step_y * d_y / step
    current_x = s_x
    current_y = s_y

    for _ in range(step + 1):
        for thick in range(size):
            if d_x >= d_y:
                ft_draw_pixel(surface, (round(current_x), round(current_y + thick)), color)
            elif d_y >= d_x:
                ft_draw_pixel(surface, (round(current_x + thick), round(current_y)), color)
        current_x += incm_x
        current_y += incm_y

   