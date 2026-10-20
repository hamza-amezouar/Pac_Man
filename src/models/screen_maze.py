
from src.models.move_pacman import Pacman_face
from src.models.maze import Maze, Maze_screen
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
        direction = None
        next_direction = None
        current_target = None
        reached = True
        speed = 5
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
            
            #maze.ft_greed()
            maze.draw_maze(walls)
            maze.menu_maze(start_ticks)
            maze.draw_all_pacgums(pacgums)
            pacman.draw_face(maze.pacman_pos, direction)
            maze.eats_pacgums(pacgums)
            clock.tick(60)
            pygame.display.update()

        


def redraw_maze(width, height, data:Parse,engine ,screen):
    for i in range(len(data['level'])):
        game_level(width, height, data, engine, screen, i)
    print("game over")
    exit(0)