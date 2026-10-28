
import time

from src.models.move_pacman import Pacman_face
from src.models.maze import Maze, Maze_screen
from src.models.ghosts import Ghosts 
from src.config_parser import Parse
import pygame

def game_level(width, height, data:Parse, engine, screen, l):
        maze_w = data["level"][l]['width']
        maze_h = data["level"][l]['height']
        pacgum = data["level"][l]['pacgum']
        start_ticks = pygame.time.get_ticks()
        seed =  data['seed'] 
        conf_maze = Maze(size=(maze_w, maze_h), seed=seed, level=l + 1)
        walls = conf_maze.get_walls()
        maze = Maze_screen(width, height,maze_w, maze_h, screen, data, engine, l + 1)
        maze.draw_maze(walls)
        pacgums = maze.existing_pacgums(pacgum, walls)
        pacman = Pacman_face(width, height,maze_w, maze_h, screen, data, engine, l + 1)
        ghost = Ghosts(width, height, maze_w, maze_h, screen, walls, data, engine, l + 1)
        ghosts_data = ghost.init_ghosts()

        c_x = int((maze.pacman_pos[0] - maze.start_x) // maze.cell_size)
        c_y = int((maze.pacman_pos[1] - maze.start_y) // maze.cell_size)

        ghosts_data['blue']["old_path"] = ghost.calculate_ghost_path(ghosts_data['blue']["pos"], (c_x, c_y))
        ghosts_data['yellow']["old_path"] = ghost.calculate_ghost_path(ghosts_data['yellow']["pos"], (c_x, c_y))
        ghosts_data['pink']["old_path"] = ghost.calculate_ghost_path(ghosts_data['pink']["pos"], (c_x, c_y))
        ghosts_data['red']["old_path"] = ghost.calculate_ghost_path(ghosts_data['red']["pos"], (c_x, c_y))

        direction = None
        next_direction = None
        current_target = None
        reached = True
        speed = 10
        clock = pygame.time.Clock()
        run = True
        while run:
            screen.fill((30, 30, 30))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        return True

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
                 
            if not pacgums:
                return True
            if reached:
                next_target = None
                if next_direction is not None:
                    next_target = pacman.target_pacman(maze.pacman_pos, next_direction, walls)

                if next_target is not None:
                    direction = next_direction
                    current_target = next_target
                    next_direction = None
            
                elif direction is not None:
                    current_target = pacman.target_pacman(
                                maze.pacman_pos, direction, walls)
                    if current_target is None:
                        direction = "blocked" 
                        next_direction = None
            
                    
            if current_target is not None:
                reached = pacman.move_pacman(maze.pacman_pos, current_target, speed)
                if reached:
                    current_target = None
            else:
                reached = True
            
            maze.draw_maze(walls)
            maze.menu_maze(start_ticks)
            maze.draw_all_pacgums(pacgums)
            pacman.draw_face(maze.pacman_pos, direction)
            maze.eats_pacgums(pacgums)
            for specter in ghosts_data.values():
                old_path = specter["old_path"]
                if specter["current_pos"] + 1 < len(old_path):
                    start_cell = old_path[specter["current_pos"]]
                    target_cell = old_path[specter["current_pos"] + 1]
                else:
                    start_cell = old_path[-1]
                    target_cell = old_path[-1]
                pacman_pos = ghost.ghosts_brain(specter, direction, maze.pacman_pos)
                
                ghost.is_eat_super_pacgums(maze.pacman_pos)

                if ghost.Scared_Mode:
                    ghost.scard(start_cell, target_cell, specter["total_speed"], specter, start_eat)
                    if specter["move_now"] >= specter["total_speed"]:
                        specter["move_now"] = 0
                        specter["current_frame"] += 1
                        if specter["current_pos"] + 1 < len(old_path):
                            ghost_reached_cell = old_path[specter["current_pos"] + 1]
                        else:
                            ghost_reached_cell = old_path[-1]
                        new_path = ghost.calculate_ghost_path(ghost_reached_cell, specter["my_pos"])
                        specter["old_path"] = new_path

                else:

                    if ghost.is_caught(ghosts_data, maze.pacman_pos):
                        print("Game Over11")
                    ghost.chase(start_cell, target_cell, specter["total_speed"], specter)

                    if specter["move_now"] >= specter["total_speed"]:
                        c_x = int((maze.pacman_pos[0] - maze.start_x) // maze.cell_size)
                        c_y = int((maze.pacman_pos[1] - maze.start_y) // maze.cell_size)
                        specter["move_now"] = 0
                        specter["current_frame"] += 1
                        if specter["current_pos"] + 1 < len(old_path):
                            ghost_reached_cell = old_path[specter["current_pos"] + 1]
                        else:
                            ghost_reached_cell = old_path[-1]
                        print(f"pacman pos == {pacman_pos}")
                        new_path = ghost.calculate_ghost_path(ghost_reached_cell, pacman_pos)
                        specter["old_path"] = new_path
                    start_eat = pygame.time.get_ticks()

                specter["move_now"] += 2
            clock.tick(60)
            pygame.display.update()

        


def redraw_maze(width, height, data:Parse,engine ,screen):
    for i in range(len(data['level'])):
        game_level(width, height, data, engine, screen, i)
    print("game over")
    exit(0)