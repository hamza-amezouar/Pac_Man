from src.models.move_pacman import Pacman_face
from src.models.maze import Maze_screen
import pygame

def redraw_maze(width, height, maze_w, maze_h, screen, walls, pacgum):
        run = True
        direction = None
        maze = Maze_screen(width, height, maze_w, maze_h, screen)
        pacman:Pacman_face = Pacman_face(width, height, maze_w, maze_h, screen)
        maze.draw_pacgums(pacgum, walls)
        while run:         
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                 exit(0)
            elif keys [pygame.K_UP] or keys[pygame.K_w]:
                direction = "up"
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                direction = "right"
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                direction = "down"
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                direction = "left"
            if direction:
                old_pos = maze.pacman_pos[:]
                pacman.moves_pacman(walls, maze.pacman_pos, direction)

                if maze.pacman_pos == old_pos:
                    direction = None
            
            screen.fill((30, 30, 30))
            maze.draw_maze(walls)
            pacman.draw_face(maze.pacman_pos)            
            
            pygame.display.update()
            pygame.time.wait(100)