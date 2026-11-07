from src.models.move_pacman import Pacman_face
from src.models.maze import Maze, Maze_screen
from src.models.ghosts import Ghosts
from src.helper_func.draw_rect import custom_rect
from typing import Tuple, Dict, Any, TYPE_CHECKING
import pygame
import time
import json
import sys

if TYPE_CHECKING:
    from src.engine.game_engine import Engine


def pause_menu(width: int, height: int, screen: pygame.surface.Surface) -> int:
    """
    Display the pause menu and handle button clicks.

    Args:
        width: The width of the game screen.
        height: The height of the game screen.
        screen: The Pygame surface used to draw the menu.

    Returns:
        1 if the player selects Play.
        2 if the player selects Menu.
        0 if the player selects Quit.
        3 if the menu loop ends.
    """

    pause_img = pygame.image.load("assists/images/pause_img.jpeg")
    pause_img = pygame.transform.scale(pause_img, (400, 450))
    x = int(width * 0.40)
    y = int(height * 0.30)
    screen.blit(pause_img, (x, y))
    b_x = int(width * 0.46)
    b_y = int(height * 0.47)
    padding = 0
    run = True
    normal_font = pygame.font.Font("assists/fonts/ka1.ttf", 30)
    hover_font = pygame.font.Font("assists/fonts/PixeloidSansBold-1jpBg.ttf",
                                  30)
    for b in range(3):

        custom_rect(screen, (255, 255, 255), (b_x, (b_y + padding), 170, 50))
        custom_rect(screen, (223, 124, 0),
                    (b_x + 5, (b_y + padding) + 5, 160, 40))

        if b == 0:
            play_button = pygame.Rect((b_x, (b_y + padding), 170, 50))
        elif b == 1:
            menu_button = pygame.Rect((b_x, (b_y + padding), 170, 50))
        else:
            quit_button = pygame.Rect((b_x, (b_y + padding), 170, 50))
        padding += 70

    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if play_button.collidepoint(event.pos):
                        return 1
                    elif menu_button.collidepoint(event.pos):
                        return 2
                    elif quit_button.collidepoint(event.pos):
                        return 0

        buttons = [(play_button, "PLAY"), (menu_button, "MENU"),
                   (quit_button, "QUIT")]

        mouse_pos = pygame.mouse.get_pos()
        for button, msg in buttons:
            custom_rect(screen, (223, 124, 0),
                        (button.x + 5, button.y + 5, 160, 40))
            if button.collidepoint(mouse_pos):
                msg_surface = hover_font.render(msg, True, (25, 25, 166))
            else:
                msg_surface = normal_font.render(msg, True, (25, 25, 166))
            text_center = msg_surface.get_rect(center=button.center)
            screen.blit(msg_surface, text_center)

        pygame.display.update()
    return 3


def receive_name_player(width: int, height: int,
                        screen: pygame.surface.Surface, engine: "Engine",
                        status: str) -> int:
    """
    Ask the player for their name and save their score.

    Args:
        width: The width of the game screen.
        height: The height of the game screen.
        screen: The Pygame surface used to draw the screen.
        engine: The game engine instance.
        status: The game result, either game_over or win.

    Returns:
        0 after saving the player's name and score.
        1 if the name entry loop ends without saving.
    """
    time.sleep(1)
    background_img = pygame.image.load("assists/images/background.png")
    background_img = pygame.transform.scale(background_img, (width, height))
    gamer_img = pygame.image.load("assists/images/gamer.png")
    gamer_img = pygame.transform.scale(gamer_img, (900, 150))
    high_score = pygame.image.load("assists/images/high_score.png")
    score_img = pygame.transform.scale(high_score, (700, 500))
    name = ""
    n_text = pygame.font.Font("assists/fonts/AgentOrange.ttf", 32)
    score_font = pygame.font.Font("./assists/fonts/ka1.ttf", 20)
    score_text = score_font.render(f"{str(engine.score)} PTS", True,
                                   (255, 255, 255))
    lose_font = pygame.font.Font("assists/fonts/PixeloidSansBold-1jpBg.ttf",
                                 40)
    win_font = pygame.font.Font("assists/fonts/PixeloidSansBold-1jpBg.ttf", 40)
    runing = True
    while runing:

        screen.blit(background_img, (0, 0))
        screen.blit(gamer_img, (500, 50))
        screen.blit(score_img, (610, 400))
        screen.blit(score_text, (width * 0.48, height * 0.58))
        score_img

        if status == "game_over":
            msg = "LOSE"
            msg_text = lose_font.render(msg, True, (255, 0, 0))
            screen.blit(msg_text, (900, 220))
        else:
            msg = "WIN"
            msg_text = win_font.render(msg, True, (0, 255, 0))

            screen.blit(msg_text, (910, 250))

        for even in pygame.event.get():
            if even.type == pygame.QUIT:
                sys.exit(0)

            if even.type == pygame.KEYDOWN:
                if even.key == pygame.K_RETURN:
                    informal = {name: engine.score}
                    engine.info.append(informal)
                    runing = False

                elif even.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif even.key == pygame.K_SPACE and len(name) < 10:
                    name += " "
                elif even.unicode.isalnum() and len(name) < 10:
                    name += even.unicode
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            sys.exit(0)

        name_text = n_text.render(name, True, (255, 255, 255))
        new_width = (width - name_text.get_width()) // 2
        screen.blit(name_text, (new_width, height * 0.62))
        if not runing:
            engine.info = sorted(
                engine.info,
                reverse=True,
                key=lambda player: list(player.values())[0])[:10]
            with open(engine.data["highscore_filename"], "w") as file:
                json.dump(engine.info, file, indent=2)
                engine.draw_highscore.draw_high_score(engine.info)
            return 0
        pygame.display.update()
    return 1


