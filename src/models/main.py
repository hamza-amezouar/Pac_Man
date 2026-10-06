from typing import List, Dict
from src.models.move_pacman import Pacman_face
from src.models.maze import Screen
import pygame

def redraw_game(screen:Screen, walls:List[List[Dict[str, bool]]], pacman: Pacman_face) -> None:
    screen.ft_greed()
    screen.draw_maze(walls)
    pacman.draw_face(screen.pacman_pos)
    pygame.display.update()
    

def maze_loop(screen:Screen, walls: List[List[Dict[str, bool]]], pacman) -> None:
        screen.screen.fill((30, 30, 30))
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   run = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                run = False
            redraw_game(screen, walls, pacman)
        pygame.quit()

