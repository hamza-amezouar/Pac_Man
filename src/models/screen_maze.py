
import random
import time

from src.models.move_pacman import Pacman_face
from src.models.maze import Maze_screen
import pygame
from src.models.ghosts import Ghosts


def redraw_maze(width, height, maze_w, maze_h, screen, walls, pacgum):
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

    speed = 3
    clock = pygame.time.Clock()
    ghost = Ghosts(width, height, maze_w, maze_h, screen, walls)
    current_pos = 0
    move_now = 1
    maze.draw_maze(walls)
    ghosts_data = ghost.init_ghosts()
    ghosts_data['blue']["old_path"] = ghost.calculate_ghost_path(ghosts_data['blue']["pos"], maze.pacman_pos)
    ghosts_data['yellow']["old_path"] = ghost.calculate_ghost_path(ghosts_data['yellow']["pos"], maze.pacman_pos)
    ghosts_data['pink']["old_path"] = ghost.calculate_ghost_path(ghosts_data['pink']["pos"], maze.pacman_pos)
    ghosts_data['red']["old_path"] = ghost.calculate_ghost_path(ghosts_data['red']["pos"], maze.pacman_pos)
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

        # maze.ft_greed()
        maze.draw_maze(walls)
        maze.draw_all_pacgums(pacgums)
        pacman.draw_face(maze.pacman_pos, direction)
        for specter in ghosts_data.values():
            old_path = specter["old_path"]
            if specter["current_pos"] + 1 < len(old_path):
                start_cell = old_path[specter["current_pos"]]
                target_cell = old_path[specter["current_pos"] + 1]
            else:
                start_cell = old_path[-1]
                target_cell = old_path[-1]
            pacman_pos = ghost.ghosts_brain(specter, direction, maze.pacman_pos, ghosts_data["red"]["pos"])
            ghost.chase(start_cell, target_cell, specter["total_speed"], specter)
            specter["move_now"] += 2
            if specter["move_now"] >= specter["total_speed"]:
                x = int((pacman_pos[0] - maze.start_x) // maze.cell_size)
                y = int((pacman_pos[1] - maze.start_y) // maze.cell_size)
                if target_cell == (x, y):
                    print("game over")
                    exit()
                specter["move_now"] = 0
                specter["current_frame"] += 1
                if specter["current_pos"] + 1 < len(old_path):
                    ghost_reached_cell = old_path[specter["current_pos"] + 1]
                else:
                    ghost_reached_cell = old_path[-1]
                new_path = ghost.calculate_ghost_path(ghost_reached_cell, pacman_pos)
                specter["old_path"] = new_path
                specter["current_pos"] = 0
        clock.tick(60)
        pygame.display.update()
