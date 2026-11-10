from src.models.move_pacman import Pacman_face
from src.models.maze import Maze, Maze_screen
from src.models.ghosts import Ghosts
from src.helper_func.draw_rect import custom_rect
from typing import List, Tuple, Dict, Any, TYPE_CHECKING
import pygame
import time
import json
import sys

if TYPE_CHECKING:
    from src.engine.game_engine import Engine


class Update_game():
    """
    Manage the Pac-Man game state, gameplay mechanics, and level progression.

    Initialize and coordinate the maze, Pac-Man, and ghosts. Handle player
    input, movement, collisions, scoring, lives, pause menus, cheat modes,
    high scores, and transitions between game levels.
    """

    def __init__(self, width: int, height: int, data: Dict[str, Any],
                 engine: "Engine", screen: pygame.surface.Surface) -> None:
        """
        Initialize the game manager and its initial configuration.

        Args:
            width (int): Width of the game window.
            height (int): Height of the game window.
            data (Dict[str, Any]): Game configuration and level settings.
            engine (Engine): Main game engine instance.
            screen (pygame.surface.Surface): Surface used to display the game.
        """
        self.width = width
        self.height = height
        self.data = data
        self.engine = engine
        self.screen = screen
        self.time = self.data["level_max_time"]
        self.lives = self.data["lives"]
        self.score = 0
        self.is_invincibile = False
        self.cheat_time = False
        self.real_time = self.data["level_max_time"]
        self.total_pacgums: List[List[Tuple[int, int]]] = []

    def set_objects(self, level: int) -> None:
        """
        Initialize the maze, Pac-Man, and ghosts for the specified level.

        Generate the maze, retrieve its walls, initialize the game objects,
        and calculate the initial paths for all ghosts toward Pac-Man.

        Args:
            level (int): Zero-based index of the current level.

        Returns:
            None.
        """

        maze_w = self.data["level"][level]['width']
        maze_h = self.data["level"][level]['height']
        seed = self.data['seed']
        self.conf_maze = Maze(size=(maze_w, maze_h),
                              seed=seed,
                              level=level + 1)
        self.walls = self.conf_maze.get_walls()
        self.maze = Maze_screen(self.width, self.height, maze_w, maze_h,
                                self.screen, self.data, self, level + 1)
        self.maze.draw_maze(self.walls)
        self.pacman = Pacman_face(self.width, self.height, maze_w, maze_h,
                                  self.screen, self.data, self, level + 1)
        self.ghost = Ghosts(self.width, self.height, maze_w, maze_h,
                            self.screen, self.walls, self.data, self,
                            level + 1)
        self.ghosts_data = self.ghost.init_ghosts()
        c_x = int((self.maze.pacman_pos[0] - self.maze.start_x) //
                  self.maze.cell_size)
        c_y = int((self.maze.pacman_pos[1] - self.maze.start_y) //
                  self.maze.cell_size)

        self.ghosts_data['blue']["old_path"] = self.ghost.calculate_ghost_path(
            self.ghosts_data['blue']["pos"], (c_x, c_y))
        self.ghosts_data['yellow'][
            "old_path"] = self.ghost.calculate_ghost_path(
                self.ghosts_data['yellow']["pos"], (c_x, c_y))
        self.ghosts_data['pink']["old_path"] = self.ghost.calculate_ghost_path(
            self.ghosts_data['pink']["pos"], (c_x, c_y))
        self.ghosts_data['red']["old_path"] = self.ghost.calculate_ghost_path(
            self.ghosts_data['red']["pos"], (c_x, c_y))
        return None

    def get_pacgums(self, level: int) -> None:
        """
        Initialize the pacgums available in the current level.

        Generate pacgum positions using the configured number of pacgums
        and the maze walls.

        Args:
            level (int): Zero-based index of the current level.

        Returns:
            None.
        """

        pacgum = self.data["level"][level]['pacgum']
        self.pacgums = self.maze.existing_pacgums(pacgum, self.walls)

    def pause_menu(self) -> int:
        """
        Display the pause menu and handle player interactions.

        Show the available options and detect mouse clicks to determine
        the player's selection.

        Returns:
            int:
                1: Resume the game.
                2: Return to the main menu.
                0: Quit the game.
                3: The menu loop ends without a selection.
        """

        pause_img = pygame.image.load("assists/images/pause_img.jpeg")
        pause_img = pygame.transform.scale(pause_img, (400, 450))
        x = int(self.width * 0.40)
        y = int(self.height * 0.30)
        self.screen.blit(pause_img, (x, y))
        b_x = int(self.width * 0.46)
        b_y = int(self.height * 0.47)
        padding = 0
        run = True
        normal_font = pygame.font.Font("assists/fonts/ka1.ttf", 30)
        hover_font = pygame.font.Font(
            "assists/fonts/PixeloidSansBold-1jpBg.ttf", 30)
        for b in range(3):

            custom_rect(self.screen, (255, 255, 255),
                        (b_x, (b_y + padding), 170, 50))
            custom_rect(self.screen, (223, 124, 0),
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
                custom_rect(self.screen, (223, 124, 0),
                            (button.x + 5, button.y + 5, 160, 40))
                if button.collidepoint(mouse_pos):
                    msg_surface = hover_font.render(msg, True, (25, 25, 166))
                else:
                    msg_surface = normal_font.render(msg, True, (25, 25, 166))
                text_center = msg_surface.get_rect(center=button.center)
                self.screen.blit(msg_surface, text_center)

            pygame.display.update()
        return 3

    def receive_name_player(self, status: str) -> int:
        """
        Ask the player for their name and save their score.

        Args:
            status: The game result, either game_over or win.

        Returns:
            0 after saving the player's name and score.
            1 if the name entry loop ends without saving.
        """
        time.sleep(1)
        background_img = pygame.image.load("assists/images/background.png")
        background_img = pygame.transform.scale(background_img,
                                                (self.width, self.height))
        gamer_img = pygame.image.load("assists/images/gamer.png")
        gamer_img = pygame.transform.scale(gamer_img, (900, 150))
        high_score = pygame.image.load("assists/images/high_score.png")
        score_img = pygame.transform.scale(high_score, (700, 500))
        name = ""
        n_text = pygame.font.Font("assists/fonts/AGENTORANGE.TTF", 32)
        score_font = pygame.font.Font("./assists/fonts/ka1.ttf", 20)
        score_text = score_font.render(f"{str(self.score)} PTS", True,
                                       (255, 255, 255))
        lose_font = pygame.font.Font(
            "assists/fonts/PixeloidSansBold-1jpBg.ttf", 40)
        win_font = pygame.font.Font("assists/fonts/PixeloidSansBold-1jpBg.ttf",
                                    40)
        runing = True
        while runing:
            self.screen.blit(background_img, (0, 0))
            self.screen.blit(gamer_img, (500, 50))
            self.screen.blit(score_img, (610, 400))
            self.screen.blit(score_text,
                             (self.width * 0.48, self.height * 0.58))
            score_img

            if status == "game_over":
                msg = "LOSE"
                msg_text = lose_font.render(msg, True, (255, 0, 0))
                self.screen.blit(msg_text, (900, 220))
            else:
                msg = "WIN"
                msg_text = win_font.render(msg, True, (0, 255, 0))

                self.screen.blit(msg_text, (910, 250))

            for even in pygame.event.get():
                if even.type == pygame.QUIT:
                    sys.exit(0)

                if even.type == pygame.KEYDOWN:
                    if even.key == pygame.K_RETURN:
                        informal = {name: self.score}
                        self.engine.info.append(informal)
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
            new_width = (self.width - name_text.get_width()) // 2
            self.screen.blit(name_text, (new_width, self.height * 0.62))
            if not runing:
                self.engine.info = sorted(
                    self.engine.info,
                    reverse=True,
                    key=lambda player: list(player.values())[0])[:10]
                with open(self.engine.data["highscore_filename"], "w") as file:
                    json.dump(self.engine.info, file, indent=2)
                    self.engine.draw_highscore.draw_high_score(
                        self.engine.info)
                return 0
            pygame.display.update()
        return 1

    def game_level(self, level: int) -> int:
        """
        Run one game level and manage Pac-Man, ghosts, and game events.

        Args:
            level: The index of the current level.

          Returns:
            int:
                0: The player returned to the main menu or finished
                   the game-over name-entry process.
                1: The player completed the current level.
                2: The player lost a life and must restart the level.
               -1: The game loop ended without another result.
        """
        game_over_img = pygame.image.load("assists/images/game_over.png")
        game_over_img = pygame.transform.scale(game_over_img, (800, 200))
        win_img = pygame.image.load("assists/images/win.png")
        win_img = pygame.transform.scale(win_img, (800, 200))

        background_img = pygame.image.load("assists/images/bg_maze.png")

        background_img = pygame.transform.scale(background_img,
                                                (self.width, self.height))

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
                        for button in self.engine.draw_highscore.buttons:
                            if button.collidepoint(event.pos):
                                return 0
                if event.type == pygame.KEYDOWN:
                    # cheat_Mode
                    if event.key == pygame.K_p:
                        if level == len(self.data['level']) - 1:
                            x = self.maze.start_x + (
                                self.maze.maze_pixel_w -
                                game_over_img.get_width()) // 2
                            y = self.maze.start_y + (
                                (self.maze.maze_pixel_h -
                                 game_over_img.get_height()) //
                                2) - self.maze.cell_size
                            self.screen.blit(win_img, (x, y))
                            pygame.display.update()
                        return 1
                    elif event.key == pygame.K_g:
                        if self.is_invincibile:
                            self.is_invincibile = False
                        else:
                            self.is_invincibile = True
                    elif event.key == pygame.K_t:
                        if self.cheat_time:
                            self.time = self.real_time
                            self.cheat_time = False
                        else:
                            self.time = 9999
                            self.cheat_time = True

                    # pause_game
                    if event.key == pygame.K_SPACE and not game_pause:
                        time_pause = pygame.time.get_ticks() - start_ticks
                        game_pause = True
                        pause = self.pause_menu()
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
                    self.screen.blit(background_img, (0, 0))
                    mouse_pos: Tuple = pygame.mouse.get_pos()

                    self.engine.draw_highscore.draw_back_button(
                        mouse_pos, "BACK TO HOME")

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
                    if not self.pacgums:
                        time.sleep(1)
                        if level == len(self.data['level']) - 1:
                            x = self.maze.start_x + (
                                self.maze.maze_pixel_w -
                                game_over_img.get_width()) // 2
                            y = self.maze.start_y + (
                                (self.maze.maze_pixel_h -
                                 game_over_img.get_height()) //
                                2) - self.maze.cell_size
                            self.screen.blit(win_img, (x, y))
                            pygame.display.update()
                        return 1
                    if reached:
                        next_target = None
                        if next_direction is not None:
                            next_target = self.pacman.target_pacman(
                                self.maze.pacman_pos, next_direction,
                                self.walls)

                        if next_target is not None:
                            direction = next_direction
                            current_target = next_target
                            next_direction = None

                        elif direction is not None:
                            current_target = self.pacman.target_pacman(
                                self.maze.pacman_pos, direction, self.walls)
                            if current_target is None:
                                direction = "blocked"
                                next_direction = None
                    if current_target is not None:
                        reached = self.pacman.move_pacman(
                            self.maze.pacman_pos, current_target, speed)
                        if reached:
                            current_target = None
                    else:
                        reached = True

                    if self.maze.menu_maze(start_ticks):
                        self.lives -= 1
                        if self.lives <= 0:
                            game_over = True
                        else:
                            return 2
                    self.maze.draw_maze(self.walls)
                    self.maze.draw_all_pacgums(self.pacgums)
                    self.pacman.draw_face(self.maze.pacman_pos, direction)
                    self.maze.eats_pacgums(self.pacgums)
                    # ghost
                    for specter in self.ghosts_data.values():
                        old_path = specter["old_path"]
                        if specter["current_pos"] + 1 < len(old_path):
                            start_cell = old_path[specter["current_pos"]]
                            target_cell = old_path[specter["current_pos"] + 1]
                        else:
                            start_cell = old_path[-1]
                            target_cell = old_path[-1]
                        pacman_pos = self.ghost.ghosts_brain(
                            specter, direction, self.maze.pacman_pos)
                        if self.ghost.is_eat_super_pacgums(
                                self.maze.pacman_pos):
                            self.ghost.Scared_Mode = True
                            for g in self.ghosts_data.keys():
                                self.ghosts_data[g]["add_score"] = False
                                self.ghosts_data[g]["remain"] = False
                                self.ghosts_data[g]["scared_pos"] = None
                            start_eat = pygame.time.get_ticks()
                        if self.ghost.Scared_Mode:
                            self.ghost.was_eaten_ghosts(
                                self.ghosts_data, self.maze.pacman_pos)
                            self.ghost.scared(start_cell, target_cell,
                                              specter["total_speed"], specter,
                                              start_eat)

                            self.ghost.create_random_path(
                                self.maze.pacman_pos, specter)
                            if specter["move_now"] >= specter["total_speed"]:
                                specter["move_now"] = 0
                                specter["current_frame"] += 1
                                if specter["current_pos"] + 1 < len(old_path):
                                    ghost_reached_cell = \
                                        old_path[specter["current_pos"] + 1]
                                else:
                                    ghost_reached_cell = old_path[-1]
                                if specter["was_eaten"]:
                                    new_path = self.ghost.calculate_ghost_path(
                                        ghost_reached_cell, specter["my_pos"])
                                else:
                                    new_path = self.ghost.calculate_ghost_path(
                                        ghost_reached_cell,
                                        specter["scared_pos"])
                                specter["old_path"] = new_path
                        else:
                            specter["add_score"] = False
                            specter["remain"] = False
                            specter["scared_pos"] = None
                            specter["was_eaten"] = False
                            self.ghost.chase(start_cell, target_cell,
                                             specter["total_speed"], specter)
                            if not self.is_invincibile:
                                if self.ghost.is_caught(
                                        self.ghosts_data,
                                        self.maze.pacman_pos):
                                    self.lives -= 1
                                    if self.lives <= 0:
                                        game_over = True
                                    else:
                                        return 2
                            if specter["move_now"] >= specter["total_speed"]:
                                specter["move_now"] = 0
                                specter["current_frame"] += 1
                                if specter["current_pos"] + 1 < len(old_path):
                                    ghost_reached_cell = \
                                        old_path[specter["current_pos"] + 1]
                                else:
                                    ghost_reached_cell = old_path[-1]
                                new_path = self.ghost.calculate_ghost_path(
                                    ghost_reached_cell, pacman_pos)
                                specter["old_path"] = new_path
                        specter["move_now"] += 2

                    clock.tick(60)
                    pygame.display.update()
                else:
                    # game over
                    x = self.maze.start_x + (self.maze.maze_pixel_w -
                                             game_over_img.get_width()) // 2
                    y = self.maze.start_y + (
                        (self.maze.maze_pixel_h - game_over_img.get_height())
                        // 2) - self.maze.cell_size
                    self.screen.blit(game_over_img, (x, y))
                    pygame.display.update()
                    if self.receive_name_player("game_over") == 0:
                        return 0
                    clock.tick(60)
                    pygame.display.update()
        return -1

    def redraw_maze(self) -> int:
        """
        Manage game progression across all configured levels.

        Initialize each level, run its gameplay loop, handle level
        transitions and restarts, and display the final high-score
        screen when all levels are completed.

        Returns:
            int:
                0: The game session ended or returned to the main menu.
        """

        level = 0
        self.set_objects(level)
        self.get_pacgums(level)
        while level in range(len(self.data['level']) - 1):
            game = self.game_level(level)
            if game == 1:
                level += 1
                self.set_objects(level)
                self.get_pacgums(level)
            if game == 0:
                return 0
            if game == 2:
                self.set_objects(level)
        self.game_level(level)
        self.receive_name_player("win")
        self.engine.draw_highscore.draw_high_score(self.engine.info)
        return 0
