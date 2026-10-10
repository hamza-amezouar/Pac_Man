import pygame
from src.engine.splash_screen import DrawSplash
from src.engine.main_menu import Draw_main
from src.highscore import Draw_highscores
from src.models.maze import Maze
from src.models.screen_maze import redraw_maze
from src.config_parser import Parse




class Engine:

    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.data:Parse = Parse().get_data()
        pygame.init()
        # pygame.mixer.init()
        pygame.font.init()
        # pygame.mixer.music.load("./assists/audios/background.mp3")
        # pygame.mixer.music.play(-1)
        self.screen: pygame.surface.Surface = pygame.display.set_mode(
            (self.width, self.height))
        self.running = True
        self.colors = {
            "yellow": (255, 255, 0),
            "dark": (0, 0, 0),
            "deep_blue": (25, 25, 166),
            "blue": (33, 33, 222),
            "warm_peach": (222, 161, 133),
            "red": (253, 1, 0),
            "green": (0, 255, 1),
            "yellow_dark": (223, 124, 0),
            "main": (0, 0, 36),
            "buttons": (0, 14, 90),
            "gray": (142, 151, 160),
            "white": (255, 255, 255),
            "blue_light": (0, 0, 71),
            "background": (0, 0, 26),
            "profile_bg": (17, 26, 43),
            "rank_number": (137, 151, 176),
            "rank_1": (244, 211, 90),
            "rank_2": (167, 197, 237),
            "rank_3": (201, 151, 109)
        }
        self.draw_splash: DrawSplash = DrawSplash(self.width, self.height,
                                                  self.screen, self.colors)
        self.draw_highscore: Draw_highscores = Draw_highscores(
            self.screen, self.colors, self.width, self.height, {
                "mas3oood": 110,
                "cheb laarbi": 2900,
                "chaba soad": 1011,
                "hicham smati": 3434
            })

        self.draw_main: Draw_main = Draw_main(self.width, self.height,
                                              self.screen, self.colors)
        self.maze_w = self.data['level'][0]['width']
        self.maze_h = self.data['level'][0]['height']
        seed = self.data['seed']
        self.pacgum = self.data['level'][0]['pacgum']
        self.maze = Maze(size=(self.maze_w, self.maze_h), seed=seed, level=1)
        self.walls = self.maze.get_walls()

    def run_engine(self) -> None:
        #self.draw_splash.show_splash()
        #flag: int = self.draw_main.Draw_menu()
        score_flag = redraw_maze(self.width, self.height, self.maze_w, self.maze_h, self.screen, self.walls, self.pacgum)
        while self.running:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if flag == 0:
                score_flag = redraw_maze(self.width, self.height, self.maze_w, self.maze_h, self.screen, self.walls, self.pacgum)
                if score_flag == 0:
                    flag = self.draw_main.Draw_menu()

            if flag == 1:
                score_flag: int = self.draw_highscore.draw_high_score()
                if score_flag == 0:
                    flag = self.draw_main.Draw_menu()
            if flag == 3:
                exit(0)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   self.running = False
