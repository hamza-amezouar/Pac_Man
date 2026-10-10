from src.models.move_pacman import Pacman_face
from src.models.maze import Maze_screen
import pygame

def redraw_maze(width, height, maze_w, maze_h, screen, walls, pacgum):
        run = True
        maze = Maze_screen(width, height, maze_w, maze_h, screen)
        pacman:Pacman_face = Pacman_face(width, height, maze_w, maze_h, screen)
        screen.fill((30, 30, 30))
        maze.draw_pacgums(pacgum, walls)
        while run:         
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                 exit(0)
            elif keys[pygame.K_UP] or keys[pygame.K_w]:
                 pacman.moves_pacman(maze.pacman_pos, "up")
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                pass
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                pass
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                pass
            
        
            
            #maze.ft_greed()
            maze.draw_maze(walls)
            pacman.draw_face(maze.pacman_pos)            
            
            pygame.display.update()
            pygame.time.wait(100)