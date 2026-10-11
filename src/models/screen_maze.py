from src.models.move_pacman import Pacman_face
from src.models.maze import Maze_screen
import pygame
from src.models.ghosts import Ghosts

def redraw_maze(width, height, maze_w, maze_h, screen, walls, pacgum):
        run = True
        maze = Maze_screen(width, height, maze_w, maze_h, screen)
        pacman:Pacman_face = Pacman_face(width, height, maze_w, maze_h, screen)
        ghosts = Ghosts(width, height, maze_w, maze_h, screen, walls)
        maze.draw_pacgums(pacgum, walls)
        step = 10
        while run:    
            screen.fill((30, 30, 30))
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
            ghosts.chase(maze.pacman_pos, step)
            step += 20
            
        
            
            #maze.ft_greed()
            maze.draw_maze(walls)
            pacman.draw_face(maze.pacman_pos)            
            
            pygame.display.update()
            pygame.time.wait(100)