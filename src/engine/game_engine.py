import pygame
from src.engine.splash_screen import DrawSplash
from src.engine.main_menu import Draw_main
from src.highscore import Draw_highscores


class Engine:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        pygame.init()
        # pygame.mixer.init()
        pygame.font.init()
        # pygame.mixer.music.load("./assists/audios/background.mp3")
        # pygame.mixer.music.play(-1)
        self.screen = pygame.display.set_mode((self.width, self.height))
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
        self.draw_splash = DrawSplash(self.width, self.height, self.screen,
                                      self.colors)
        self.draw_highscore = Draw_highscores(self.screen, self.colors, self.width, self.height, {"mas3oood": 110,"cheb laarbi": 2900,"chaba soad": 1011, "hicham smati": 3434})
        
        self.draw_main = Draw_main(self.width, self.height, self.screen,self.colors)




    def run_engine(self):
        self.draw_splash.show_splash()
        flag = self.draw_main.Draw_menu()
        while self.running:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if flag == 0:
                exit(0)
            if flag == 1:
                score_flag = self.draw_highscore.draw_high_score()
                if score_flag == 1:
                    flag = self.draw_main.Draw_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

