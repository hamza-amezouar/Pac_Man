import pygame

def custom_rect(surface, color, rect_coords):
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