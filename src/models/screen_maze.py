from src.models.move_pacman import Pacman_face
from src.models.maze import Maze_screen

import pygame

def redraw_maze(width, height, maze_w, maze_h, screen, walls, pacgum):
        run = True
        maze = Maze_screen(width, height, maze_w, maze_h, screen)
        pacman = Pacman_face(width, height, maze_w, maze_h, screen)
        screen.fill((30, 30, 30))
        while run:         
            
            
            #maze.ft_greed()
            maze.draw_maze(walls)
            #maze. draw_super_pacgum(pacgum)
            # maze.draw_pacgums(pacgum, walls)
            pacman.draw_face(maze.pacman_pos)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                 exit(0)
            
            
            pygame.display.update()
            pygame.time.wait(100)