def game_level(width: int, height: int, data: Dict[str, Any], engine: "Engine",
               screen: pygame.surface.Surface, level: int) -> int:
    """
    Run one game level and manage Pac-Man, ghosts, and game events.

    Args:
        width: The width of the game screen.
        height: The height of the game screen.
        data: The game configuration data.
        engine: The game engine instance.
        screen: The Pygame surface used to draw the game.
        level: The index of the current level.

    Returns:
        1 if the player completes the level.
        0 if the player returns to the menu or the game ends.
       -1 if the game loop ends.
    """

    maze_w = data["level"][level]['width']
    maze_h = data["level"][level]['height']
    pacgum = data["level"][level]['pacgum']
    seed = data['seed']
    conf_maze = Maze(size=(maze_w, maze_h), seed=seed, level=level + 1)
    walls = conf_maze.get_walls()
    maze = Maze_screen(width, height, maze_w, maze_h, screen, data, engine,
                       level + 1)
    maze.draw_maze(walls)
    pacgums = maze.existing_pacgums(pacgum, walls)
    pacman = Pacman_face(width, height, maze_w, maze_h, screen, data, engine,
                         level + 1)
    ghost = Ghosts(width, height, maze_w, maze_h, screen, walls, data, engine,
                   level + 1)
    ghosts_data = ghost.init_ghosts()
    c_x = int((maze.pacman_pos[0] - maze.start_x) // maze.cell_size)
    c_y = int((maze.pacman_pos[1] - maze.start_y) // maze.cell_size)

    ghosts_data['blue']["old_path"] = ghost.calculate_ghost_path(
        ghosts_data['blue']["pos"], (c_x, c_y))
    ghosts_data['yellow']["old_path"] = ghost.calculate_ghost_path(
        ghosts_data['yellow']["pos"], (c_x, c_y))
    ghosts_data['pink']["old_path"] = ghost.calculate_ghost_path(
        ghosts_data['pink']["pos"], (c_x, c_y))
    ghosts_data['red']["old_path"] = ghost.calculate_ghost_path(
        ghosts_data['red']["pos"], (c_x, c_y))

    game_over_img = pygame.image.load("assists/images/game_over.png")
    game_over_img = pygame.transform.scale(game_over_img, (800, 200))
    win_img = pygame.image.load("assists/images/win.png")
    win_img = pygame.transform.scale(win_img, (800, 200))

    background_img = pygame.image.load("assists/images/bg_maze.png")

    background_img = pygame.transform.scale(background_img, (width, height))

    direction = None
    next_direction = None
    current_target = None
    reached = True
    speed = 10
    run = True
    game_over = False
    game_pause = False
    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()
    time_pause = 0

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in engine.draw_highscore.buttons:
                        if button.collidepoint(event.pos):
                            return 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if level == len(data['level']) - 1:
                        x = maze.start_x + (maze.maze_pixel_w -
                                            game_over_img.get_width()) // 2
                        y = maze.start_y + (
                            (maze.maze_pixel_h - game_over_img.get_height()) //
                            2) - maze.cell_size
                        screen.blit(win_img, (x, y))
                        pygame.display.update()
                    return 1
                if event.key == pygame.K_SPACE and not game_pause:
                    time_pause = pygame.time.get_ticks() - start_ticks
                    game_pause = True
                    pause = pause_menu(width, height, screen)
                    if pause == 0:
                        sys.exit(0)
                    if pause == 1 and game_pause:
                        start_ticks = pygame.time.get_ticks() - time_pause
                        game_pause = False
                    if pause == 2:
                        return 0
        if game_pause:
            clock.tick(60)
            continue
        else:
            if not game_over:
                screen.blit(background_img, (0, 0))
                mouse_pos: Tuple = pygame.mouse.get_pos()

                engine.draw_highscore.draw_back_button(mouse_pos,
                                                       "BACK TO HOME")

                keys = pygame.key.get_pressed()
                if keys[pygame.K_q]:
                    sys.exit(0)
                elif keys[pygame.K_UP] or keys[pygame.K_w]:
                    next_direction = "up"
                elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    next_direction = "down"
                elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    next_direction = "right"
                elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    next_direction = "left"
                # pacman
                if not pacgums:
                    time.sleep(1)
                    if level == len(data['level']) - 1:
                        x = maze.start_x + (maze.maze_pixel_w -
                                            game_over_img.get_width()) // 2
                        y = maze.start_y + (
                            (maze.maze_pixel_h - game_over_img.get_height()) //
                            2) - maze.cell_size
                        screen.blit(win_img, (x, y))
                        pygame.display.update()
                    return 1
                if reached:
                    next_target = None
                    if next_direction is not None:
                        next_target = pacman.target_pacman(
                            maze.pacman_pos, next_direction, walls)

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
                    reached = pacman.move_pacman(maze.pacman_pos,
                                                 current_target, speed)
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
                # ghost
                c_x = int(
                    (maze.pacman_pos[0] - maze.start_x) // maze.cell_size)
                c_y = int(
                    (maze.pacman_pos[1] - maze.start_y) // maze.cell_size)

                for specter in ghosts_data.values():
                    old_path = specter["old_path"]
                    if specter["current_pos"] + 1 < len(old_path):
                        start_cell = old_path[specter["current_pos"]]
                        target_cell = old_path[specter["current_pos"] + 1]
                    else:
                        start_cell = old_path[-1]
                        target_cell = old_path[-1]
                    pacman_pos = ghost.ghosts_brain(specter, direction,
                                                    maze.pacman_pos)
                    if ghost.is_eat_super_pacgums(maze.pacman_pos):
                        ghost.Scared_Mode = True
                        for g in ghosts_data.keys():
                            ghosts_data[g]["add_score"] = False
                            ghosts_data[g]["remain"] = False
                            ghosts_data[g]["scared_pos"] = None
                        start_eat = pygame.time.get_ticks()
                    if ghost.Scared_Mode:
                        ghost.was_eaten_ghosts(ghosts_data, maze.pacman_pos,
                                               engine)
                        ghost.scared(start_cell, target_cell,
                                     specter["total_speed"], specter,
                                     start_eat)

                        ghost.create_random_path(maze.pacman_pos, specter)
                        if specter["move_now"] >= specter["total_speed"]:
                            specter["move_now"] = 0
                            specter["current_frame"] += 1
                            if specter["current_pos"] + 1 < len(old_path):
                                ghost_reached_cell = \
                                    old_path[specter["current_pos"] + 1]
                            else:
                                ghost_reached_cell = old_path[-1]
                            if specter["was_eaten"]:
                                new_path = ghost.calculate_ghost_path(
                                    ghost_reached_cell, specter["my_pos"])
                            else:
                                new_path = ghost.calculate_ghost_path(
                                    ghost_reached_cell, specter["scared_pos"])
                            specter["old_path"] = new_path
                    else:
                        specter["was_eaten"] = False
                        specter["remain"] = False
                        specter["add_score"] = False
                        ghost.chase(start_cell, target_cell,
                                    specter["total_speed"], specter)
                        if ghost.is_caught(ghosts_data, maze.pacman_pos):
                            engine.lives -= 1
                            if engine.lives < 0:
                                game_over = True
                            else:
                                return 2
                        if specter["move_now"] >= specter["total_speed"]:
                            if specter["remain"]:
                                specter["remain"] = False
                            specter["move_now"] = 0
                            specter["current_frame"] += 1
                            if specter["current_pos"] + 1 < len(old_path):
                                ghost_reached_cell = \
                                    old_path[specter["current_pos"] + 1]
                            else:
                                ghost_reached_cell = old_path[-1]
                            new_path = ghost.calculate_ghost_path(
                                ghost_reached_cell, pacman_pos)
                            specter["old_path"] = new_path
                    specter["move_now"] += 2

                clock.tick(60)
                pygame.display.update()
            else:
                # game over
                x = maze.start_x + (maze.maze_pixel_w -
                                    game_over_img.get_width()) // 2
                y = maze.start_y + (
                    (maze.maze_pixel_h - game_over_img.get_height()) //
                    2) - maze.cell_size
                screen.blit(game_over_img, (x, y))
                pygame.display.update()
                if receive_name_player(width, height, screen, engine,
                                       "game_over") == 0:
                    return 0
                clock.tick(60)
                pygame.display.update()
    return -1


def redraw_maze(width: int, height: int, data: Dict[str, Any],
                engine: "Engine", screen: pygame.surface.Surface) -> int:
    """
    Manage all game levels and show the final high scores.

    Args:
        width: The width of the game screen.
        height: The height of the game screen.
        data: The game configuration data.
        engine: The game engine instance.
        screen: The Pygame surface used to draw the game.

    Returns:
        0 when the game returns to the menu or finishes.
    """
    i = 0
    while i in range(len(data['level']) - 1):
        game = game_level(width, height, data, engine, screen, i)
        if game == 1:
            i += 1
        if game == 0:
            return 0
        if game == 2:
            game_level(width, height, data, engine, screen, i)
    game_level(width, height, data, engine, screen, i)
    receive_name_player(width, height, screen, engine, "win")
    engine.draw_highscore.draw_high_score(engine.info)
    return 0
