
from src.models.move_pacman import Pacman_face
from src.models.maze import Maze_screen
import pygame


def redraw_maze(width, height, maze_w, maze_h, screen, walls, pacgum):
<<<<<<< HEAD
    run = True
    maze = Maze_screen(width, height, maze_w, maze_h, screen)
    pacman: Pacman_face = Pacman_face(
        width, height, maze_w, maze_h, screen
    )
    pacgums = maze.existing_pacgums(pacgum, walls)

    direction = None
    next_direction = None
    current_target = None
    reached = True

    speed = 2
    clock = pygame.time.Clock()

    while run:
        screen.fill((30, 30, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_q]:
            exit(0)
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            next_direction = "up"
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            next_direction = "down"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            next_direction = "right"
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            next_direction = "left"

        # 1. Choose a new target only when the previous target is reached
        if reached:
            next_target = None

            # Try the direction requested by the player
            if next_direction is not None:
                next_target = pacman.target_pacman(
                    maze.pacman_pos, next_direction, walls
                )

            # If that direction is open, choose it
            if next_target is not None:
                direction = next_direction
                current_target = next_target
                next_direction = None

            # Otherwise, continue in the current direction
            elif direction is not None:
                current_target = pacman.target_pacman(
                    maze.pacman_pos, direction, walls
                )

        # 2. Move toward the saved current target
        if current_target is not None:
            reached = pacman.move_pacman(
                maze.pacman_pos, current_target, speed
            )

            if reached:
                current_target = None

        maze.ft_greed()
        maze.draw_maze(walls)
        maze.draw_all_pacgums(pacgums)
        pacman.draw_face(maze.pacman_pos, direction)

        clock.tick(60)
        pygame.display.update()
=======
        run = True
        maze = Maze_screen(width, height, maze_w, maze_h, screen)
        pacman:Pacman_face = Pacman_face(width, height, maze_w, maze_h, screen)
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
            step += 20
            
        
            
            # maze.ft_greed()
            maze.draw_maze(walls)
            pacman.draw_face(maze.pacman_pos)            
            
            pygame.display.update()
            pygame.time.wait(100)
>>>>>>> 89b18d94fdae4cb778343c049f8477284b7015e4
