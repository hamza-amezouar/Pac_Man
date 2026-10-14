from src.models.move_pacman import Pacman_face
from src.models.maze import Maze_screen
import pygame

def redraw_maze(width, height, maze_w, maze_h, screen, walls, pacgum):
        run = True
        direction = None
        maze = Maze_screen(width, height, maze_w, maze_h, screen)
        pacman:Pacman_face = Pacman_face(width, height, maze_w, maze_h, screen)
        pacgums = maze.existing_pacgums(pacgum, walls)
        clock = pygame.time.Clock()
        
        while run:         
            screen.fill((30, 30, 30))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                 exit(0)
            elif keys [pygame.K_UP] or keys[pygame.K_w]:
                direction = "up"
                target = pacman.target_pacman(maze.pacman_pos, direction)
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                direction = "right"
                target = pacman.target_pacman(maze.pacman_pos, direction)
            # elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            #     direction = "down"
            # elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            #     direction = "left"
                
            if (direction and  target) is not None:
                pacman.move_pacman(walls, maze.pacman_pos, direction, target)
                if tuple(maze.pacman_pos) == target:
                    target = pacman.target_pacman(
                    maze.pacman_pos, direction
                )
            
            maze.ft_greed()
            maze.draw_maze(walls)
            maze.draw_all_pacgums(pacgums)
            pacman.draw_face(maze.pacman_pos)            
            clock.tick(20)
            pygame.display.update()
            