from src.models.move_pacman import Pacman_face
from src.models.maze import Maze, Maze_screen
from src.models.ghosts import Ghosts 
from src.config_parser import Parse
from typing import Tuple, List, Dict, Any, TYPE_CHECKING
import pygame
import time
import json


if TYPE_CHECKING:
    from src.engine.game_engine import Engine

def receive_name_player(width, height, screen:pygame.surface.Surface, engine:"Engine", status:str):
    background_img = pygame.image.load("assists/images/background.png")
    time.sleep(1)
    background_img = pygame.transform.scale(background_img, (width, height))
    gamer_img = pygame.image.load("assists/images/gamer.png")
    gamer_img = pygame.transform.scale(gamer_img, (900, 150))
    high_score = pygame.image.load("assists/images/high_score.png")
    score_img = pygame.transform.scale(high_score, (700, 500))
    name = ""
    n_text = pygame.font.Font("assists/fonts/PixeloidSansBold-1jpBg.ttf",32)
    runing = True
    
    while runing:

        screen.blit(background_img, (0,0))
        screen.blit(gamer_img, (500, 50))
        screen.blit(score_img, (610, 400))

        if status == "game_over":
            msg = "LOSE"
            msg_font = pygame.font.Font("assists/fonts/PixeloidSansBold-1jpBg.ttf", 40)
            msg_text = msg_font.render(msg, True, (255, 0, 0))
            screen.blit(msg_text, (900, 220))
        else:
            msg = "WIN"
            msg_font = pygame.font.Font("assists/fonts/PixeloidSansBold-1jpBg.ttf", 40)
            msg_text = msg_font.render(msg, True, (0, 255, 0))
            screen.blit(msg_text, (910, 250))

        for even in pygame.event.get():
            if even.type == pygame.QUIT:
                exit(0)
            
            if even.type == pygame.KEYDOWN:
                if even.key == pygame.K_RETURN:
                    informal = {name: engine.score}
                    engine.info.append(informal)
                    with open(engine.data["highscore_filename"], "w") as file:
                        json.dump(engine.info, file)
                    runing = False
                
                elif even.key == pygame.K_BACKSPACE:
                    name  = name[:-1]
                elif even.key == pygame.K_SPACE and len(name) < 10:
                    name += " "
                elif even.unicode.isalnum() and len(name) < 10:
                    name += even.unicode

        name_text = n_text.render(name, True, (255, 255, 255))
        new_width = (width - name_text.get_width()) // 2
        screen.blit(name_text, (new_width, height * 0.62))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            exit(0)
        if not runing:
            engine.draw_highscore.draw_high_score()
            return 0
        pygame.display.update()

def game_level(width, height, data:Parse, engine:"Engine", screen:pygame.surface.Surface, l):
        print(l)
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
        ghosts_data['blue']["old_path"] = ghost.calculate_ghost_path(ghosts_data['blue']["pos"], maze.pacman_pos)
        ghosts_data['yellow']["old_path"] = ghost.calculate_ghost_path(ghosts_data['yellow']["pos"], maze.pacman_pos)
        ghosts_data['pink']["old_path"] = ghost.calculate_ghost_path(ghosts_data['pink']["pos"], maze.pacman_pos)
        ghosts_data['red']["old_path"] = ghost.calculate_ghost_path(ghosts_data['red']["pos"], maze.pacman_pos)

        direction = None
        next_direction = None
        current_target = None
        reached = True
        speed = 10
        clock = pygame.time.Clock()
        run = True
        game_over = False
        game_over_img = pygame.image.load("assists/images/game_over.png")
        game_over_img = pygame.transform.scale(game_over_img, (800, 200))
        win_img = pygame.image.load("assists/images/congratulations.png")
        win_img = pygame.transform.scale(win_img, (800, 200))

        
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        return 1
            if not game_over:
                screen.fill((30, 30, 30))
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
                #pacman  
                if not pacgums:
                    return 1
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
                
                if maze.menu_maze(start_ticks):
                    game_over = True
                maze.draw_maze(walls)
                maze.draw_all_pacgums(pacgums)
                pacman.draw_face(maze.pacman_pos, direction)
                maze.eats_pacgums(pacgums)
                # ghosts
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
            else:
                x = maze.start_x + (maze.maze_pixel_w - game_over_img.get_width()) //2
                y = maze.start_y + ((maze.maze_pixel_h - game_over_img.get_height()) // 2) - maze.cell_size
                screen.blit(game_over_img, (x, y))
                pygame.display.update()
                if receive_name_player(width, height, screen,engine,"game_over") == 0:
                    print("enter")
                    return 0
                pygame.display.update()
        return -1
            


def redraw_maze(width, height, data:Parse,engine:"Engine" ,screen:pygame.surface.Surface):
    i = 0
    while i in range(len(data['level'])):
        game =  game_level(width, height, data, engine, screen, i)
        if game == 1:
            i += 1
        if game == 0:
            return 0
    
    # x = maze.start_x + (maze.maze_pixel_w - game_over_img.get_width()) //2
    # y = maze.start_y + ((maze.maze_pixel_h - game_over_img.get_height()) // 2) - maze.cell_size
    # screen.blit(game_over_img, (x, y))
    game_level(width, height, data, engine, screen, i)
    receive_name_player(width, height, screen, engine,"win")
    engine.draw_highscore.draw_high_score()
    return 0
